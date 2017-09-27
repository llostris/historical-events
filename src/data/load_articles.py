import os
import pickle

from sqlalchemy.orm import Session

from data.service import BaseService
from settings import DATA_DIR

# from articles import RawArticle
from model.wiki_model import Article, Category
from wiki_config import CATEGORY_REGEXP


def load_article_from_pickle(filename):
    article_batch = pickle.load(open(DATA_DIR + "/" + filename, 'rb'))
    return article_batch


def get_category_from_db(category_name, session):
    category = session.query(Category).filter_by(name = category_name).first()
    print(category)
    return category

def get_categories(content, session):
    categories = []

    for category_tag in CATEGORY_REGEXP.findall(content):
        category_name = category_tag[2:-2]
        category = get_category_from_db(category_name, session)
        if category is not None:
            categories.append(category)

    return categories


def convert_articles_to_model(article_batch, session):
    articles = []
    for raw_article in article_batch:
        categories = get_categories(raw_article.content.encode('utf-8'), session)
        article = Article(pageid = raw_article.pageid,
                          title = raw_article.title.encode('utf-8'),
                          content = raw_article.content.encode('utf-8'),
                          categories = categories)
        articles.append(article)
        # print article

    return articles


if __name__ == "__main__":

    base_service = BaseService(False)

    session = Session(bind = base_service.engine)

    session.query(Article).delete()
    session.commit()

    article_file_name_prefix = "articles.pickle"

    articles = []

    for elem in os.listdir(DATA_DIR) :
        if elem.startswith(article_file_name_prefix) :
            print(elem)
            article_batch = load_article_from_pickle(elem)
            article_models = convert_articles_to_model(article_batch, session)
            articles += article_models

    print(len(articles))
    print(articles[0], articles[1])
    session.add_all(articles)

    print(session.dirty)
    session.commit()