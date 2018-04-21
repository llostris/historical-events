from tools.analysis.embedding.node2vec import SnapNode2Vec

from graphs.history.wiki_config import HISTORY_DATA_DIR

if __name__ == '__main__':
    SnapNode2Vec(HISTORY_DATA_DIR, 'graph.graph', dimensions=3).create_embedding()
