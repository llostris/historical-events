from subprocess import call

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from settings import NODE2VEC_EXT
from file_operations import get_filepath


class SnapNode2Vec:

    def __init__(self, graph_dir: str, filename: str, embedding_filename: str ='graph', dimensions=128, walk_length=80,
                 num_walks=10, context_size=10, max_iter=1, is_weighted=False):
        """
        Creates node2vec embedding using SNAP's node2vec algorithm. Convenience function, can be replaced by
        calling ./node2vec directly from cmd line.

        :param filename: Graph file needs to be a list of edges (*.graph file).
        """
        self.graph_filename = get_filepath(graph_dir, filename)
        self.embedding_filename = get_filepath(graph_dir,
                                               embedding_filename + '_{}dim'.format(dimensions),
                                               ext=NODE2VEC_EXT)
        self.dimensions = dimensions
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.context_size = context_size
        self.max_iter = max_iter
        self.is_weighted = is_weighted
        self.embedding = None

    def create_embedding(self):
        args = [
            "gem/c_exe/node2vec",
            "-i:{}".format(self.graph_filename),
            "-o:{}".format(self.embedding_filename),
            "-d:%d" % self.dimensions,
            "-l:%d" % self.walk_length,
            "-r:%d" % self.num_walks,
            "-k:%d" % self.context_size,
            "-e:%d" % self.max_iter,
            "-dr",  # Directed graph
            "-v"    # Verbose
        ]

        if self.is_weighted:
            args.append("-w")

        try:
            call(args)
        except Exception as e:
            print(str(e))

        print("Created embedding successfully and saved it to {}.".format(self.embedding_filename))

    def load_embedding(self):
        with open(self.embedding_filename, "r") as f:
            lines = f.read().splitlines()
            first_line = lines[0]
            graph_size = int(first_line[0])
            dimensions = int(first_line[1])
            print(graph_size, dimensions)

            embedding = []

            for line in lines[1:]:
                splitted = line.split()
                id = splitted[0]
                coordinates = splitted[1:]
                embedding.append({
                    "id": id,
                    "coordinates": [float(coord) for coord in coordinates]
                })

            self.embedding = embedding
            return embedding

    def visualise(self):
        if not self.embedding:
            raise Exception("No embedding loaded!")

        coordinates_list = [node['coordinates'] for node in self.embedding]
        coordinates = []
        for dim in range(self.dimensions):
            coordinates.append([x[dim] for x in coordinates_list])

        fig = plt.figure()
        if self.dimensions == 2:
            plt.scatter(coordinates[0], coordinates[1])
        elif self.dimensions == 3:
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(coordinates[0], coordinates[1], coordinates[2])
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')

        plt.show()
