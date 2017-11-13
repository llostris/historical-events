# -*- coding: utf-8 -*-
import os
import pickle

import networkx as nx
from sqlalchemy.orm import Session

from base_wiki_config import is_article_relevant
from data.model.graph_model import Event, UncertainDate, Article
from data.service import BaseService
from file_operations import load_pickle, save_pickle
from graph.dataextraction.date_extractor import DateExtractor
from graph.dataextraction.relationship_extractor import RelationshipExtractor
from graph.model.vertex_extractor import ARTICLE_FILE_NAME_PREFIX, load_article_from_pickle
from settings import DATA_DIR, GRAPH_GML_FILE, get_graph_logger, RELATIONSHIP_MAP_FILE, GRAPH_IN_PROGRESS_FILE
from download.articles import RawArticle

logger = get_graph_logger()
# parse_error_logger = get_parse_error_logger()


def get_nodes_and_relationships(articles, graph, relationship_map, session=None):
    if graph is None:
        graph = nx.DiGraph()
    if relationship_map is None:
        relationship_map = {}   # temporary to keep edges

    # extract vertices
    for article in articles:
        if is_article_relevant(article.title, article.content) and not is_duplicate_event(article, graph, session):
            event_name = article.title

            graph.add_node(event_name, wikiid=article.pageid)
            if session:
                date_extractor = DateExtractor(article.title, article.content)
                date_extractor.fill_dates()

                for date in [date_extractor.date, date_extractor.start_date, date_extractor.end_date]:
                    if not is_valid_date(date):
                        logger.error('Invalid date parsed for title: {} {}'.format(article.title, date))

                date_extractor.validate_dates()  # remove invalid dates

                attributes = {
                    'start_date': date_extractor.start_date,
                    'end_date': date_extractor.end_date,
                    'date': date_extractor.date
                }
                save_event_in_db(event_name, attributes, article.pageid, article.content, session)

            relationship_extractor = RelationshipExtractor(article.content)
            relationships = relationship_extractor.get_relationships()

            relationship_map[event_name] = relationships

    return graph, relationship_map


def is_duplicate_event(article, graph, session):
    if session:
        existing_event = session.query(Event).filter(Event.wiki_id == article.pageid).first()
        if existing_event is not None:
            return True

        return False
    else:
        return graph.has_node(article.title)


def save_event_in_db(name, attributes, page_id, article_content, session):
    event = Event(name=name, wiki_id=page_id)

    start_date = save_date_in_db(attributes['start_date'], session)
    if start_date is not None:
        event.start_date_id = start_date.id

    end_date = save_date_in_db(attributes['end_date'], session)
    if end_date is not None:
        event.end_date_id = end_date.id

    date = save_date_in_db(attributes['date'], session)
    if date is not None:
        event.date_id = date.id

    session.add(event)
    session.commit()

    article = Article(content=article_content, event_id=event.id)
    session.add(article)
    try:
        session.commit()
    except Exception as e:
        logger.error(e)
        logger.error("Could not save article {} content: {}".format(name, article_content))
        session.rollback()


def save_date_in_db(flexi_date, session):
    if flexi_date is None:
        return None
    if DateExtractor.is_unparsed(flexi_date):
        return None

    year = get_int_from_value(flexi_date.year)
    month = get_int_from_value(flexi_date.month)
    day = get_int_from_value(flexi_date.day)
    is_bc = year < 0 if year is not None else False
    circa = 'circa' in flexi_date.qualifier

    date = UncertainDate(year=year, month=month, day=day, is_bc=is_bc, is_circa=circa)
    session.add(date)
    session.commit()
    return date


def get_int_from_value(value):
    if isinstance(value, str) and value != '':
        try:
            return int(value)
        except ValueError as e:
            logger.error(e)
            return None
    else:
        return None


def create_graph(graph, relationship_map):

    # extract edges
    for source_node, references in relationship_map.items():
        for destination_node in references:
            if graph.has_node(destination_node) and not graph.has_edge(source_node, destination_node):
                graph.add_edge(source_node, destination_node)

    return graph


def is_valid_date(date):
    return 'UNPARSED' not in str(date)


def save_graph(graph):
    nx.write_gml(graph, GRAPH_GML_FILE)


def dump_graph(graph):
    pass


# <editor-fold desc="Serialization of relationship map">

def load_relationship_map(filename=RELATIONSHIP_MAP_FILE):
    return load_pickle(filename)


def save_relationship_map(relationship_map, filename=RELATIONSHIP_MAP_FILE):
    save_pickle(relationship_map, filename)


def update_relatioship_map(new_relashionship_map):
    relationship_map = load_relationship_map()

    relationship_map.update(new_relashionship_map)

    save_relationship_map(relationship_map)

# </editor-fold>


# <editor-fold desc="Serialization of in-progress graph">

def load_in_progress_graph(filename=GRAPH_IN_PROGRESS_FILE):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return nx.DiGraph()


def save_in_progress_graph(in_progress_graph):
    with open(GRAPH_IN_PROGRESS_FILE, 'wb') as f:
        pickle.dump(in_progress_graph, f)

# </editor-fold>


if __name__ == "__main__":
    # base_service = BaseService(True)
    # session = Session()

    graph = load_in_progress_graph()
    relationship_map = load_relationship_map()

    article_files = sorted(filter(lambda x: x.startswith(ARTICLE_FILE_NAME_PREFIX), os.listdir(DATA_DIR)))

    # 0:35 - done
    # remaining [13:]

    for elem in article_files[30:]:
        logger.info("*** Loading file: {}".format(elem))
        print(elem)

        article_batch = load_article_from_pickle(elem)

        # graph, relationship_map = get_nodes_and_relationships(article_batch, graph, {}, session) # this will populate sql database and parse dates
        graph, relationship_map = get_nodes_and_relationships(article_batch, graph, relationship_map, None)
        update_relatioship_map(relationship_map)
        save_in_progress_graph(graph)

    graph = create_graph(graph, relationship_map)

    # for node in graph.nodes:
    #     attributes = graph.node[node]['attributes']
    #     wiki_id = attributes['wiki_id']
    #     del graph.nodes[node]['attributes']
    #     graph.nodes[node]['wikiid'] = wiki_id

    save_graph(graph)
