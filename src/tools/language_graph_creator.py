import networkx as nx

from file_operations import load_pickle, save_pickle
from settings import GRAPH_GML_FILENAME, LANGUAGE_MAP_FILENAME, GRAPH_LANGUAGE_GML_FILENAME


class LanguageGraphCreator:

    def __init__(self, data_dir: str, language: str):
        self.data_dir = data_dir
        self.graph = nx.read_gml(self.data_dir + '/' + GRAPH_GML_FILENAME)
        self.language_map = load_pickle(self.data_dir + '/' + LANGUAGE_MAP_FILENAME)
        self.language = language

    def _filter_out_language_nodes(self):
        filtered = filter(lambda x: self.language in self.language_map[x]['languages'], self.language_map)
        return set(filtered)

    def create_language_restricted_graph(self):
        matching_nodes = self._filter_out_language_nodes()
        nodes_to_remove = []

        for node in self.graph.nodes():
            if node not in matching_nodes:
                nodes_to_remove.append(node)

        self.graph.remove_nodes_from(nodes_to_remove)

        nx.write_gml(self.graph, self.data_dir + '/' + GRAPH_LANGUAGE_GML_FILENAME.format(self.language))
        save_pickle(self.graph, self.data_dir + '/' + GRAPH_LANGUAGE_GML_FILENAME.format(self.language) + '.pickle')

        print("Number of nodes:", self.graph.number_of_nodes())
        print("Number of edges:", self.graph.number_of_edges())
