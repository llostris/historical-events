from graphs.history.wiki_config import HISTORY_DATA_DIR
from tools.language_graph_creator import LanguageGraphCreator

if __name__ == "__main__":
    language_graph_creator = LanguageGraphCreator(data_dir=HISTORY_DATA_DIR, language='pl')
    language_graph_creator.create_language_restricted_graph()

    language_graph_creator = LanguageGraphCreator(data_dir=HISTORY_DATA_DIR, language='de')
    language_graph_creator.create_language_restricted_graph()
