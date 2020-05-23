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

import json
from time import sleep

import requests
from bs4 import BeautifulSoup

from elasticsearch_snack.scrapper import scrap

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }

    # noinspection PyShadowingNames
    def append_json(new_data: json, filename: str) -> None:
        """Function to append more data to a JSON file"""
        merged_data = []
        try:
            with open(filename, "rb") as f:
                merged_data.append(json.load(f))
            merged_data.append(new_data)
            with open(filename, "w") as f:
                json.dump(merged_data, f, indent=4)
        except FileNotFoundError:
            with open(filename, "x") as f:
                json.dump(new_data, f, indent=4)

    filename = 'data-collection.json'  # The file to store the scrapped data
    url = 'https://www.allrecipes.com/recipes/76/appetizers-and-snacks/'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('.fixed-recipe-card__h3 a')

        scrapped_texts = []
        for link in links:
            sleep(2)
            scrapped_texts.append(scrap(link['href'], headers))

        append_json(scrapped_texts, filename)
