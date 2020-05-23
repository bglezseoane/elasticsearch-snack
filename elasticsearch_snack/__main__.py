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

"""Main of Elasticsearch snack"""

from elasticsearch_snack.scrapper import scrap_allrecipes_snack_recipes

if __name__ == '__main__':
    scrap_allrecipes_snack_recipes()
