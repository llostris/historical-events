# -*- coding: utf-8 -*-
"""Contains different functions for converting pickle files (nodes and relationship matrix) to different graph
formats, i.e.:
* GML
* ivGa graph format
* SNAP format
"""

from graph.graph_creator import load_in_progress_graph, load_relationship_map
from settings import DATA_DIR

attributes_networkx = ['date', 'startdate', 'enddate']
attributes = [] #[ 'date', 'start_date', 'end_date' ]


def create_graph_ivga(graph, relationship_map, filename='graph', include_lone_nodes=True):
    """

    :param graph: Graph in networkx format.
    :param relationship_map: Map in form of source -> [ destinations ]
    :param filename: String. Name of the file (without extension) that the graph should be saved to.
    :return: None
    """

    nodes_to_id_map = {}

    index = 0
    for node in graph.node :
        nodes_to_id_map[node] = index
        index += 1

    graph_edges = []

    existing_nodes = set()
    lone_vertices = set()

    with open(DATA_DIR + "/" + filename + '.graph', 'w+', encoding='utf-8') as f:
        for node, edges in relationship_map.items():
            source_node = nodes_to_id_map[node]
            existing_nodes.add(source_node)
            for destination_name in set(edges):
                if destination_name in nodes_to_id_map:
                    destination_node = nodes_to_id_map[destination_name]
                    f.write("{} {}\n".format(source_node, destination_node))

                    existing_nodes.add(destination_node)

        f.close()

    print(len(existing_nodes))

    with open(DATA_DIR + '/' + filename + '.desc', 'w+', encoding='utf-8') as f:
        f.write(',\t'.join(['title'] + attributes))
        f.write('\n')
        # f.write('string,\tstring,\tstring,\tstring\n')
        f.write('string\n')
        len_of_nodes = len(graph.node)
        for node in graph.node:
            print(node)
            index = nodes_to_id_map[node]

            if index in existing_nodes:
                title = node.replace(",", "")
                attribute_values = ['"' + graph.node[node][attr] + '"' for attr in attributes]
                attribute_values = ['"' + title + '"'] + attribute_values
                attrs_row = '\t'.join(attribute_values)
                line = "{}\t{}\n".format(index, attrs_row)

                if index == len_of_nodes - 1:
                    line = line[:-2]

                f.write(line)
            else:
                lone_vertices.add(node)
                # print('Vertex with no edges: ' + node)

        if include_lone_nodes:
            for node in lone_vertices:
                pass
                # TODO: implement me

        f.close()


if __name__ == "__main__":

    graph = load_in_progress_graph()
    relationship_map = load_relationship_map()

    print("Loaded")

    create_graph_ivga(graph, relationship_map, include_lone_nodes=True)