import logging
import os

import pickle

import networkx as nx

from file_operations import save_pickle, load_pickle
from settings import GRAPH_IN_PROGRESS_FILENAME, RELATIONSHIP_MAP_FILENAME, GRAPH_GML_FILENAME
from tools.category_matcher import CategoryMatcher
from tools.relationship_extractor import RelationshipExtractor


class GraphCreator:

    def __init__(self, data_dir: str, category_matcher: CategoryMatcher):
        self.data_dir = data_dir
        self.in_progress_graph_filename = data_dir + '/' + GRAPH_IN_PROGRESS_FILENAME
        self.relationship_map_filename = data_dir + '/' + RELATIONSHIP_MAP_FILENAME
        self.graph_filename = data_dir + GRAPH_GML_FILENAME

        self.category_matcher = category_matcher
        self.graph = nx.DiGraph()
        self.relationship_map = self.load_relationship_map()

        self.load_in_progress_graph()

    def load_in_progress_graph(self):
        if os.path.isfile(self.in_progress_graph_filename):
            with open(self.in_progress_graph_filename, 'rb') as f:
                self.graph = pickle.load(f)

    def save_in_progress_graph(self):
        save_pickle(self.graph, self.in_progress_graph_filename)

    def load_relationship_map(self):
        return load_pickle(self.relationship_map_filename, is_dict=True)

    def save_relationship_map(self):
        save_pickle(self.relationship_map, self.relationship_map_filename)

    def load_article(self, filename):
        return pickle.load(open(self.data_dir + "/" + filename, 'rb'))

    def is_duplicate_article(self, article):
        return self.graph.has_node(article.title)

    def get_nodes_and_relationships(self, articles):
        """
        Extracts nodes from articles and adds them to the graph.
        Extracts the edges from articles and adds them to a separate dictionary as we might not have some of those nodes
        in our graph yet."""

        for article in articles:
            if self.category_matcher.is_article_relevant(article.title, article.content) \
                    and not self.is_duplicate_article(article):
                event_name = article.title

                self.graph.add_node(event_name, wikiid=article.pageid)

                relationship_extractor = RelationshipExtractor(article.content)
                relationships = relationship_extractor.get_relationships()
                self.relationship_map[event_name] = relationships

    def add_edges(self):
        """Adds edges from relationship map to the graph."""
        for source_node, references in self.relationship_map.items():
            for destination_node in references:
                if self.graph.has_node(destination_node) and not self.graph.has_edge(source_node, destination_node):
                    self.graph.add_edge(source_node, destination_node)

    def create_graph_from_articles(self, start=0, end=None):
        """
        Loads articles from files starting with 'articles_' prefix.
        :param start: Integer stating the index of file we should start creating a graph from. Defaults to 0.
        :param end: Integer or None stating the index of last file. Defaults to None.
        :return:
        """
        article_files = sorted(filter(lambda x: x.startswith('articles_'), os.listdir(self.data_dir)))

        for filename in article_files[start:end]:
            logging.info("*** Loading file: {}".format(filename))
            print("*** Loading file: {}".format(filename))

            article_batch = self.load_article(filename)
            self.get_nodes_and_relationships(article_batch)
            self.save_relationship_map()
            self.save_in_progress_graph()

        self.add_edges()

        nx.write_gml(self.graph, self.graph_filename)

