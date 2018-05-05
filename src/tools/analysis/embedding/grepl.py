"""Implementation of Node2Vec according to publication 'Graph Embeddings with Predicted Links' (GREPL)."""
import networkx as nx

from graphs.history.wiki_config import HISTORY_DATA_DIR
from settings import GRAPH_GML_FILENAME


class LinkPredictor:

    def __init__(self, graph, training_nodes):
        self.graph = graph
        self.training_nodes = training_nodes
        self.link_probability_matrix = [] # make np.array

    def build_matrix(self):
        pass


class GraphEmbeddingWithPredictedLinks:

    def __init__(self, graph):
        """
        :param graph: NetworkX graph
        """
        self.graph = graph

    def get_link_predictions(self):
        """Training dataset consists of equal numnber of positive (with links) and negative (without links) examples."""
        positive_training_examples, negative_training_examples = self._get_positive_and_negative_examples()

    def _get_common_neighbour_node_pairs(self):
        """
        Calculates pairs of nodes (i, j) that have at least one common neighbour.
        :return: list of tuples (i, j)
        """
        node_pairs = []
        for node1 in self.graph.node:
            for node2 in self.graph.node:
                if node1 != node2:
                    neighbour_count = nx.common_neighbors(self.graph, node1, node2)
                    if len(neighbour_count) >= 1:
                        node_pairs.append((node1, node2))
        return node_pairs

    def _get_positive_and_negative_examples(self):
        """
        Positive Examples: Nodes connected by an edge, that have at lest one common neighbour.
        Negative Examples: Nodes not connected by an edge, that have at lest one common neighbour.
        :param:node_pairs: list of tuples (i, j) representing nodes
        :returns: two lists of nodes
        """
        common_neighbour_node_pairs = self._get_common_neighbour_node_pairs()

        positive_examples = []
        negative_examples = []
        for node1, node2 in common_neighbour_node_pairs:
            if node1 in node2.neighbors():
                positive_examples = node2
            else:
                negative_examples = node2

        return positive_examples, negative_examples


if __name__ == "__main__":
    graph_filename = HISTORY_DATA_DIR + '/' + GRAPH_GML_FILENAME
    graph = nx.read_gml(graph_filename)

    grepl = GraphEmbeddingWithPredictedLinks(graph)
    grepl.get_link_predictions()


