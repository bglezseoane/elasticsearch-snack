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

import logging

from elasticsearch import Elasticsearch


def connect_elasticsearch():
    """This function starts and verifies the connection with Elasticsearch

    :raise ConnectionError: if Elasticsearch is unreachable
    """
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('Elasticsearch reachable')
    else:
        raise ConnectionError('Elasticsearch unreachable')
    return es
