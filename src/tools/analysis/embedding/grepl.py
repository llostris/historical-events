"""Implementation of Node2Vec according to publication 'Graph Embeddings with Predicted Links' (GREPL)."""
import random

import networkx as nx
import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


class LinkPredictor:

    def __init__(self, graph, nodes=list(), training_split=0.1):
        """

        :param graph: Graph in NetworkX format.
        :param nodes: List of nodes on which we're going to train our LinkPredictor.
        """
        self.graph = graph.to_undirected()  # This algorithm doesn't work for directed graphs?
        self.neighbour_counts = {}
        self._fill_neighbour_counts()

        self.common_neighbours_node_pairs = self._get_common_neighbour_node_pairs()
        self.nodes = nodes
        self.number_of_nodes = len(self.graph.nodes())
        self.rf_classifier = None
        self.cv_score = 0.0
        self.link_probability_matrix = None # A sparse matrix

    def _fill_neighbour_counts(self):
        for node1 in self.graph.nodes():
            for node2 in self.graph.nodes():
                if node1 != node2:
                    count = len(list(nx.common_neighbors(self.graph, node1, node2)))
                    self.neighbour_counts[(node1, node2)] = count


    def _get_common_neighbour_node_pairs(self):
        """
        Calculates pairs of nodes (i, j) that have at least one common neighbour.
        :return: list of tuples (i, j)
        """
        node_pairs = []
        for node1 in self.graph.nodes():
            for node2 in self.graph.nodes():
                if node1 != node2:
                    neighbour_count = self.neighbour_counts[(node1, node2)]
                    if neighbour_count >= 1:
                        node_pairs.append((node1, node2))
        return node_pairs

    def _get_positive_and_negative_examples(self):
        """
        Positive Examples: Nodes connected by an edge, that have at lest one common neighbour.
        Negative Examples: Nodes not connected by an edge, that have at lest one common neighbour.
        :param:common_neighbour_node_pairs: list of tuples (i, j) representing node
        :returns: two lists of tuples (i, j) representing nodes
        """
        positive_examples = set()
        negative_examples = set()
        for node in self.graph.node:
            neighbours_with_common_neighbours = [j for j in self.graph.nodes()
                                                 if (node, j) in self.common_neighbours_node_pairs]

            positive_i = {j for j in neighbours_with_common_neighbours if j in self.graph.neighbors(node)}

            nodes_without_edges = {j for j in neighbours_with_common_neighbours if j not in self.graph.neighbors(node)}
            sample_size = min(len(positive_i), len(nodes_without_edges))
            negative_i = random.sample(nodes_without_edges, sample_size)

            positive_examples |= {(node, j) for j in positive_i}
            negative_examples |= {(node, j) for j in negative_i}

        return positive_examples, negative_examples

    def _get_test_examples(self):
        test_examples = set()
        for node1, node2 in self.common_neighbours_node_pairs:
                if node1 not in self.graph.neighbors(node2):
                    test_examples.add((node1, node2))
        return test_examples

    def _build_data_frame(self):
        df = pd.DataFrame(columns=['nodes', 'adjusted_degree1', 'adjusted_degree2', 'common_neighbours',
                                   'adamic_adar_score'])

        for node1, node2 in self.common_neighbours_node_pairs:
            has_edge = 1 if node1 in self.graph.neighbors(node2) else 0

            # Returned result is an one-element list of (node1, node2, score)
            adamic_adar_score_result = list(nx.adamic_adar_index(self.graph, [(node1, node2)]))
            adamic_adar_score = adamic_adar_score_result[0][2]

            df = df.append({
                'nodes': (node1, node2),
                'adjusted_degree1': self.graph.degree(node1) - has_edge,
                'adjusted_degree2': self.graph.degree(node2) - has_edge,
                'common_neighbours': self.neighbour_counts[(node1, node2)],
                'adamic_adar_score': adamic_adar_score,
                'edge': has_edge
            }, ignore_index=True)

        df = df.set_index('nodes')

        return df

    def _get_X_and_y(self, df):
        X = df.drop('edge', axis=1)
        y = df['edge']
        return X, y

    def _train_model(self, df):
        positive_examples, negative_examples = self._get_positive_and_negative_examples()

        # Take only rows that are in our positive or negative examples
        training_df = df[df.index.isin(positive_examples | negative_examples)]
        train_X, train_y = self._get_X_and_y(training_df)

        # print(positive_examples, negative_examples)
        # print(len(self.graph.edges()))
        # print(len(positive_examples | negative_examples))
        # print('DataFrame before filtering', df.shape)
        # print('DataFrame after filtering', training_df.shape)

        # Train RF Classifier
        self.rf_classifier = RandomForestClassifier() # FIXME: should it be classifier?
        self.rf_classifier.fit(train_X, train_y)

        cv_scores = cross_val_score(self.rf_classifier, train_X, train_y, scoring='accuracy')
        self.cv_score = cv_scores.mean()
        print(cv_scores, self.cv_score)

    def _get_predictions(self, df):
        test_examples = self._get_test_examples()

        test_df = df[df.index.isin(test_examples)]
        test_X, _ = self._get_X_and_y(test_df)

        predictions = self.rf_classifier.predict(test_X)

        smoothed_predictions = self.cv_score * predictions + (1 - self.cv_score) * (1 - predictions)

        return test_df, smoothed_predictions

    def _convert_to_matrix(self, predictions_dict: dict):
        matrix = sp.dok_matrix((self.number_of_nodes, self.number_of_nodes), dtype=np.float)

        for (i, j), probability in predictions_dict.items():
            matrix[i, j] = probability

        matrix = matrix.transpose().tocsr()
        return matrix

    def build_predictions_matrix(self):
        """Training dataset consists of equal numnber of positive (with links) and negative (without links) examples."""
        df = self._build_data_frame()

        self._train_model(df)

        test_df, smoothed_predictions = self._get_predictions(df)

        predictions_dict = {}
        for (row_index, row), prediction in zip(test_df.iterrows(), smoothed_predictions):
            predictions_dict[row_index] = prediction

        self.link_probability_matrix = self._convert_to_matrix(predictions_dict)
        print(predictions_dict)
        # print(self.link_probability_matrix.shape)
        # print(self.link_probability_matrix)


