import re

from base_wiki_config import CATEGORY_REGEXP, YEAR_IN_REGEXP, NUMBER_ONLY_REGEXP


DATE_YEAR_IN_REGEXP = re.compile(r"(\d+ .* in)|(in \d+)")


class CategoryMatcher:

    def __init__(self, whitelist=set(), blacklist=set(), title_whitelist=set(), title_blacklist=set(),
                 match_dates=False):
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.title_whitelist = title_whitelist
        self.title_blacklist = title_blacklist
        self.match_dates = match_dates  # should be set true only for historical articles

    def is_category_related(self, category_name):
        category_name = category_name.lower()

        if self.match_dates and DATE_YEAR_IN_REGEXP.match(category_name):
            return True

        return self.is_category_relevant(category_name)

        # if self.is_category_relevant(category_name):
        #     if self.match_dates and DATE_YEAR_IN_REGEXP.match(category_name):
        #         return True
        # return False

    def is_category_relevant(self, category_name, strict=True):
        for white_word in self.whitelist:
            if white_word in category_name.lower():
                return True

        for forbidden_word in self.blacklist:
            if forbidden_word in category_name.lower():
                return False
        return True

    def is_article_relevant(self, title, content):
        categories = CATEGORY_REGEXP.findall(content)
        for category in categories:
            if not self.is_category_relevant(category, strict=False):
                return False

        return self.is_article_title_relevant(title)

    def is_article_title_relevant(self, title):
        for white_word in self.title_whitelist:
            if white_word in title.lower():
                return True

        for forbidden_word in self.title_blacklist:
            if forbidden_word in title.lower():
                return False

        if self.match_dates and \
                (YEAR_IN_REGEXP.search(title) is not None or NUMBER_ONLY_REGEXP.search(title) is not None):
            return False

        return True
