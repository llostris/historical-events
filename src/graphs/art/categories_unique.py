from graphs.art.categories import ArtCategoryMatcher
from graphs.art.wiki_config import ART_DATA_DIR
from tools.unique_category_generator import UniqueCategoryListGenerator

if __name__ == "__main__":
    unique_list_generator = UniqueCategoryListGenerator(data_dir=ART_DATA_DIR, category_matcher=ArtCategoryMatcher())
    unique_list_generator.get_unique_categories()
