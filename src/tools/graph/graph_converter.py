
class GraphConverter:

    def __init__(self, graph, filename: str, attributes=list()):
        self.graph = graph
        self.filename = filename
        self.attributes = attributes
        self.nodes_to_id_map = self.map_nodes_to_indexes()

    def map_nodes_to_indexes(self):
        nodes_to_id_map = {}
        index = 0
        for node in self.graph.node:
            nodes_to_id_map[node] = index
            index += 1
        return nodes_to_id_map

    def create_ivga_nodes_file(self):
        with open(self.filename + '.desc', 'w', encoding='utf-8') as f:
            f.write(',\t'.join(['name'] + self.attributes))
            f.write('\n')
            f.write('string\n')
            # f.write('string,\tstring,\tstring,\tstring\n')
            f.write('string\n')

            for node in self.graph.node:
                print(node)
                title = node.replace(",", "")
                attribute_values = ['"' + self.graph.node[node][attr] + '"' for attr in self.attributes]
                attribute_values = ['"' + title + '"'] + attribute_values
                attrs_row = '\t'.join(attribute_values)

                index = self.nodes_to_id_map[node]
                line = "{}\t{}\n".format(index, attrs_row)
                f.write(line)

            f.close()

    def create_ivga_edges_file(self):
        with open(self.filename + '.graph', 'w', encoding='utf-8') as f:
            for edge in self.graph.edges:
                print(edge)
                source_id = self.nodes_to_id_map[edge[0]]
                destination_id = self.nodes_to_id_map[edge[1]]
                f.write("{} {}\n".format(source_id, destination_id))
            f.close()

    def create_ivga_graph(self):
        self.create_ivga_nodes_file()
        self.create_ivga_edges_file()
