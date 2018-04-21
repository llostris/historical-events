from tools.analysis.embedding.node2vec import SnapNode2Vec
from graphs.art.wiki_config import ART_DATA_DIR

if __name__ == '__main__':
    SnapNode2Vec(ART_DATA_DIR, 'graph.graph', dimensions=2).create_embedding()
