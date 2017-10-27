import logging
import pickle

from requests.exceptions import ChunkedEncodingError

from file_operations import save_pickle, load_pickle
from settings import ARTICLES_FILENAME_TEMPLATE
from download.wiki_api_utils import run_query, is_query_finished, handle_query_continuation
from base_wiki_config import NAMESPACES, TAG_QUERY, TAG_PAGES

from tools.unique_category_generator import CategoryLoaderMixin
from tools.utils import batch

CATEGORIES_BUGS = []


class RawArticle:

    def __init__(self, pageid, title, content):
        self.pageid = pageid
        self.title = title
        self.content = content

    def __repr__(self):
        return "(%s, %s, %s)" % (self.pageid, self.title, self.content[:100])


class ArticleScraper(CategoryLoaderMixin):
    """Class to download articles in given list of categories.
    Should avoid serializing on the hard drive duplicated articles and run basic tests for article relevancy.

    Usage:
    ArticleScraper(category_matcher, data_dir).download_articles().
    """

    def __init__(self, category_matcher, data_dir):
        super().__init__(data_dir)

        self.category_matcher = category_matcher
        self.data_dir = data_dir

        self.visited_article_ids_filename = self.data_dir + '/visited_article_ids.pickle'
        self.downloaded_articles_ids = set()
        self.load_visited_ids()

    def load_visited_ids(self):
        visited_ids = load_pickle(self.visited_article_ids_filename)
        if len(visited_ids) > 0:
            self.downloaded_articles_ids = visited_ids

    def download_articles(self):
        categories = self.load_category_list()
        categories = set(filter(self.category_matcher.is_category_relevant, categories))

        index = 0
        for category_batch in batch(list(categories), 1000):
            articles = self.get_articles_for_categories(category_batch)
            self.save_articles_to_file(articles, index)

            save_pickle(self.downloaded_articles_ids, self.visited_article_ids_filename)

            index += 1000

        print(CATEGORIES_BUGS)

    def get_articles_for_categories(self, categories):
        articles = []

        for category in categories:
            query = self.get_default_article_query(category)
            articles += self.get_articles(query)

        return articles

    def get_articles(self, query):
        print(query["gcmtitle"])

        try:
            result = run_query(query)
        except ChunkedEncodingError as e:
            logging.error("Error while trying to download articles for query: {0}".format(query["gcmtitle"]))
            return []

        if not self.is_response_valid(query, result):
            return []

        found_articles = result[TAG_QUERY][TAG_PAGES]

        articles = []
        for article in found_articles:
            if "revisions" not in article:
                continue

            page_id = article["pageid"]
            title = article["title"]
            namespace = article["ns"]
            content = article["revisions"][0]["content"]

            if namespace == NAMESPACES["article"] and page_id not in self.downloaded_articles_ids \
                    and self.category_matcher.is_article_relevant(title, content):
                articles.append(RawArticle(page_id, title, content))
                self.downloaded_articles_ids.add(page_id)

        if not is_query_finished(result):
            print('continuation query required')
            query = handle_query_continuation(query, result)
            more_articles = self.get_articles(query)
            articles = articles + more_articles

        return articles

    @staticmethod
    def get_default_article_query(title=""):
        return {
            "action": "query",
            "generator": "categorymembers",
            "gcmlimit": "max",
            "format": "json",
            "gcmtitle": title,
            "prop": "revisions",
            "rvprop": "content",
            # "rvlimit" : 1,
            "gcmnamespace": NAMESPACES["article"],  # cmnamespace
            "formatversion": 2
        }

    @staticmethod
    def is_response_valid(query, result):
        if "query" not in result:
            CATEGORIES_BUGS.append(query["gcmtitle"])
            logging.warning("Invalid category: " + query["gcmtitle"])
            if "warnings" in result:
                try:
                    logging.warning(query["gcmtitle"] + " returned no results: " + str(result["warnings"]["main"]))
                except (TypeError, KeyError) as e:
                    logging.error("Error while logging: {0} ".format(e))

            return False

        return True

    def save_articles_to_file(self, articles, index):
        filename = self.data_dir + '/' + ARTICLES_FILENAME_TEMPLATE.format(index)
        with open(filename, 'wb') as f:
            pickle.dump(articles, f)
