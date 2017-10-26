# -*- coding: utf-8 -*-
import os
import pickle

# from data.load_articles import load_article_from_pickle, convert_articles_to_model
# import pandas as pd

from download.articles import RawArticle as Article
# from data.load_articles import convert_articles_to_model
from graph.dataextraction.date_extractor import DateExtractor
from settings import DATA_DIR

from base_wiki_config import is_title_relevant

ARTICLE_FILE_NAME_PREFIX = "articles.pickle"


class RawEvent:

    def __init__(self, name, pageid):
        self.pageid = pageid
        self.name = name
        self.start_date = None
        self.end_date = None
        self.date = None
        self.exact_start_date = False
        self.exact_end_date = False
        self.exact_date = False
        self.date_type = 'date'
        pass

    def __repr__(self):
        return "<Event(name='{0}')>".format(self.name)


def load_article_from_pickle(filename):
    return pickle.load(open(DATA_DIR + "/" + filename, 'rb'))


def extract_event(article):
    print(article.title)
    event = RawEvent(article.title, article.pageid)
    # print(article.content)
    date_extractor = DateExtractor(article.title, article.content)
    date_extractor.fill_dates()
    event.date, event.start_date, event.end_date = date_extractor.date, date_extractor.start_date, date_extractor.end_date
    return event


def convert_articles_to_model_no_categories(article_batch):
    articles = []
    for raw_article in article_batch:
        if is_title_relevant(raw_article.title):
            article = Article(pageid=raw_article.pageid,
                              title=raw_article.title,
                              content=raw_article.content)
            articles.append(article)
        # print article

    return articles


if __name__ == "__main__":

    articles = []

    for elem in os.listdir(DATA_DIR):
        if elem.startswith(ARTICLE_FILE_NAME_PREFIX):
            print(elem)
            article_batch = load_article_from_pickle(elem)
            article_models = convert_articles_to_model_no_categories(article_batch)
            articles += article_models

    print(len(articles))

    events = []
    # for article in articles[1500:2500]:
    for article in articles[3000:4000]:
    # for article in articles[:30]:
        if is_title_relevant(article.title):
            event = extract_event(article)
            events.append(event)

    print(len(events))

    with open(DATA_DIR + 'events.pickle', 'wb') as f:
        pickle.dump(events, f)
        f.close()
