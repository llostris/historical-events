import os
import re

import mwparserfromhell as hell

from graph.model.vertex_extractor import ARTICLE_FILE_NAME_PREFIX, load_article_from_pickle
from settings import DATA_DIR


class RelationshipExtractor:
    forbidden_keywords = ['File:', 'Category:', 'ca:']
    language_regexp = re.compile(r"^[a-z]{2}:")

    def __init__(self, content, tree=None):
        self.content = content
        self.tree = tree
        self.wikilinks = []

        if tree is None:
            self.tree = hell.parse(content)

    def extract_wikilinks(self):
        raw_wikilinks = self.tree.filter_wikilinks()
        print(raw_wikilinks)

        stripped = map(self.strip_wikilink, raw_wikilinks)

        filtered = filter(self.filter_wikilink, stripped)

        self.wikilinks = list(filtered)

    def get_relationships(self) :
        if len(self.wikilinks) == 0:
            self.extract_wikilinks()

        return self.wikilinks

    @staticmethod
    def filter_wikilink(text):
        for key in RelationshipExtractor.forbidden_keywords:
            if key in text:
                return False

        if len(RelationshipExtractor.language_regexp.findall(text)) > 0:
            return False

        return True

    @staticmethod
    def strip_wikilink(text):
        """
        Extracts title of the page referenced by the link.
        From: https://en.wikipedia.org/wiki/Help:Link
        [[abc]] is seen as "abc" in text and links to page "abc".
        [[a|b]] is labelled "b" on this page but links to page "a".
        [[a]]b gives ab. So does [[a|ab]]: ab. The code [[a|b]]c gives bc, just as [[a|bc]] does. However, all four of these examples will link to page "a".
        a[[b]] gives ab.
        [[a]]:b gives a:b since the colon is outside the end brackets. The same goes for [[Washington]]'s or e-[[mail]].
        [[a]]''b'', ''[[a]]''b gives ab. (Double apostrophes turn on and off italics.)
        [[a|b]]cd gives bcd, and shows an example of link trailing.
        [[a]]<nowiki />b gives ab. (The nowiki tag is needed to turn off the so-called "linktrail rules".)
        [[a|b]]<nowiki />c gives bc.

        :param text:  a wikilink, ex. [[Great Britain|England]]
        :return: a title of a wikipage which is referenced by the wikilink
        """
        stripped = text[2:-2]
        page_title = stripped.split("|")[0]
        return page_title


if __name__ == "__main__":

    articles = []

    for elem in os.listdir(DATA_DIR):
        if elem.startswith(ARTICLE_FILE_NAME_PREFIX):
            print(elem)
            article_batch = load_article_from_pickle(elem)
            articles += article_batch

    print(len(articles))

    events = []
    for article in articles[0:1]:
        print(article.title)
        relationship_extractor = RelationshipExtractor(article.content)
        print(relationship_extractor.get_relationships())

