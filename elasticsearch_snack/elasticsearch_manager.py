# -*- coding: utf-8 -*-

###########################################################
# Elasticsearch Snack 0.0dev0
#
# A brief example case indexing recipes with Elasticsearch,
# Python and Docker containers
#
# Copyright 2020 Borja González Seoane
#
# Contact: borja.gseoane@udc.es
###########################################################

"""Elasticsearch manager module

This module closure a set of functions to manage Elasticsearch.
"""

import json
from typing import Dict

from elasticsearch import Elasticsearch

from elasticsearch_snack.properties import INDEX_NAME, \
    RECIPES_COLLECTION_FILENAME, ELASTICSEARCH_SERVER_HOST


def connect_elasticsearch() -> Elasticsearch:
    """This function starts and verifies the connection with Elasticsearch

    :return: the Elasticsearch object instance
    :raise ConnectionError: if Elasticsearch is unreachable
    """
    es = Elasticsearch(ELASTICSEARCH_SERVER_HOST)
    if not es.ping():
        raise ConnectionError('Elasticsearch unreachable')
    return es


def create_snack_recipes_index(es_object: Elasticsearch) -> None:
    """This function creates an Elasticsearch index to store Allrecipes recipes

    This function creates an index to store the scrapped Allrecipes snack
    recipes into Elasticsearch.

    Warning: If the index already exists, this function overwrites it.

    :param es_object: the Elasticsearch object instance
    :raise Exception: for any error during the creation process
    """

    # Index settings
    settings = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0
        },
        'mappings': {
            'members': {
                'dynamic': 'strict',
                'properties': {
                    'title': {
                        'type': 'text'
                    },
                    'description': {
                        'type': 'text'
                    },
                    'ingredients': {
                        'type': 'text'
                    },
                    'calories': {
                        'type': 'integer'
                    },
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(INDEX_NAME):
            # Ignore 400 to ignore "Index already exist" error
            es_object.indices.create(index=INDEX_NAME,
                                     ignore=400,
                                     body=settings)
    except Exception:
        raise Exception('Error during the index creation process')


def index_snack_recipes(es_object: Elasticsearch) -> None:
    """Index scrapped Allrecipes snack recipes

    This function index the scrapped and saved to a JSON file Allrecipes
    snack recipes to an Elasticsearch "recipes" index.

    :param es_object: the Elasticsearch object instance
    :raise FileNotFoundError: if the data collection file is missed
    :raise Exception: for any error during the indexation process
    """
    try:
        with open(RECIPES_COLLECTION_FILENAME, 'rb') as f:
            recipes = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(RECIPES_COLLECTION_FILENAME)

    try:
        for recipe in recipes:
            es_object.index(index=INDEX_NAME, body=recipe)
    except Exception:
        raise Exception('Error in indexing data')


def search(es_object: Elasticsearch, search_object: Dict) -> Dict:
    """Run a search on a Elasticsearch instance

    :param es_object: the Elasticsearch object instance
    :param search_object: the query ro run
    :return: the result of the query
    """
    return es_object.search(index=INDEX_NAME, body=search_object)
