# -*- coding: utf-8 -*-
import logging
import re

import mwparserfromhell as hell

from settings import get_graph_logger
from tools.data_extraction.base_extractor import BaseDateExtractor, THREE_FOUR_DIGIT_YEAR, YEAR_REGEXP, DAY_REGEXP, \
    MONTHS
from tools.data_extraction.date_parser import DateParser
from tools.data_extraction.infobox_extractor import InfoboxDateExtractor
from tools.data_extraction.template_mixin import TemplateDateExtractorMixin

# constants

WIKIPEDIA_SECTION_HEADER_REGEXP = re.compile(r"==.*==")
CONTENT_TIME_PERIOD_REGEXP = re.compile(r"\([^\)]*\)")

# logger

logger = get_graph_logger()
logger.setLevel(logging.INFO)


class DateExtractor(InfoboxDateExtractor, TemplateDateExtractorMixin):

    def __init__(self, title, content):
        BaseDateExtractor.__init__(self)

        self.title = title
        self.content = content

        self.date_parser = DateParser()

    @staticmethod
    def is_unparsed(date):
        if isinstance(date.qualifier, str):
            return 'UNPARSED' in date.qualifier
        else:
            return 'UNPARSED' in date.qualifier.decode('utf-8')

    def get_isoformat(self, date):
        print("get_isoformat: {}".format(date))
        if date is not None and not self.is_unparsed(date):
            return date.isoformat()
        else:
            logger.error(u'Error parsing date for article: {} - {}'.format(self.title, self.date))
            return "None"

    def get_iso_dates(self):
        dates_map = {
            'date': self.get_isoformat(self.date),
            'start_date': self.get_isoformat(self.start_date),
            'end_date': self.get_isoformat(self.end_date)
        }
        return dates_map

    @staticmethod
    def date_matcher(x):
        lowered = x.lower()
        # print('node ' + lowered)
        keywords = ['{{date', '{{start date', '{{end date']
        for key in keywords:
            if key in lowered:
                return True

        if type(x) == hell.nodes.template.Template and "infobox" in x.name.lower():
            # we have infobox, now check for date
            # print("template name " + str(x.name))
            if "date" in x.lower():
                # TODO: make more strict
                return True

        return False

    def fill_dates(self):
        page_tree = hell.parse(self.content)
        logger.info('Title: ' + self.title)
        filtered = page_tree.filter(forcetype=hell.nodes.Node, matches=DateExtractor.date_matcher)

        for node in filtered:
            lowered = node.lower()

            self.extract_start_date_from_templates(lowered)
            self.extract_end_date_from_templates(lowered)

            if self.start_date is None and self.date is None and "infobox" in lowered:
                self.extract_from_infobox(node)

            if not self.start_date and not self.end_date and not self.date:
                logger.debug(lowered)

        # if other means failed try to extract date (such as year) from content and/or title
        if self.is_extraction_not_finished():
            self.extract_from_content(self.content)

        if self.is_extraction_not_finished():
            self.extract_from_title(self.title)

        logger.info("Article: {} - Dates : {} {} {}".format(self.title, self.date, self.start_date, self.end_date))

    def extract_from_content(self, node):
        # print node
        text = self.preprocess_node_str(node)
        text = DateExtractor.remove_files_etc(text)
        text = DateExtractor.remove_files_etc(text, left_sign='{', right_sign='}')
        # logger.debug('Content: {}'.format(text))

        # use only first paragraph
        section_headers = WIKIPEDIA_SECTION_HEADER_REGEXP.findall(text)
        if len(section_headers) > 0:
            text = text.split(section_headers[0])[0]

        print(text)
        date_found = self.extract_time_period_from_content(text)

        if not date_found:
            self.extract_from_raw_text(text)

    def extract_time_period_from_content(self, text):
        sentences = text.split(".")
        text = '. '.join(sentences[:2])  # ignore the rest

        matches = CONTENT_TIME_PERIOD_REGEXP.findall(text)

        for match in matches:
            stripped = match[1:-1]
            splitted = stripped.split(';')
            stripped = splitted[-1]  # take the last one

            if self.is_contains_two_dates(stripped):
                from_date, till_date = self.get_two_dates_from_one_str(stripped)
                found = False

                if from_date is not None and DateParser.is_valid_date(from_date):
                    self.start_date = DateParser.parse_flexi_date(from_date)
                    found = True
                if till_date is not None and DateParser.is_valid_date(till_date):
                    self.end_date = DateParser.parse_flexi_date(till_date)
                    found = True

                if found:
                    return True # break
            else:
                stripped = DateExtractor.clean_date(stripped)
                fd = DateParser.parse_flexi_date(stripped)
                if fd is not None and DateParser.is_valid_date(fd):
                    self.date = fd
                    return True

        return False

    def extract_from_raw_text(self, text):
        year = self.extract_from_title(self.title)

        # look for years:
        years = THREE_FOUR_DIGIT_YEAR.findall(text)
        first_year = 0
        if len(years) > 0:
            first_year = years[0]
        if year in years:
            first_year = year
        # create 3-grams around selected years
        tokens = re.sub(r"[,.!:-?]", "", text).split()
        trigrams = []
        for index in range(len(tokens) - 3):
            trigram = tokens[index: index + 3]
            if first_year in trigram:
                trigrams.append(trigram)

        # print(trigrams)

        filtered = []
        for trigram in trigrams:
            for month in MONTHS:
                if month in trigram:
                    # check if the third value is a day
                    joined = ' '.join(trigram)
                    matches = DAY_REGEXP.findall(joined)
                    if len(matches) > 0:
                        filtered.append(trigram)
                    else:
                        digram = self.get_2grams(joined)
                        filtered.append(digram)
                        # cut out one part of the 3-gram

        if len(filtered) == 0 and first_year is not None:
            # no month data, keep only year
            logger.debug(first_year)
            self.date = DateParser.parse_flexi_date(str(first_year))
        else:
            datestr = ' '.join(filtered[0])
            if self.is_contains_two_dates(datestr):
                # print datestr
                from_datestr, till_datestr = self.get_two_dates_from_one_str(datestr)
                if till_datestr is not None:
                    self.start_date = DateParser.parse_flexi_date(from_datestr)
                    self.end_date = DateParser.parse_flexi_date(till_datestr)
            else:
                self.date = DateParser.parse_flexi_date(datestr)

    def get_2grams(self, trigram_joined):
        valid_parts = []
        for month in MONTHS:
            if month in trigram_joined:
                valid_parts.append(month)
                break
        year = YEAR_REGEXP.findall(trigram_joined)[-1]
        valid_parts.append(year)
        return valid_parts

    def extract_from_title(self, title):
        # print('from title')
        years = YEAR_REGEXP.findall(title)
        for year in years:
            self.date = DateParser.parse_flexi_date(year)

            # TODO: try to extract full date
