import networkx as nx

from graphs.history.wiki_config import HISTORY_DATA_DIR
from settings import GRAPH_GML_FILENAME
from tools.graph.ivga_graph_converter import IvgaGraphConverter

if __name__ == '__main__':
    graph_filename = HISTORY_DATA_DIR + '/' + GRAPH_GML_FILENAME
    graph = nx.read_gml(graph_filename)
    ivga_graph_filename_no_extension = HISTORY_DATA_DIR + '/' + 'graph'

    print("Converting graph")
    graph_converter = IvgaGraphConverter(graph, ivga_graph_filename_no_extension)
    graph_converter.convert()
