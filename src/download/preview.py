"""Allows previewing saved category/article data to see the data set size etc."""

import os

from download.articles import load_category_list
from graph.model.vertex_extractor import ARTICLE_FILE_NAME_PREFIX, load_article_from_pickle
from settings import DATA_DIR
from wiki_config import is_category_relevant
from articles import RawArticle

if __name__ == "__main__":

    # Categories data
    categories = load_category_list()
    print('All categories: {}'.format(len(categories)))
    unique_categories = set(filter(is_category_relevant, categories))
    print('Unique and relevant categories: {}'.format(len(unique_categories)))

    # Articles data

    articles = []

    for elem in os.listdir(DATA_DIR) :
        if elem.startswith(ARTICLE_FILE_NAME_PREFIX) :
            article_batch = load_article_from_pickle(elem)
            print(elem, len(article_batch))
            articles += article_batch

    print(len(articles))

    # for article in articles:
    #     if 'Second Battle of El Alamein' in article.title:
    #         print article.title #, article.content
