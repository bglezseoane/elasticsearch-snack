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

"""TUI module

This module manages a TUI for this project.
"""

import sys

from elasticsearch import Elasticsearch

from elasticsearch_snack.elasticsearch_manager import connect_elasticsearch, \
    create_snack_recipes_index, index_snack_recipes, search
from elasticsearch_snack.properties import ELASTICSEARCH_SERVER_HOST
from elasticsearch_snack.scrapper import scrap_allrecipes_snack_recipes

# Print style macros
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RST_COLOR = '\033[0m'


def print_main_menu() -> None:
    """Prints the main menu"""
    print('\nAvailable actions:')
    print(f'    * {BLUE}d{RST_COLOR}: Download the data collection from '
          f'Allrecipes')
    print(f'    * {BLUE}i{RST_COLOR}: Reindex the data collection on '
          f'Elasticsearch')
    print(f'    * {BLUE}s{RST_COLOR}: Search something')
    print(f'    * {BLUE}q{RST_COLOR}: Quit')


def print_search_menu() -> None:
    """Prints the search menu"""
    print('Configuring your search:')
    print(f'    * {BLUE}t{RST_COLOR}: Set title to match')
    print(f'    * {BLUE}d{RST_COLOR}: Add description keywords to match')
    print(f'    * {BLUE}i{RST_COLOR}: Add ingredients to match')
    print(f'    * {BLUE}c{RST_COLOR}: Set the maximum of calories to filter')
    print(f'    * {BLUE}r{RST_COLOR}: Run the search')
    print(f'    * {BLUE}b{RST_COLOR}: Return to the main menu')


def parse_input_opt(possible_opts: [str]) -> str:
    """Asks and parses an user input option

    :param possible_opts: a list with the legal options.
    :return: the user input option code as string.
    """
    input_opt = None
    while not input_opt:
        input_opt = input('\nWrite the option code: ')
        if input_opt not in possible_opts:
            print(f'{RED}[ERROR]:{RST_COLOR} Unrecognised option. Try again...')
            input_opt = None
    return input_opt


def run_opt(opt: str, es_object: Elasticsearch) -> None:
    """Runs the correct action given an option code

    :param opt: the option to run.
    :param es_object: the Elasticsearch object instance
    :raise SyntaxError: if the option is illegal.
    """
    if opt == 'q':
        sys.exit(0)  # Finish
    elif opt == 'd':
        print('Downloading data... This process may take a while')
        scrap_allrecipes_snack_recipes()
        print(f'{GREEN}[OK]:{RST_COLOR} Data collection dowloaded')
    elif opt == 'i':
        try:
            es_object.ping()
            # Create an index for the recipes and add our scrapped ones
            create_snack_recipes_index(es_object)
            print(f'{GREEN}[OK]:{RST_COLOR} Created index to store the data')
            index_snack_recipes(es_object)
            print(f'{GREEN}[OK]:{RST_COLOR} Data indexed')
        except Exception:
            print(f'{RED}[ERROR]:{RST_COLOR} Error during the process. Have '
                  f'you connected Elasticsearch? Use option \'c\' to check it.')
    elif opt == 's':
        run_search(es_object)
    else:
        """This not occur if the option is asked by 'parse_input_opt()' and
        this switch is exhaustive with 'possible_opts' list"""
        raise SyntaxError('Illegal option')


