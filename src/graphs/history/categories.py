from tools.category_matcher import CategoryMatcher

from settings import HISTORY_DATA_DIR
from tools.category_scraper import CategoryScraper
from wiki_config import FORBIDDEN_CATEGORY_KEYWORDS, CATEGORY_KEYWORDS, FORBIDDEN_TITLE_KEYWORDS, TITLE_KEYWORDS


class HistoryCategoryMatcher(CategoryMatcher):

    def __init__(self):
        super().__init__(whitelist=CATEGORY_KEYWORDS,
                         blacklist=FORBIDDEN_CATEGORY_KEYWORDS,
                         title_whitelist=TITLE_KEYWORDS,
                         title_blacklist=FORBIDDEN_TITLE_KEYWORDS,
                         match_dates=True)


if __name__ == "__main__":
    title = "Category:History"
    history_category_scraper = CategoryScraper(data_dir=HISTORY_DATA_DIR, category_matcher=HistoryCategoryMatcher())
    history_category_scraper.get_all_categories(title)
