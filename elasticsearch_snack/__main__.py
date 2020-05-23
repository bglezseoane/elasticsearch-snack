# -*- coding: utf-8 -*-

###########################################################
# Elasticsearch snack 0.0dev0
#
# A brief example case indexing recipes with Elasticsearch,
# Python and Docker containers
#
# Copyright 2020 Borja González Seoane
#
# Contact: borja.gseoane@udc.es
###########################################################

"""Main of Elasticsearch snack"""

import json

from elasticsearch_snack.elasticsearch_manager import connect_elasticsearch, \
    create_snack_recipes_index, index_snack_recipes, search
from elasticsearch_snack.scrapper import scrap_allrecipes_snack_recipes

if __name__ == '__main__':
    # Firstly scrap snack recipes from Allrecipes
    scrap_allrecipes_snack_recipes()

    # Start the Elasticsearch engine
    es = connect_elasticsearch()

    # Create an index for the recipes and add our scrapped ones
    create_snack_recipes_index(es)
    index_snack_recipes(es)

    # Prepare a query to search a "Bruschetta" recipe and print the results
    search_object = {'query': {'match': {'title': 'Bruschetta'}}}
    results = search(es, json.dumps(search_object))
    print(results)
