import re

from graphs.art.wiki_config import ART_CATEGORY_WHITELIST, ART_CATEGORY_BLACKLIST, ART_TITLE_WHITELIST, \
    ART_TITLE_BLACKLIST, \
    ART_DATA_DIR
from tools.category_matcher import CategoryMatcher
from tools.category_scraper import CategoryScraper


class ArtCategoryMatcher(CategoryMatcher):
    DATE_YEAR_IN_COUNTRY_REGEXP = re.compile(r"\d+ by country")

    def __init__(self):
        super().__init__(whitelist=ART_CATEGORY_WHITELIST,
                         blacklist=ART_CATEGORY_BLACKLIST,
                         title_whitelist=ART_TITLE_WHITELIST,
                         title_blacklist=ART_TITLE_BLACKLIST)

    def is_category_relevant(self, category_name):
        category_name = category_name.lower()

        if self.DATE_YEAR_IN_COUNTRY_REGEXP.match(category_name):
            return False

        return super().is_category_relevant(category_name)


if __name__ == "__main__":
    art_category_scraper = CategoryScraper(data_dir=ART_DATA_DIR,
                                           category_matcher=ArtCategoryMatcher(),
                                           continuation=True)
    title = 'Category:Arts'
    art_category_scraper.get_all_categories(title)
