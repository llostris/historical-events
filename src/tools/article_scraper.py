import logging
import pickle

from requests.exceptions import ChunkedEncodingError
from tqdm import tqdm

from base_wiki_config import NAMESPACES, TAG_QUERY, TAG_PAGES
from file_operations import save_pickle, load_pickle
from settings import ARTICLES_FILENAME_TEMPLATE, get_wiki_logger
from tools.unique_category_generator import CategoryLoaderMixin
from tools.utils import batch
from tools.wiki_api_utils import run_query, is_query_finished, handle_query_continuation

CATEGORIES_BUGS = []

logger = get_wiki_logger()


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
        self.downloaded_articles_ids = load_pickle(self.visited_article_ids_filename, is_set=True)

    def download_articles(self, start=0, end=None, step=1000):
        categories = self.load_category_list()

        categories = list(filter(self.category_matcher.is_category_relevant, set(categories)))

        index = start
        for category_batch in batch(categories[start:end], step):
            articles = self.get_articles_for_categories(category_batch)
            self.save_articles_to_file(articles, index)

            save_pickle(self.downloaded_articles_ids, self.visited_article_ids_filename)

            index += step

        print(CATEGORIES_BUGS)

    def get_articles_for_categories(self, categories):
        articles = []

        for category in tqdm(categories, desc="Category batch"):
            query = self.get_default_article_query(category)
            articles += self.get_articles(query)

        return articles

    def get_articles(self, query):
        # print(query["gcmtitle"])

        try:
            result = run_query(query)
        except ChunkedEncodingError as e:
            logger.error("Error while trying to download articles for query: {0}".format(query["gcmtitle"]))
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
            # print('continuation query required')
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
            logger.warning("Invalid category: " + query["gcmtitle"])
            if "warnings" in result:
                try:
                    logger.warning(query["gcmtitle"] + " returned no results: " + str(result["warnings"]["main"]))
                except (TypeError, KeyError) as e:
                    logger.error("Error while logging: {0} ".format(e))

            return False

        return True

    def save_articles_to_file(self, articles, index):
        filename = self.data_dir + '/' + ARTICLES_FILENAME_TEMPLATE.format(index)
        with open(filename, 'wb') as f:
            pickle.dump(articles, f)
