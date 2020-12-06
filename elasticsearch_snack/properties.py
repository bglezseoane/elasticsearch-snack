# -*- coding: utf-8 -*-

###########################################################
# Elasticsearch Snack 1.1
#
# A brief example case indexing recipes with Elasticsearch,
# Python and Docker containers
#
# Copyright 2020 Borja González Seoane
#
# Contact: borja.gseoane@udc.es
###########################################################

"""Properties module

This file only store some useful properties to generalize
them in the rest of the code.
"""

import os

# The URL of the source of the data collection
ALLRECIPES_SNACKS_PAGE_URL = 'https://www.allrecipes.com/recipes/76' \
                             '/appetizers-and-snacks/'

# The host where the Elasticsearch is run locally
ELASTICSEARCH_SERVER_HOST = 'elasticsearch-snack-server:9200'

# The file to store the scrapped data
RECIPES_COLLECTION_FILENAME = os.path.normpath('../recipes-collection.json')

# The name of the index where store the snack recipes on Elasticsearch
INDEX_NAME = 'recipes'
