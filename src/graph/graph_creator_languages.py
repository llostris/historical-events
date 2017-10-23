"""Create a graph based on existing historical graph and langlinks. 
This results in a smaller, more specific graph."""
from networkx import write_gml

from file_operations import load_pickle, save_pickle
from graph.graph_creator import load_in_progress_graph
from settings import LANGUAGE_MAP_FILE, GRAPH_LANGUAGE_GML_FILE


def filter_out_language_nodes(language_map, language):
    filtered = filter(lambda x: language in language_map[x]['languages'], language_map)
    return set(filtered)


def build_graph_restricted_to_language(graph, language):
    language_map = load_pickle(LANGUAGE_MAP_FILE)

    matching_nodes = filter_out_language_nodes(language_map, language)
    for node in graph.nodes():
        if node not in matching_nodes:
            graph.remove_node(node)

    write_gml(graph, GRAPH_LANGUAGE_GML_FILE.format(language))
    save_pickle(graph, GRAPH_LANGUAGE_GML_FILE.format(language) + '.pickle')

    print("Number of nodes:", graph.number_of_nodes())
    print("Number of edges:", graph.number_of_edges())

if __name__ == "__main__":
    graph = load_in_progress_graph()
    build_graph_restricted_to_language(graph, 'pl')

    graph = load_in_progress_graph()
    build_graph_restricted_to_language(graph, 'de')
