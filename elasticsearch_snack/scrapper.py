# -*- coding: utf-8 -*-

###########################################################
# Elasticsearch Snack 1.0
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
import re
from time import sleep
from typing import Dict

import requests
from bs4 import BeautifulSoup

from elasticsearch_snack.properties import ALLRECIPES_SNACKS_PAGE_URL, \
    RECIPES_COLLECTION_FILENAME


def scrap_allrecipes_recipe(url: str) -> Dict:
    """This function scraps a recipe of Allrecipes, given its URL,
    and prepare a JSON file to index in Elasticsearch.

    :param url: the URL of the recipe
    :return: the recipe as a JSON-like dictionary
    :raise: ConnectionError, if the connection against Allrecipes crashes
    """

    def filter_noisy_chars(text: str) -> str:
        """Filter in a text new line symbols and excessive spaces"""
        return text.replace('\n', '').replace('  ', '').strip()

    # Data schema
    title = ''
    description = ''
    ingredients = []
    calories = 0

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
                title = filter_noisy_chars(title_section[0].text)

            if description_section:
                description = filter_noisy_chars(description_section[0].text)

            if ingredients_section:
                ingredient_list = ingredients_section[0].text.split('\n')
                ingredient_list = [filter_noisy_chars(i)
                                   for i in ingredient_list]
                # Remove nulls
                ingredient_list = [i for i in ingredient_list if i]

                for ingredient in ingredient_list:
                    ingredients.append(ingredient)

            if nutrition_section:
                nutrition_info = filter_noisy_chars(nutrition_section[0].text)
                calories = re.findall(r'(\d+) calories', nutrition_info)[0]
                calories = int(calories)

            recipe = {'title': title,
                      'description': description,
                      'ingredients': ingredients,
                      'calories': calories}
        else:
            raise ConnectionError('Exception trying yo connect with Allrecipes')
    except Exception:
        raise Exception('Exception while parsing')
    finally:
        return recipe


def scrap_allrecipes_snack_recipes() -> None:
    """This function scraps all the snack recipes of Allrecipes and saves
    the information to a JSON file to index in Elasticsearch.

    :raise: ConnectionError, if the connection against Allrecipes crashes
    """

    # noinspection PyShadowingNames
    def save_json(new_data: json, filename: str) -> None:
        """Function to save data to a JSON file, overwriting it if exists"""
        try:
            with open(filename, 'x') as f:
                json.dump(new_data, f, indent=4)
        except FileExistsError:
            with open(filename, 'w') as f:
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

        save_json(scrapped_texts, RECIPES_COLLECTION_FILENAME)
    else:
        raise ConnectionError('Exception trying yo connect with Allrecipes')
