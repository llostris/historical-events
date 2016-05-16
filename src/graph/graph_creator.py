import os

import networkx as nx
from graph.date_extractor import DateExtractor

from graph.dataextraction.relationship_extractor import RelationshipExtractor
from graph.model.vertex_extractor import ARTICLE_FILE_NAME_PREFIX, load_article_from_pickle
from settings import DATA_DIR, GRAPH_GML_FILE, get_graph_logger
from wiki_config import is_title_relevant, CATEGORY_REGEXP, is_category_relevant

logger = get_graph_logger()

def is_article_relevant(title, content):
    categories = CATEGORY_REGEXP.findall(content)
    for category in categories:
        if not is_category_relevant(category):
            return False

    return is_title_relevant(title)


def create_graph(articles):
    graph = nx.DiGraph()
    relationship_map = {} # temporary to keep edges

    # extract vertices
    for article in articles:
        if is_article_relevant(article.title, article.content):
            event_name = article.title

            date_extractor = DateExtractor(article.title, article.content)
            date_extractor.fill_dates()

            relationship_extractor = RelationshipExtractor(article.content)
            relationships = relationship_extractor.get_relationships()

            attributes = {
                'date' : date_extractor.date,
                'start_date' : date_extractor.start_date,
                'end_date' : date_extractor.end_date
            }
            graph.add_node(event_name, attr_dict = attributes)

            relationship_map[event_name] = relationships

    # extract edges
    for source_node, references in relationship_map.items():
        for destination_node in references:
            if graph.has_node(destination_node) and not graph.has_edge(source_node, destination_node):
                graph.add_edge(source_node, destination_node)

    return graph

def save_graph(graph):
    nx.write_gml(graph, GRAPH_GML_FILE)

if __name__ == "__main__":

    articles = []

    for elem in os.listdir(DATA_DIR) :
        if elem.startswith(ARTICLE_FILE_NAME_PREFIX) :
            print elem
            article_batch = load_article_from_pickle(elem)
            articles += article_batch

    print len(articles)

    # graph = create_graph(articles[27987:28000]) # first - 10,000 metres world reord
    # graph = create_graph(articles[29293:30000]) # 5th-century-562
    graph = create_graph(articles)
    # graph = create_graph(articles[33654:35000])
    save_graph(graph)

    print(graph.number_of_nodes())
    print(graph.number_of_edges())
