"""Implementation of Node2Vec according to publication 'Graph Embeddings with Predicted Links' (GREPL)."""
import networkx as nx
import pandas as pd

from graphs.history.wiki_config import HISTORY_DATA_DIR
from settings import GRAPH_GML_FILENAME


class LinkPredictor:

    def __init__(self, graph, training_nodes):
        self.graph = graph.to_undirected()  # This algorithm doesn't work for directed graphs?
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
        # positive_training_examples, negative_training_examples = self._get_positive_and_negative_examples()

        common_neighbour_node_pairs = self._get_common_neighbour_node_pairs()
        df = pd.DataFrame(columns=['adjusted_degree1', 'adjusted_degree2', 'common_neighbours', 'adamic_adar_score'])
        for node1, node2 in common_neighbour_node_pairs:
            a_ij = 1 if node1 in self.graph.neighbors(node2) else 0   # value of adjacency matrix for (node1, node2)
            df.append({
                'adjusted_degree1': self.graph.degree(node1) - a_ij,
                'adjusted_degree2': self.graph.degree(node2) - a_ij,
                'common_neighbours': len(list(nx.common_neighbors(self.graph, node1, node2))),  # FIXME: Don't calcualte this twice~
                'adamic_adar_score': 0  # TODO: calculate
            }, ignore_index=True)

        positive_examples, negative_examples = self._get_positive_and_negative_examples(common_neighbour_node_pairs)


        # Train RF classifier
        # think how?

        # Cross-validation accuracy ofm

    def _get_common_neighbour_node_pairs(self):
        """
        Calculates pairs of nodes (i, j) that have at least one common neighbour.
        :return: list of tuples (i, j)
        """
        node_pairs = []
        for node1 in self.graph.nodes():
            for node2 in self.graph.nodes():
                if node1 != node2:
                    neighbour_count = list(nx.common_neighbors(self.graph, node1, node2))
                    if len(neighbour_count) >= 1:
                        node_pairs.append((node1, node2))
        return node_pairs

    def _get_positive_and_negative_examples(self, node_pairs):
        """
        Positive Examples: Nodes connected by an edge, that have at lest one common neighbour.
        Negative Examples: Nodes not connected by an edge, that have at lest one common neighbour.
        :param:node_pairs: list of tuples (i, j) representing nodes
        :returns: two lists of nodes
        """

        positive_examples = set()
        negative_examples = set()
        for node1, node2 in node_pairs:
            if node1 in self.graph.neighbors(node2):
                positive_examples.add((node1, node2))
            else:
                negative_examples.add((node1, node2))

        return positive_examples, negative_examples

    def _get_positive_and_negative_examples_article_version(self, common_neighbour_node_pairs):
        # For comparison purposes
        positive_examples = set()
        negative_examples = set()
        for node in self.graph.node:
            neighbours_with_common_neighbours = [j for j in self.graph.nodes()
                                                 if (node, j) in common_neighbour_node_pairs]

            positive_i = {j for j in neighbours_with_common_neighbours if j in self.graph.neighbors(node)}
            negative_i = {j for j in neighbours_with_common_neighbours if j not in self.graph.neighbors(node)}
            print(positive_i, negative_i)
            positive_examples |= {(node, j) for j in positive_i}
            negative_examples |= {(node, j) for j in negative_i}

        return positive_examples, negative_examples


if __name__ == "__main__":
    # graph_filename = HISTORY_DATA_DIR + '/' + GRAPH_GML_FILENAME
    # graph = nx.read_gml(graph_filename)
    graph = nx.circular_ladder_graph(5)
    print('Graph loaded')

    grepl = GraphEmbeddingWithPredictedLinks(graph)
    grepl.get_link_predictions()


