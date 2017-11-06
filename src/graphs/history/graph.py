from graphs.history.categories import HistoryCategoryMatcher
from graphs.history.wiki_config import HISTORY_DATA_DIR
from tools.graph_creator import GraphCreator

if __name__ == "__main__":
    graph_creator = GraphCreator(data_dir=HISTORY_DATA_DIR, category_matcher=HistoryCategoryMatcher())
    graph_creator.create_graph_from_articles()
