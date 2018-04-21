from subprocess import call

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
