from graphs.history.wiki_config import HISTORY_CATEGORY_WHITELIST, HISTORY_CATEGORY_BLACKLIST, HISTORY_TITLE_WHITELIST, \
    HISTORY_TITLE_BLACKLIST, HISTORY_DATA_DIR
from tools.category_matcher import CategoryMatcher

from tools.category_scraper import CategoryScraper


class HistoryCategoryMatcher(CategoryMatcher):

    def __init__(self):
        super().__init__(whitelist=HISTORY_CATEGORY_WHITELIST,
                         blacklist=HISTORY_CATEGORY_BLACKLIST,
                         title_whitelist=HISTORY_TITLE_WHITELIST,
                         title_blacklist=HISTORY_TITLE_BLACKLIST,
                         match_dates=True)


if __name__ == "__main__":
    title = "Category:History"
    history_category_scraper = CategoryScraper(data_dir=HISTORY_DATA_DIR, category_matcher=HistoryCategoryMatcher())
    history_category_scraper.get_all_categories(title)
