import pickle

from categories import VISITED_IDS
from safestring import safe_str, safe_unicode
from settings import CATEGORIES_FILE, ARTICLE_LOG_FILE, ARTICLES_FILE, DATA_DIR
from wiki_api_utils import run_query
from wiki_config import NAMESPACES, TAG_QUERY, CATEGORYMEMBERS, TAG_PAGES, FORBIDDEN_TITLE_KEYWORDS, \
    FORBIDDEN_CATEGORY_KEYWORDS, is_category_relevant


import logging

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


def load_category_list() :
    categories = set()

    with open(CATEGORIES_FILE, 'r') as f:
        for line in f.readlines():
            splitted = line.strip().split(",")
            categories.add(safe_unicode(splitted[1]))

    return categories


def is_matching_article_title(title, content):
    for forbidden_word in FORBIDDEN_TITLE_KEYWORDS:
        if forbidden_word in title.lower():
            return False

    for forbidden_word in FORBIDDEN_CATEGORY_KEYWORDS:
        if forbidden_word in content.lower():
            return False
    return True


def is_response_valid(query, result):
    if not "query" in result:
        CATEGORIES_BUGS.append(query["gcmtitle"])
        logging.warn("Invalid category: " + query["gcmtitle"])
        if "warnings" in result:
            try:
                logging.warn(query["gcmtitle"] + " returned no results: " + result["warnings"]["main"])
            except (TypeError, KeyError) as e:
                logging.error("Error while logging: {0} ".format(e))

        return False

    return True


def get_articles(query, visited_ids, categories) :
    print query["gcmtitle"]
    result = run_query(query)
    print 'json:', result

    if not is_response_valid(query, result):
        return []

    found_articles = result[TAG_QUERY][TAG_PAGES]

    if len(found_articles) > 450:
        logging.warn(query["gcmtitle"] + " might need a continuation query " + str(len(found_articles)))

    all_articles = []
    for article in found_articles:
        pageid = article["pageid"]
        title = article["title"]
        namespace = article["ns"]
        content = article["revisions"][0]["content"]

        print article

        if namespace == NAMESPACES["article"] and is_matching_article_title(title, content):
            all_articles.append(RawArticle(pageid, safe_str(title), safe_str(content)))
            visited_ids.add(pageid)

    return all_articles


def get_articles_for_categories(query, categories):
    articles = []
    visited_ids = set()

    for category in categories:
        query["gcmtitle"] = category
        articles += get_articles(query, visited_ids, categories)

    return articles


def save_to_file(articles, index):
    with open(ARTICLES_FILE + '_' + str(index), 'wb') as f :
        pickle.dump(articles, f)

if __name__ == "__main__" :
    title = "Category:History"
    title = "Category:1918 in military history"
    query = {
        "action" : "query",
        "generator" : "categorymembers",
        "cmlimit" : "max",
        "format" : "json",
        "gcmtitle" : title,
        "prop" : "revisions",
        "rvprop" : "content",
        "cmnamespace" : NAMESPACES["article"],
        "formatversion" : 2
    }

    categories = load_category_list()
    categories = set(filter(is_category_relevant, categories))
    # print categories
    articles = { }

    num_categories = len(categories)
    start = 18000
    last_index = start

    for index in range(start, num_categories, 1000):
        articles = get_articles_for_categories(query, set(list(categories)[index:index + 1000]))
        print articles[0]

        save_to_file(articles, index)
        last_index = index + 1000

    articles  = get_articles_for_categories(query, set(list(categories)[last_index:last_index + 1000]))
    save_to_file(articles, last_index)

    print(CATEGORIES_BUGS)
