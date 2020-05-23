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

"""Scrap script

This module closure the scrapper to scraps online a collection of data of
Allrecipes and prepare it as JSON format to save into Elasticsearch.
"""

import json
from typing import Dict

import requests
from bs4 import BeautifulSoup


def scrap(url: str, headers: Dict[str, str]) -> json:
    """This function scraps a recipe of Allrecipes, given its URL,
    and prepare a JSON file to index in Elasticsearch.

    :param url: the URL of the recipe
    :param headers: the headers to prepare the request
    :return: the recipe as JSON
    :raise: ConnectionError, if the connection against Allrecipes crashes
    """

    # Data schema
    title = ''
    description = ''
    ingredients = []
    nutrition = ''

    # Recipe dictionary
    recipe = dict()

    try:
        request = requests.get(url, headers=headers)

        if request.ok:
            html = request.text
            soup = BeautifulSoup(html, 'lxml')
            # Title
            title_section = soup.select('h1')
            # Description
            description_section = soup.select('.recipe-summary p')
            # Ingredients
            ingredients_section = soup.select('.ingredients-section')
            # Calories
            nutrition_section = soup.select('.recipe-nutrition-section')

            # Pass the data
            if title_section:
                title = title_section[0].text

            if description_section:
                description = description_section[0].text.strip()

            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text \
                            and ingredient_text != '':
                        ingredients.append(ingredient.text.strip())

            if nutrition_section:
                nutrition = nutrition_section[0].text.strip()

            recipe = {'title': title,
                      'description': description,
                      'ingredients': ingredients,
                      'nutrition': nutrition}
    except Exception:
        raise ConnectionError('Exception while parsing')
    finally:
        return json.dumps(recipe)
