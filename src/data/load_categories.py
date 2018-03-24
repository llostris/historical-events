from sqlalchemy.orm import Session

from data.model.graph_model import Category
from graphs.history.service import BaseService
from settings import CATEGORIES_FILE
from tools.article_scraper import load_category_list


def load_category_map():
    categories = {}

    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            splitted = line.strip().split(",")
            id = int(splitted[0])
            name = splitted[1]
            categories[id] = name

    return categories


def convert_to_model(category_map):
    categories = []
    for category_id, name in category_map.items():
        category = Category(wiki_id=category_id, name=name)
        categories.append(category)
    return categories


def convert_list_to_model(categories):
    models = []
    for name in categories:
        category = Category(name=name)
        models.append(category)
    return models


def load_categories(category_names):
    session = Session()

    categories = convert_list_to_model(category_names)

    session.query(Category).delete()
    session.commit()

    session.add_all(categories)
    session.commit()


if __name__ == "__main__":
    categories_all = load_category_list()
    unique = set(categories_all)
    filtered = list(filter(is_category_relevant, unique))

    models = convert_list_to_model(filtered)

    base_service = BaseService(True)
    load_categories(filtered)
