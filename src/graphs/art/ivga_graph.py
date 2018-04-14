import networkx as nx

from graphs.art.wiki_config import ART_DATA_DIR
from settings import GRAPH_GML_FILENAME
from tools.graph.ivga_graph_converter import IvgaGraphConverter

if __name__ == '__main__':
    graph_filename = ART_DATA_DIR + '/' + GRAPH_GML_FILENAME
    graph = nx.read_gml(graph_filename)
    ivga_graph_filename_no_extension = ART_DATA_DIR + '/' + 'graph'

    print("Converting graph")
    graph_converter = IvgaGraphConverter(graph, ivga_graph_filename_no_extension)
    graph_converter.convert()
