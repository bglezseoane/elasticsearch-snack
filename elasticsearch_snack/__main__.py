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

"""Main of Elasticsearch Snack"""

from elasticsearch_snack.tui import start_tui

if __name__ == '__main__':
    start_tui()
