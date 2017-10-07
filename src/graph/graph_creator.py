# -*- coding: utf-8 -*-
import os
import pickle

import networkx as nx

from graph.dataextraction.date_extractor import DateExtractor
from graph.dataextraction.relationship_extractor import RelationshipExtractor
from graph.model.vertex_extractor import ARTICLE_FILE_NAME_PREFIX, load_article_from_pickle
from settings import DATA_DIR, GRAPH_GML_FILE, get_graph_logger, RELATIONSHIP_MAP_FILE, GRAPH_IN_PROGRESS_FILE
from wiki_config import is_article_relevant
from download.articles import RawArticle

logger = get_graph_logger()


def get_nodes_and_relationships(articles, graph, relationship_map):
    if graph is None:
        graph = nx.DiGraph()
    if relationship_map is None:
        relationship_map = {}   # temporary to keep edges

    # extract vertices
    for article in articles:
        if is_article_relevant(article.title, article.content):
            event_name = article.title

            date_extractor = DateExtractor(article.title, article.content)
            date_extractor.fill_dates()

            for date in [date_extractor.date, date_extractor.start_date, date_extractor.end_date]:
                if not is_valid_date(date):
                    logger.error('Invalid date parsed for title: {} {}'.format(article.title, date))

            date_extractor.validate_dates()  # remove invalid dates

            attributes = date_extractor.get_iso_dates()
            graph.add_node(event_name, attr_dict=attributes)

            relationship_extractor = RelationshipExtractor(article.content)
            relationships = relationship_extractor.get_relationships()

            relationship_map[event_name] = relationships

    return graph, relationship_map


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
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


def save_relationship_map(relationship_map, filename=RELATIONSHIP_MAP_FILE):
    with open(filename, 'wb') as f:
        pickle.dump(relationship_map, f)


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

    graph = load_in_progress_graph()
    relationship_map = {}

    article_files = sorted(filter(lambda x: x.startswith(ARTICLE_FILE_NAME_PREFIX), os.listdir(DATA_DIR)))

    for elem in article_files[6:8]:
        logger.info("*** Loading file: {}".format(elem))
        print(elem)

        article_batch = load_article_from_pickle(elem)

        graph, relationship_map = get_nodes_and_relationships(article_batch, graph, {})
        update_relatioship_map(relationship_map)
        save_in_progress_graph(graph)

    # print len(articles)

    # graph = create_graph(articles[27987:28000]) # first - 10,000 metres world reord
    # graph = create_graph(articles[29293:30000]) # 5th-century-562
    # graph = create_graph(articles)
    # graph = get_nodes_and_relationships(articles)

    # graph = create_graph(graph, load_relationship_map())
    # save_graph(graph)
    # print(graph.number_of_nodes())
    # print(graph.number_of_edges())
