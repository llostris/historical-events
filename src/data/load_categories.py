from sqlalchemy.orm import Session

from data.model.wiki_model import Category
from data.service import BaseService
from settings import CATEGORIES_FILE


def load_category_map() :
    categories = {}

    with open(CATEGORIES_FILE, 'r') as f:
        for line in f.readlines():
            splitted = line.decode('utf-8').strip().split(",")
            categories[int(splitted[0])] = splitted[1]

    return categories


def convert_to_model(category_map):
    categories = []
    for category_id, name in category_map.items():
        category = Category(category_id=category_id, name=name.encode('utf-8'))
        categories.append(category)
    return categories


def load_categories(category_map):
    session = Session()

    categories = convert_to_model(category_map)
    # print categories
    print categories[0]

    session.query(Category).delete()
    session.commit()

    session.add_all(categories)
    session.commit()


if __name__ == "__main__":
    category_map = load_category_map()

    base_service = BaseService(True)

    load_categories(category_map)
