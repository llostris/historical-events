# coding=utf-8
import pickle
import re
import signal

from settings import DATA_DIR, CATEGORIES_FILE
from wiki_api_utils import run_query
from wiki_config import CATEGORYMEMBERS, NAMESPACES, is_category_relevant, CATEGORY_KEYWORDS

DATE_YEAR_IN_REGEXP = re.compile(r"(\d+ .* in)|(in \d+)")

VISITED_IDS = {}

def signal_handler():
    with open(DATA_DIR + '/cat_visited_ids.pickle', 'wb') as f:
        pickle.dump(VISITED_IDS, f)
        f.close()

def is_category_history_related(category_name) :
    category_name = category_name.lower()

    if is_category_relevant(title):

        for keyword in CATEGORY_KEYWORDS :
            if keyword in category_name :
                return True

        if DATE_YEAR_IN_REGEXP.match(category_name) :
            return True

    return False


def save_to_file(categories, append=False) :
    mode = 'w'
    if append:
        mode = 'a'

    with open(CATEGORIES_FILE, mode) as f :
        for id, title in categories.items() :
            f.write(str(id) + "," + title.encode('utf-8') + '\n')
        f.close()


def get_categories(query, visited_ids, end = False) :
    query["cmtitle"] = unicode(query["cmtitle"]).encode('utf-8')
    result = run_query(query)
    print 'json:', result

    categories = { }
    found_categories = result["query"][CATEGORYMEMBERS]
    print 'resuls found: %d' % len(found_categories)
    for member in found_categories :
        pageid = member["pageid"]
        title = member["title"]
        namespace = member["ns"]

        if namespace == NAMESPACES["category"] and is_category_history_related(title) :
            categories[pageid] = title
            print 'category ' + title

    # if end:
    #     print 'end'
    #     return categories

    subcategories = { }
    print 'recurse'
    for id in categories :
        if id not in visited_ids :
            print id
            query["cmtitle"] = categories[id]
            visited_ids.add(id)

            subcategories_new = get_categories(query, visited_ids, True)
            subcategories.update(subcategories_new)
            print len(visited_ids)

    save_to_file(subcategories, True)

    categories.update(subcategories)

    return categories


def load_visited_ids():
    visited_ids = {}
    with open(DATA_DIR + 'cat_visited_ids.pickle', 'rb') as f:
        visited_ids = pickle.load(f)

    return visited_ids


if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal_handler)

    title = "Category:History"
    # title = u"Category:Trần Quang Khải-class frigates"
    query = {
        "action" : "query",
        "list" : "categorymembers",
        "cmtitle" : title,
        "cmlimit" : "max",
        "format" : "json",
        "cmnamespace" : NAMESPACES["category"],
        "cmtype" : "subcat", # didn't use it but should be better (less unnecessary info)
        "formatversion" : 2
    }

    visited_ids = load_visited_ids()
    VISITED_IDS = visited_ids
    categories = { }
    portals = { }

    categories = get_categories(query, visited_ids, True)

    save_to_file(categories)
