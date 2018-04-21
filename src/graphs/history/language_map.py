from graphs.history.wiki_config import HISTORY_DATA_DIR
from tools.download.language_map_creator import LanguageMapCreator

if __name__ == "__main__":
    language_map_creator = LanguageMapCreator(data_dir=HISTORY_DATA_DIR)
    language_map_creator.get_langlinks()
