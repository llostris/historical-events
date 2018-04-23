from tools.analysis.embedding.node2vec import SnapNode2Vec

from graphs.history.wiki_config import HISTORY_DATA_DIR

if __name__ == '__main__':
    node2vec = SnapNode2Vec(HISTORY_DATA_DIR, 'graph.graph', dimensions=2)
    # node2vec.create_embedding()

    embedding = node2vec.load_embedding()
    node2vec.visualise()
