from __future__ import annotations
import json
import logging
import sys
from collections import Counter

import numpy as np
from elasticsearch import Elasticsearch

from sommify.data.meat import dictionary

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout.flush())

logger.addHandler(console_handler)
logger.propagate = False


def remove_duplicate_protein(most_common_ings: list[str]) -> list[str]:
    proteins = list(dictionary.keys())
    proteins.append("lean fish")
    protein_found = 0
    for index, ing in enumerate(most_common_ings):
        if ing in proteins:
            if protein_found == 0:
                protein_found = 1
            else:
                most_common_ings.pop(index)
    return most_common_ings


def get_es_connection(
    url: str, user_name: str, password: str, port: int = 9200
) -> Elasticsearch:
    es = Elasticsearch([url], port=port, http_auth=(user_name, password))
    health = es.cluster.health()
    logger.debug(health)
    return es


def search_by_query_term(
    es: Elasticsearch, input_term: str, ings: list[str]
) -> list[str]:
    # len of query
    input_term_len = len(input_term.split(" "))
    size = 100
    logger.info(f"INPUT TERM : {input_term} | TERM LEN :{input_term_len}")

    operator = "and"  # if "and" in input_term else "or"

    q = {
        "bool": {
            "must": [
                {
                    "match": {
                        "plain": {
                            "query": input_term,
                            "analyzer": "englando_v2",
                            "operator": operator,
                        }
                    }
                },
            ]
        }
    }

    # "must": [
    #     {"terms": {"ingredients.value": ings}}

    #     ]

    # main query
    if ings != [] and ings != [None]:
        ings_q = {
            "nested": {
                "path": "ingredients",
                "query": {
                    "bool": {
                        # "must": [{"terms": {"ingredients.value": ings}}]
                        "should": [{"match": {"ingredients.value": i}} for i in ings]
                    }
                },
            }
        }

        q["bool"]["must"].append(ings_q)
        logger.info(f"Adding to query : {ings}")
    # search
    hits = es.search(index="recipes", query=q, size=size)["hits"]
    if len(hits["hits"]) == 0:
        logger.error("Zero recipes found for query. Going dark...")
        # fall back query if main did not found
        q = {
            "match": {
                "plain": {
                    "query": input_term,
                }
            }
        }
        hits = es.search(index="recipes", query=q, size=size)["hits"]

    # get all ings
    all_ings = []
    number_of_hits = len(hits["hits"])
    logger.info(f"Number of hits : {number_of_hits}")

    if number_of_hits == 0:
        raise Exception("No recipes found.")

    for r in hits["hits"]:
        all_ings.extend(i["value"] for i in r["_source"]["ingredients"])
    # calculate thresholds
    ingredient_counts = Counter(all_ings)
    max_count = max(ingredient_counts.values())
    # default search threshold
    upper_fence = np.percentile(list(ingredient_counts.values()), 75) + 1.5 * (
        np.percentile(list(ingredient_counts.values()), 75)
        - np.percentile(list(ingredient_counts.values()), 25)
    )
    upper_fence += 1

    # if query is complitated reduce threshold
    if input_term_len > 1 and max_count <= size / 2 + 1:
        upper_fence = np.percentile(list(ingredient_counts.values()), 50)

    # upper_fence = 1
    logger.info(f"Max number of ings : {max_count} | upper_fence : {upper_fence}")
    # filter ings
    above_upper_fence = {
        ingredient: count
        for ingredient, count in ingredient_counts.items()
        if count > upper_fence
    }
    above_upper_fence = dict(
        sorted(above_upper_fence.items(), key=lambda item: item[1], reverse=True)
    )
    most_common_ings = [
        k
        for k, v in sorted(
            above_upper_fence.items(), key=lambda item: item[1], reverse=True
        )
    ]
    logger.info(json.dumps(above_upper_fence))
    most_common_ings = remove_duplicate_protein(most_common_ings)

    recipe_title = hits["hits"][0]["_source"]["title"]
    logger.info(f"Recipe title : {recipe_title}")
    return (
        recipe_title,
        most_common_ings,
        hits["hits"][0]["_source"]["steps"].split("."),
    )
