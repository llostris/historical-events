"""Removes duplicates from category list and performs basic filtering of relevant categories"""

from download.articles import load_category_list
from settings import DATA_DIR
from wiki_config import is_category_relevant


def save_to_file(categories, file, append=False) :
    mode = 'w'
    if append:
        mode = 'a'

    with open(file, mode) as f :
        for title in categories :
            f.write(title.encode('utf-8') + '\n')
        f.close()


if __name__ == "__main__":
    categories_all = load_category_list()

    unique = set(categories_all)
    print 'Unique categories:', len(unique)

    filtered = filter(is_category_relevant, unique)
    print 'Relevant categories:', len(filtered)

    save_to_file(unique, DATA_DIR + '/categories_unique.csv')
    save_to_file(filtered, DATA_DIR + '/categories_relevant.csv')

    print unique.pop()

