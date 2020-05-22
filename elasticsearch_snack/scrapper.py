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

""" Scrap script

This module closure the scrapper to scraps online a collection of data of
Allrecipes and prepare it as JSON format to insire into Elasticsearch.
"""

import json
import requests
from bs4 import BeautifulSoup


def scrap(url: str, headers: str) -> json:
    """ This function scraps a recipe of Allrecipes, given its URL,
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
    calories = 0
    submit_by = ''

    # Recipe dictionary
    recipe = dict()

    try:
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            # Title
            title_section = soup.select('.recipe-summary__h1')
            # Description
            description_section = soup.select('.submitter__description')
            # Ingredients
            ingredients_section = soup.select('.recipe-ingred_txt')
            # Calories
            calories_section = soup.select('.calorie-count')
            # Submitter
            submitter_section = soup.select('.submitter__name')

            # Pass the data
            if title_section:
                title = title_section[0].text

            if description_section:
                description = description_section[0].text.strip().replace('"',
                                                                          '')
            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text \
                            and ingredient_text != '':
                        ingredients.append({'step': ingredient.text.strip()})

            if calories_section:
                calories = calories_section[0].text.replace('cals', '').strip()

            if submitter_section:
                submit_by = submitter_section[0].text.strip()

            recipe = {'title': title,
                      'description': description,
                      'ingredients': ingredients,
                      'calories': calories,
                      'submitter': submit_by}
    except Exception:
        raise ConnectionError('Exception while parsing')
    finally:
        return json.dumps(recipe)
