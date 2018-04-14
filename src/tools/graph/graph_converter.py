class GraphConverter:

    def __init__(self, graph, filename: str, attributes=list()):
        """

        :param graph: Graph or DiGraph (networkx)
        :param filename: str, filename for the converted graph
        :param attributes:
        """
        self.graph = graph
        self.filename = filename
        self.attributes = attributes

    def convert(self):
        raise NotImplementedError