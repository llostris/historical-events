# -*- coding: utf-8 -*-
from settings import ARTICLE_LOG_FILE
from io import open

CATEOGRY_PREFIX = "Category:"

if __name__ == "__main__":

    invalid_categories = []

    with open(ARTICLE_LOG_FILE, 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            if CATEOGRY_PREFIX in line:
                line = line.strip()
                index = line.index(CATEOGRY_PREFIX)
                category = line[index:]
                print(category)
                invalid_categories.append(category)

    print(len(invalid_categories))
