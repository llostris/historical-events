from graphs.art.categories import ArtCategoryMatcher
from graphs.art.wiki_config import ART_DATA_DIR
from tools.graph_creator import GraphCreator

if __name__ == "__main__":
    graph_creator = GraphCreator(data_dir=ART_DATA_DIR, category_matcher=ArtCategoryMatcher())
    graph_creator.create_graph_from_articles()
