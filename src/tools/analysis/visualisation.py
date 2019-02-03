from sklearn.manifold import TSNE


class Visualisation:

    def __init__(self, graph_embedding, dimensions=2):
        self.dimensions = dimensions
        self.tsne = TSNE(n_components=self.dimensions).fit_transform(graph_embedding)

