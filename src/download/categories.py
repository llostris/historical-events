"""
Downloads a list of categories from Wikipedia using the Wikimedia API. Saves them to categories.csv file. 
Avoids loops by keeping the in-memory list of visited category ids.
"""
# coding=utf-8
# -*- coding: utf-8 -*-

import os
import pickle
import re
import signal

from settings import DATA_DIR, CATEGORIES_FILE
from wiki_api_utils import run_query
from wiki_config import CATEGORYMEMBERS, NAMESPACES, is_category_relevant, CATEGORY_KEYWORDS

DATE_YEAR_IN_REGEXP = re.compile(r"(\d+ .* in)|(in \d+)")

VISITED_IDS = set()


def signal_handler():
    with open(DATA_DIR + '/cat_visited_ids.pickle', 'wb') as f:
        pickle.dump(VISITED_IDS, f)
        f.close()


def is_category_history_related(category_name):
    category_name = category_name.lower()

    if is_category_relevant(title):
        for keyword in CATEGORY_KEYWORDS:
            if keyword in category_name:
                return True

        if DATE_YEAR_IN_REGEXP.match(category_name):
            return True

    return False


def save_to_file(categories, file=CATEGORIES_FILE, append=False):
    mode = 'w'
    if append:
        mode = 'a'

    with open(file, mode, encoding='utf-8') as f:
        for id, title in categories.items():
            f.write(str(id) + "," + title + '\n')
        f.close()


def get_categories(query, visited_ids, end=False):
    query["cmtitle"] = query["cmtitle"]
    result = run_query(query)
    print('json:', result)

    categories = {}
    if "query" in result:
        found_categories = result["query"][CATEGORYMEMBERS]
        print('results found: %d' % len(found_categories))
        for member in found_categories:
            pageid = member["pageid"]
            title = member["title"]
            namespace = member["ns"]

            if namespace == NAMESPACES["category"] and is_category_history_related(title):
                categories[pageid] = title
                print('category ' + title)

    # if end:
    #     print 'end'
    #     return categories

    subcategories = {}
    print('recurse')
    for id in categories:
        if id not in visited_ids:
            query["cmtitle"] = categories[id]
            visited_ids.add(id)

            subcategories_new = get_categories(query, visited_ids, True)
            subcategories.update(subcategories_new)
            print('visited ids length: {}'.format(len(visited_ids)))

    save_to_file(subcategories, append=True)

    categories.update(subcategories)

    return categories


def load_visited_ids():
    visited_ids = set()
    filename = DATA_DIR + 'cat_visited_ids.pickle'
    if os.path.isfile(filename) :
        with open(filename, 'rb') as f:
            visited_ids = pickle.load(f)

    return visited_ids


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    title = "Category:History"
    query = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": title,
        "cmlimit": "max",
        "format": "json",
        "cmnamespace": NAMESPACES["category"],
        "cmtype": "subcat", # didn't use it but should be better (less unnecessary info)
        "formatversion": 2
    }

    visited_ids = load_visited_ids()
    VISITED_IDS = visited_ids   # save to global variable so signal_handler can access it
    categories = {}
    portals = {}

    categories = get_categories(query, visited_ids, True)
    # try:
    # except Exception as e:
    #     signal_handler()

    # save_to_file(categories)