class GraphEmbeddingWithPredictedLinks:

    def __init__(self, graph, omega=0.01, alpha=0.02, iterations=100, dimensions=2, training_split=0.1, batch_size=50):
        """

        :param graph: A NetworkX graph.
        :param omega: Weight assigned to probability predictions.
        :param alpha: Regularization parameter.
        :param iterations:
        :param dimensions: Number of dimensions in calculated embedding.
        :param training_split: Fraction of labelled data as training set. Should be fairly small. (10%, 20%, 30%)
        """
        self.graph = graph
        self.num_nodes = len(self.graph.nodes())
        self.iterations = iterations
        self.omega = omega
        self.alpha = alpha
        self.dimensions = dimensions
        self.training_split = training_split
        self.batch_size = batch_size

        # Matrices composing graph embedding: represent nodes and context embedding
        self.u = np.zeros(shape=[self.dimensions, self.num_nodes])
        self.v = np.zeros(shape=[self.num_nodes, self.dimensions])

        # self.m = np.zeros(shape=[self.num_nodes, self.dimensions])
        self.m = None

        # TODO: add trainig/test data size split when using LinkPredictor

    def calculate_l(self, i, j):
        return (self.m[i, j] - self.u.T[i] * self.v[j]) ** 2 \
                    + self.alpha * (np.linalg.norm(self.u) ** 2 + np.linalg.norm(self.v) ** 2)

    def calculate_l_matrix(self):
        l_matrix = np.zeros(shape=self.u.shape)

        for i in range(self.u.shape[0]):
            for j in range(self.u.shape[1]):
                l_ij = self.calculate_l(i, j)
                expected_value = np.mean([self.calculate_l(i, k) for k in range(self.u.shape[1]) if self.m[i, k] == 0])

                l_matrix[i][j] = l_ij[0] - expected_value

        return l_matrix

    def loss_function(self):
        l_matrix = self.calculate_l_matrix()

        # Sum of an element-wise multiplication of M and L matrices
        loss = np.sum(np.multiply(self.m, l_matrix))
        # FIXME: if that doesn't work try np.matrix.sum()

        # loss = 0
        # for i in range(self.u.shape[0]):
        #     for j in range(self.u.shape[1]):
        #         loss += self.m[i][j] * l_matrix[i][j]

        return loss

    def _get_matrix_m(self):
        link_predictor = LinkPredictor(self.graph)
        link_predictor.build_predictions_matrix()

        self.m = nx.to_scipy_sparse_matrix(self.graph) + self.omega * link_predictor.link_probability_matrix # TODO: add adjacency matrix of graph!!!

    def create(self):
        nodes = []
        edges = []

        self._get_matrix_m()
        # TODO: Random init of U, V

        for iteration in range(self.iterations):
            matrix_b = set()
            for i in range(self.num_nodes):
                n = int(self.batch_size * (np.sum(self.m[i]) / np.sum(self.m)))

                # pos_i = n draws with replacement from {j | Mij > 0} with uniform probabilities
                pos_set = [j for j in range(self.num_nodes) if self.m[i, j] > 0]
                pos_i = {random.choice(pos_set) for _ in range(n)}

                # neg_i = n draws with replacement from {j | Mij = 0} with uniform probabilities
                neg_set = [j for j in range(self.num_nodes) if self.m[i, j] == 0]
                neg_i = {random.choice(neg_set) for _ in range(n)}

                # B = B u {pos_i, neg_i}
                matrix_b = matrix_b | pos_i | neg_i # FIXME: is this what the notation means?

            loss = self.loss_function()

            # Update U, V over batch B to minimize loss L (Eq. 1)

        # return U + V as the graph embedding


if __name__ == "__main__":
    # graph_filename = HISTORY_DATA_DIR + '/' + GRAPH_GML_FILENAME
    # graph = nx.read_gml(graph_filename)
    graph = nx.karate_club_graph()
    print('Graph loaded')
    # nx.draw_spectral(graph)
    # plt.show()

    link_predictor = LinkPredictor(graph, nodes=graph.nodes)
    link_predictor.build_predictions_matrix()
    # print(link_predictor.link_probability_matrix[0, 9])
    # print(link_predictor.link_probability_matrix[9, 0])

    grepl = GraphEmbeddingWithPredictedLinks(graph)
    grepl.create()


