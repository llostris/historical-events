from tqdm import tqdm

from settings import IVGA_NODES_EXT, IVGA_EDGES_EXT
from tools.graph.graph_converter import GraphConverter


class IvgaGraphConverter(GraphConverter):

    def __init__(self, graph, filename: str, attributes=list()):
        super().__init__(graph, filename, attributes)
        self.nodes_to_id_map = self.map_nodes_to_indexes()

    def map_nodes_to_indexes(self):
        nodes_to_id_map = {}
        index = 0
        for node in self.graph.node:
            nodes_to_id_map[node] = index
            index += 1
        return nodes_to_id_map

    def create_ivga_nodes_file(self):
        with open(self.filename + IVGA_NODES_EXT, 'w', encoding='utf-8') as f:
            # Write header
            f.write(',\t'.join(['name'] + self.attributes))
            f.write('\n')
            f.write('string\n')

            for _ in self.attributes:
                f.write('string\n')

            for node in tqdm(self.graph.node, desc="Nodes"):
                # print(node)
                title = node.replace(",", "")
                attribute_values = ['"' + self.graph.node[node][attr] + '"' for attr in self.attributes]
                attribute_values = ['"' + title + '"'] + attribute_values
                attrs_row = '\t'.join(attribute_values)

                index = self.nodes_to_id_map[node]
                line = "{}\t{}\n".format(index, attrs_row)
                f.write(line)

            f.close()

    def create_ivga_edges_file(self):
        with open(self.filename + IVGA_EDGES_EXT, 'w', encoding='utf-8') as f:
            for edge in tqdm(self.graph.edges, desc="Edges"):
                # print(edge)
                source_id = self.nodes_to_id_map[edge[0]]
                destination_id = self.nodes_to_id_map[edge[1]]
                f.write("{} {}\n".format(source_id, destination_id))
            f.close()

    def convert(self):
        self.create_ivga_nodes_file()
        self.create_ivga_edges_file()
