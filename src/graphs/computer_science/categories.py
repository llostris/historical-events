from graphs.computer_science.wiki_config import COMP_SCI_CATEGORY_WHITELIST, COMP_SCI_DATA_DIR, \
    COMP_SCI_TITLE_BLACKLIST, COMP_SCI_TITLE_WHITELIST, COMP_SCI_CATEGORY_BLACKLIST, FIRST_CATEGORY
from tools.category_matcher import CategoryMatcher

from tools.download.category_scraper import CategoryScraper


class ComputerScienceCategoryMatcher(CategoryMatcher):

    def __init__(self):
        super().__init__(whitelist=COMP_SCI_CATEGORY_WHITELIST,
                         blacklist=COMP_SCI_CATEGORY_BLACKLIST,
                         title_whitelist=COMP_SCI_TITLE_WHITELIST,
                         title_blacklist=COMP_SCI_TITLE_BLACKLIST,
                         match_dates=False)


if __name__ == "__main__":
    title = FIRST_CATEGORY
    history_category_scraper = CategoryScraper(data_dir=COMP_SCI_DATA_DIR,
                                               category_matcher=ComputerScienceCategoryMatcher())
    history_category_scraper.get_all_categories()
