"""
Downloads a list of categories from Wikipedia using the Wikimedia API. Saves them to categories.csv file. 
Avoids loops by keeping the in-memory list of visited category ids.
"""
# -*- coding: utf-8 -*-

import re

from base_wiki_config import CATEGORYMEMBERS, NAMESPACES
from file_operations import save_pickle, load_pickle
from settings import CATEGORIES_FILENAME
from tools.wiki_api_utils import run_query

DATE_YEAR_IN_REGEXP = re.compile(r"(\d+ .* in)|(in \d+)")


class CategoryScraper:

    def __init__(self, data_dir, category_matcher, continuation=True):
        self.data_dir = data_dir
        self.category_matcher = category_matcher
        self.visited_ids = set()
        self.subcategories_to_visit = set()     # so if we crash we can continue where we left off
        self.subcategories_to_visit_filename = self.data_dir + '/subcategories_to_visit.pickle'
        if continuation:
            self.subcategories_to_visit = load_pickle(self.subcategories_to_visit_filename, is_set=True)
            # If we updated the wiki config file, filter out invalid categories that might have been added
            self.subcategories_to_visit = set(filter(lambda x: category_matcher.is_category_related(x),
                                                     self.subcategories_to_visit))

        self.load_visited_ids()

    @staticmethod
    def get_default_query(title):
        return {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": title,
            "cmlimit": "max",
            "format": "json",
            "cmnamespace": NAMESPACES["category"],
            "cmtype": "subcat",  # didn't use it but should be better (less unnecessary info)
            "formatversion": 2
        }

    def load_visited_ids(self):
        filename = self.data_dir + 'cat_visited_ids.pickle'
        self.visited_ids = load_pickle(filename, is_set=True)

    def save_to_file(self, categories, append=False):
        filename = self.data_dir + '/' + CATEGORIES_FILENAME
        mode = 'w'
        if append:
            mode = 'a'

        with open(filename, mode, encoding='utf-8') as f:
            for id, title in categories.items():
                f.write(str(id) + "," + title + '\n')
            f.close()

    def get_categories(self, query, end=False):
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

                if namespace == NAMESPACES["category"] and self.category_matcher.is_category_related(title):
                    categories[pageid] = title
                    self.subcategories_to_visit.add(title)
                    print('category ' + title)

        subcategories = {}
        print('recurse')
        for id in categories:
            if id not in self.visited_ids:
                query["cmtitle"] = categories[id]
                self.visited_ids.add(id)

                subcategories_new = self.get_categories(query, end=True)
                subcategories.update(subcategories_new)
                print('visited ids length: {}'.format(len(self.visited_ids)))
                self.subcategories_to_visit.remove(categories[id])

        self.save_to_file(subcategories, append=True)
        self.save_visited_ids()
        save_pickle(self.subcategories_to_visit, self.subcategories_to_visit_filename)

        categories.update(subcategories)

        return categories

    def get_all_categories(self, first_category):
        if not self.subcategories_to_visit:
            query = self.get_default_query(first_category)
            categories = self.get_categories(query)
            self.save_to_file(categories, append=False)
        else:
            # TODO: load previously saved categories
            self.subcategories_to_visit = set(filter(lambda x: self.category_matcher.is_category_related(x), self.subcategories_to_visit))
            categories = set()
            subcategories_to_visit = {category for category in self.subcategories_to_visit}
            # we need a copy because categories are removed from this set
            for category in subcategories_to_visit:
                query = self.get_default_query(category)
                new_categories = self.get_categories(query)
                categories.update(new_categories)

    def save_visited_ids(self):
        save_pickle(self.visited_ids, self.data_dir + '/cat_visited_ids.pickle')
