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

"""Scrap module

This module closure the scrapper to scraps online a collection of data of
Allrecipes and prepare it as JSON format to save into Elasticsearch.
"""

import json
from time import sleep

import requests
from bs4 import BeautifulSoup

from elasticsearch_snack.properties import ALLRECIPES_SNACKS_PAGE_URL, \
    RECIPES_COLLECTION_FILENAME


def scrap_allrecipes_recipe(url: str) -> json:
    """This function scraps a recipe of Allrecipes, given its URL,
    and prepare a JSON file to index in Elasticsearch.

    :param url: the URL of the recipe
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
        request = requests.get(url)
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
        else:
            raise ConnectionError('Exception trying yo connect with Allrecipes')
    except Exception:
        raise Exception('Exception while parsing')
    finally:
        return json.dumps(recipe)


def scrap_allrecipes_snack_recipes() -> None:
    """This function scraps all the snack recipes of Allrecipes and saves
    the information to a JSON file to index in Elasticsearch.

    :raise: ConnectionError, if the connection against Allrecipes crashes
    """

    # noinspection PyShadowingNames
    def append_json(new_data: json, filename: str) -> None:
        """Function to append more data to a JSON file"""
        merged_data = []
        try:
            with open(filename, 'rb') as f:
                merged_data.append(json.load(f))
            merged_data.append(new_data)
            with open(filename, 'w') as f:
                json.dump(merged_data, f, indent=4)
        except FileNotFoundError:
            with open(filename, 'x') as f:
                json.dump(new_data, f, indent=4)

    request = requests.get(ALLRECIPES_SNACKS_PAGE_URL)
    if request.ok:
        html = request.text
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('.fixed-recipe-card__h3 a')

        scrapped_texts = []
        for link in links:
            sleep(2)
            scrapped_texts.append(scrap_allrecipes_recipe(link['href']))

        append_json(scrapped_texts, RECIPES_COLLECTION_FILENAME)
    else:
        raise ConnectionError('Exception trying yo connect with Allrecipes')

