"""Implementation of Node2Vec according to publication 'Graph Embeddings with Predicted Links' (GREPL)."""
import networkx as nx
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, cross_val_score


class LinkPredictor:

    def __init__(self, graph):
        self.graph = graph.to_undirected()  # This algorithm doesn't work for directed graphs?
        self.training_nodes = set()
        self.test_nodes = set()
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
        common_neighbour_node_pairs = self._get_common_neighbour_node_pairs()
        df = pd.DataFrame(columns=['nodes', 'adjusted_degree1', 'adjusted_degree2', 'common_neighbours',
                                   'adamic_adar_score'])

        for node1, node2 in common_neighbour_node_pairs:
            has_edge = 1 if node1 in self.graph.neighbors(node2) else 0   # value of adjacency matrix for (node1, node2)

            adamic_adar_score_result = list(nx.adamic_adar_index(self.graph, [(node1, node2)]))
            # It's a one-element list of (node1, node2, score)
            adamic_adar_score = adamic_adar_score_result[0][2]

            df = df.append({
                'nodes': (node1, node2),
                'adjusted_degree1': self.graph.degree(node1) - has_edge,
                'adjusted_degree2': self.graph.degree(node2) - has_edge,
                'common_neighbours': len(list(nx.common_neighbors(self.graph, node1, node2))),  # FIXME: Don't calcualte this twice~
                'adamic_adar_score': adamic_adar_score,
                'edge': has_edge
            }, ignore_index=True)

        df = df.set_index('nodes')

        positive_examples, negative_examples = self._get_positive_and_negative_examples(common_neighbour_node_pairs)
        print(positive_examples, negative_examples)

        # Take only rows that are in our positive or negative examples
        print('DataFrame before filtering', df.shape)
        training_df = df[df.index.isin(positive_examples | negative_examples)]
        print('DataFrame after filtering', training_df.shape)

        train_X = training_df.drop('edge', axis=1)
        train_y = training_df['edge']

        # Train RF Classifier
        rf_classifier = RandomForestClassifier()
        # rf_classifier.fit(train_X, train_y)

        # Cross-validation accuracy of m

        # scoring = ['accuracy']
        # cv_result = cross_validate(rf_classifier, train_X, train_y, scoring=scoring)
        # print(cv_result)

        cv_scores = cross_val_score(rf_classifier, train_X, train_y, scoring='accuracy')
        mean_cv_score = cv_scores.mean()
        print(cv_scores, mean_cv_score)

        test_examples = self._get_test_examples()

    def _get_test_examples(self):
        test_examples = set()
        for node1 in self.graph.nodes():
            for node2 in self.graph.nodes():
                if node1 not in self.graph.neighbors(node2):
                    test_examples.add((node1, node2))

        return test_examples

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
        :returns: two lists of tuples (i, j) representing nodes
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
    graph = nx.lollipop_graph(5, 5)
    print('Graph loaded')

    grepl = GraphEmbeddingWithPredictedLinks(graph)
    grepl.get_link_predictions()


