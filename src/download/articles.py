import logging
import pickle

from categories import VISITED_IDS
from download.wiki_api_utils import get_default_article_query
from settings import CATEGORIES_FILE, ARTICLES_FILE, DATA_DIR
from wiki_api_utils import run_query, is_query_finished, handle_query_continuation
from wiki_config import NAMESPACES, TAG_QUERY, TAG_PAGES, is_category_relevant, is_article_relevant

# LOGGER = logging.getLogger()
logging.debug('test')
logging.info('test2')

CATEGORIES_BUGS = []


class RawArticle:

    def __init__(self, pageid, title, content):
        self.pageid = pageid
        self.title = title
        self.content = content

    def __repr__(self):
        return "(%s, %s, %s)" % (self.pageid, self.title, self.content[:100])


def signal_handler():
    with open(DATA_DIR + '/article_visited_ids.pickle', 'wb') as f:
        pickle.dump(VISITED_IDS, f)
        f.close()


def load_category_list():
    categories = set()

    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            splitted = line.strip().split(",")
            categories.add(splitted[1])

    return categories


def is_response_valid(query, result):
    if not "query" in result:
        CATEGORIES_BUGS.append(query["gcmtitle"])
        logging.warn("Invalid category: " + query["gcmtitle"])
        if "warnings" in result:
            try:
                logging.warn(query["gcmtitle"] + " returned no results: " + str(result["warnings"]["main"]))
            except (TypeError, KeyError) as e:
                logging.error("Error while logging: {0} ".format(e))

        return False

    return True


def get_articles(query, visited_ids, categories):
    print(query["gcmtitle"])
    result = run_query(query)
    print('json:', result)

    if not is_response_valid(query, result):
        return []

    found_articles = result[TAG_QUERY][TAG_PAGES]

    all_articles = []
    for article in found_articles:
        # print article
        if not "revisions" in article:
            continue
        page_id = article["pageid"]
        title = article["title"]
        namespace = article["ns"]
        content = article["revisions"][0]["content"]
        # print title, namespace

        if namespace == NAMESPACES["article"] and is_article_relevant(title, content):
            all_articles.append(RawArticle(page_id, title, content))
            visited_ids.add(page_id)

    if not is_query_finished(result):
        print('continuation query required')
        query = handle_query_continuation(query, result)
        more_articles = get_articles(query, visited_ids, categories)
        all_articles = all_articles + more_articles

    return all_articles


def get_articles_for_categories(query, categories):
    articles = []
    visited_ids = set()

    for category in categories:
        print('querying')

        query = get_default_article_query(category)
        articles += get_articles(query, visited_ids, categories)

        print(len(articles))

    return articles


def save_to_file(articles, index):
    with open(ARTICLES_FILE + '_' + str(index), 'wb') as f:
        pickle.dump(articles, f)


if __name__ == "__main__":
    query = get_default_article_query()

    categories = load_category_list()
    print(len(categories))
    categories = set(filter(is_category_relevant, categories))
    print(len(categories))
    articles = {}

    num_categories = len(categories)
    start = 0
    last_index = start

    # Split into batches to allow for easier re-running the script and fixing errors
    for index in range(start, num_categories, 1000):
        articles = get_articles_for_categories(query, set(list(categories)[index:index + 1000]))

        save_to_file(articles, index)
        last_index = index + 1000

    # Get articles for any remaining categories
    articles = get_articles_for_categories(query, set(list(categories)[last_index:last_index + 1000]))
    save_to_file(articles, last_index)

    print(CATEGORIES_BUGS)
