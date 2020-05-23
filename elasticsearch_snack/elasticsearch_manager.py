# -*- coding: utf-8 -*-

###########################################################
# Elasticsearch snack 0.1
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

from elasticsearch import Elasticsearch

from elasticsearch_snack.properties import INDEX_NAME, \
    RECIPES_COLLECTION_FILENAME


def connect_elasticsearch():
    """This function starts and verifies the connection with Elasticsearch

    :raise ConnectionError: if Elasticsearch is unreachable
    """
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('[OK]: Elasticsearch reachable')
    else:
        raise ConnectionError('Elasticsearch unreachable')
    return es


def create_snack_recipes_index(es_object):
    """This function creates an Elasticsearch index to store Allrecipes recipes

    This function creates an index to store the scrapped Allrecipes snack
    recipes into Elasticsearch.

    Warning: If the index already exists, this function overwrites it.

    :param es_object: the Elasticsearch object instance
    :raise Exception: for any error during the creation process
    """

    index_name = 'recipes'

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
                    'nutrition': {
                        'type': 'text'
                    },
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 to ignore "Index already exist" error
            es_object.indices.create(index=index_name,
                                     ignore=400,
                                     body=settings)
            print('[OK]: Index created')
    except Exception:
        raise Exception('Error during the index creation process')


def index_snack_recipes(es_object: Elasticsearch) -> None:
    """Index scrapped Allrecipes snack recipes

    This function index the scrapped and saved to a JSON file Allrecipes
    snack recipes to an Elasticsearch "recipes" index.

    :param es_object: the Elasticsearch object instance
    """
    with open(RECIPES_COLLECTION_FILENAME, 'rb') as f:
        recipes = json.load(f)

    try:
        for recipe in recipes:
            es_object.index(index=INDEX_NAME, body=recipe)
    except Exception:
        raise Exception('Error in indexing data')
