"""Removes duplicates from category list and performs basic filtering of relevant categories"""

from settings import CATEGORIES_UNIQUE_FILENAME, CATEGORIES_RELEVANT_FILENAME, CATEGORIES_FILENAME
from tools.category_matcher import CategoryMatcher


class UniqueCategoryListGenerator:

    def __init__(self, category_matcher: CategoryMatcher, data_dir: str):
        self.category_matcher = category_matcher
        self.data_dir = data_dir

    def get_unique_categories(self):
        categories_all = self.load_category_list()

        unique = set(categories_all)
        print('Unique categories:', len(unique))

        filtered = list(filter(self.category_matcher.is_category_relevant, unique))

        self.save_to_file(unique, self.data_dir + '/' + CATEGORIES_UNIQUE_FILENAME)
        self.save_to_file(filtered, self.data_dir + '/' + CATEGORIES_RELEVANT_FILENAME)

    def load_category_list(self):
        categories = set()
        with open(self.data_dir + '/' + CATEGORIES_FILENAME, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                splitted = line.strip().split(",")
                categories.add(splitted[1])

        return categories

    def save_to_file(self, categories, file, append=False):
        mode = 'w'
        if append:
            mode = 'a'

        with open(file, mode, encoding='utf-8') as f:
            for title in categories:
                f.write(title + '\n')
            f.close()
#
#
# if __name__ == "__main__":
#     categories_all = load_category_list()
#
#     unique = set(categories_all)
#     print('Unique categories:', len(unique))
#
#     filtered = list(filter(is_category_relevant, unique))
#
#     save_to_file(unique, DATA_DIR + '/categories_unique.csv')
#     save_to_file(filtered, DATA_DIR + '/categories_relevant.csv')
#
#     print(unique.pop())