def run_search(es_object: Elasticsearch) -> None:
    """Configures, runs a search and prints the results

    :param es_object: the Elasticsearch object instance
    :raise SyntaxError: if the option is illegal.
    """
    possible_opts = ['t', 'd', 'i', 'c', 'r', 'b']

    try:
        es_object.ping()  # Check connection

        # Searching components
        title = None
        description_keywords = []
        ingredients = []
        calories = None

        while True:  # The user exits by himself with 'r' or 'b'
            print_search_menu()
            opt = parse_input_opt(possible_opts)

            if opt == 'b':
                return  # Go back
            elif opt == 'r':
                break  # Continue
            elif opt == 't':
                title = input('Input the desired title to search: ')
            elif opt == 'd':
                description_keywords = input('Input the desired keywords to '
                                             'search in the recipe description '
                                             'separated by commas: ')
                description_keywords = \
                    description_keywords.replace(' ', '').split(',')
            elif opt == 'i':
                ingredients = input('Input the desired ingredients to search'
                                    'separated by commas: ')
                ingredients = \
                    ingredients.replace(' ', '').split(',')
            elif opt == 'c':
                calories = input('Input the desired maximum of calories '
                                 'filter: ')
                try:
                    calories = int(calories)
                except ValueError:
                    print(f'{RED}[ERROR]:{RST_COLOR} The calories maximun '
                          f'filter must be an integer value. Try again...')
                    calories = None
            else:
                """This not occur if the option is asked by 'parse_input_opt()'
                and this switch is exhaustive with 'possible_opts' list"""
                raise SyntaxError('Illegal option')

        # Compound the search object
        match_title = None
        match_keywords = None
        match_ingredients = None
        filter_calories = None
        if title or description_keywords or ingredients or calories:
            if title:
                match_title = {'match': {'title': title}}
            if description_keywords:
                match_keywords = \
                    {'bool': {'must': [{'match': {'description': kw}} for
                                       kw in description_keywords]}}
            if ingredients:
                match_ingredients = \
                    {'bool': {'must': [{'match': {'ingredients': i}} for
                                       i in ingredients]}}
            if calories:
                filter_calories = \
                    {'range': {'calories': {'lte': calories}}}

            # Merge the search subelements
            match_hand = None
            filter_hand = None
            match_hand_parts = [match_title, match_keywords, match_ingredients]
            match_hand_true_parts = [p for p in match_hand_parts if p]
            n_match_hand_parts = sum([1 for p in match_hand_parts if p])
            if n_match_hand_parts >= 1:
                if n_match_hand_parts > 1:
                    match_hand = {'bool': {'must': match_hand_true_parts}}
                else:
                    match_hand = match_hand_true_parts[0]
            if filter_calories:
                filter_hand = filter_calories

            # Merge the search elements
            if match_hand and filter_hand:
                merged_hands = {'must': match_hand}
                merged_hands.update({'filter': filter_hand})
                merged_hands = {'bool': merged_hands}
                search_object = \
                    {'query': merged_hands}
            elif match_hand:
                search_object = {'query': match_hand}
            else:
                search_object = {'query': filter_hand}
        else:
            print(f'{RED}[ERROR]:{RST_COLOR} You have to try to search '
                  f'anything. Try again...')
            return

        # Run the search
        res = search(es_object, search_object)

        # Access results ignoring metadata
        results = res['hits']['hits']
        if results:
            for result in results:
                print(result['_source']['title'])
        else:
            print('There are not results to show...')
    except Exception:
        print(f'{RED}[ERROR]:{RST_COLOR} Error during the process. Have you '
              f'connected Elasticsearch? Use option \'c\' to check it.')


def start_tui() -> None:
    """This function starts the conversation with the user and launches all

    Really is simply an infinite loop, because the user finish the exection
    with the quit option.
    """

    # The possible options to run by the user
    possible_opts = ['d', 'i', 's', 'q']

    print(f'{BLUE}Welcome to Elasticsearch Snack!{RST_COLOR}')

    try:
        print(f'Connecting to the Elasticsearch server using the host '
              f'\'{ELASTICSEARCH_SERVER_HOST}\'...')
        es = connect_elasticsearch()
        print(f'{GREEN}[OK]:{RST_COLOR} Connected to Elasticsearch')
    except ConnectionError:
        print(f'{RED}[ERROR]:{RST_COLOR} Elasticsearch unreachable. Have '
              f'you started the server?')
        sys.exit(1)  # Quit with error

    # With connection success
    while True:  # While the user do not exists with 'q'
        print_main_menu()
        run_opt(parse_input_opt(possible_opts), es)
