from download.category_scraper import CategoryScraper
from download.category_matcher import CategoryMatcher
from wiki_art_config import ART_CATEGORY_WHITELIST, ART_CATEGORY_BLACKLIST, ART_TITLE_WHITELIST, ART_TITLE_BLACKLIST, \
    ART_DATA_DIR


class ArtCategoryMatcher(CategoryMatcher):

    def __init__(self):
        super().__init__(whitelist=ART_CATEGORY_WHITELIST,
                         blacklist=ART_CATEGORY_BLACKLIST,
                         title_whitelist=ART_TITLE_WHITELIST,
                         title_blacklist=ART_TITLE_BLACKLIST)


if __name__ == "__main__":
    history_category_scraper = CategoryScraper(data_dir=ART_DATA_DIR, category_matcher=ArtCategoryMatcher())
    title = 'Category:Arts'
    history_category_scraper.get_all_categories(title)
