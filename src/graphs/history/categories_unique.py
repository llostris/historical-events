from graphs.history.categories import HistoryCategoryMatcher
from graphs.history.wiki_config import HISTORY_DATA_DIR
from tools.unique_category_generator import UniqueCategoryListGenerator

if __name__ == "__main__":
    unique_list_generator = UniqueCategoryListGenerator(data_dir=HISTORY_DATA_DIR,
                                                        category_matcher=HistoryCategoryMatcher())
    unique_list_generator.get_unique_categories()
