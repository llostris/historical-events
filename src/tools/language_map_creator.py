import pickle

import os

from file_operations import load_pickle, save_pickle
from settings import LANGUAGE_MAP_FILENAME
from tools.utils import batch


class LanguageMapCreator:

    def __init__(self, data_dir: str, init=False):
        self.data_dir = data_dir
        self.language_map_filename = data_dir + '/' + LANGUAGE_MAP_FILENAME
        if init:
            self.language_map = {}
        else:
            self.language_map = load_pickle(self.language_map_filename, is_dict=True)

    @staticmethod
    def get_default_langlink_query(title=""):
        return {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "langlinks",
            "formatversion": 2,
            "lllimit": 500
        }

    @staticmethod
    def is_valid_response(result):
        return "query" in result and 'pages' in result['query']

    def get_corresponding_languages_for_query_batch(self, query):
        result = run_query(query)

        if not self.is_valid_response(result):
            return []

        for page in result[TAG_QUERY][TAG_PAGES]:
            self.extract_langlinks(page)

        if not is_query_finished(result):
            print('continuation query required')
            query = handle_query_continuation(query, result)
            add_corresponding_languages_for_batch(query, language_map)

    def extract_langlinks(self, page):
        title = page['title']
        page_id = page['pageid'] if 'pageid' in page else None

        languages = set()
        if TAG_LANGLINKS in page:
            for lang_link in page[TAG_LANGLINKS]:
                lang = lang_link[TAG_LANG]
                languages.add(lang)

        if title in language_map:
            self.language_map[title]["languages"] = language_map[title]["languages"].union(languages)
        else:
            self.language_map[title] = {"languages": languages, "wiki_id": page_id}

        print(title, languages)

    def load_article(self, filename):
        # TODO: move out as it's the same as in graph creator
        return pickle.load(open(self.data_dir + "/" + filename, 'rb'))

    def get_langlinks(self):
        article_files = sorted(filter(lambda x: x.startswith('articles_'), os.listdir(self.data_dir)))

        for file in article_files:
            article_batch = self.load_article(file)

            for query_batch in batch(article_batch, 50):
                titles = [article.title for article in query_batch if article.title not in self.language_map]

                if len(titles) > 0:
                    query = self.get_default_langlink_query()
                    query['titles'] = "|".join(titles)

                    self.get_corresponding_languages_for_query_batch(query)

        save_pickle(self.language_map, self.language_map_filename)
