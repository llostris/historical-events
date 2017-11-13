import re

from settings import get_graph_logger
from tools.data_extraction import BaseDateExtractor, DATE_REGEXPS
from tools.data_extraction import DateParser

logger = get_graph_logger()


class InfoboxDateExtractor(BaseDateExtractor):

    def __init__(self):
        BaseDateExtractor.__init__(self)

    def extract_infobox_birth_date(self, text):
        matches = DATE_REGEXPS['infobox_birth'].findall(text)
        if len(matches) > 0:
            stripped = self.extract_infobox_parameter(matches[0])
            self.start_date = DateParser.parse_flexi_date(stripped)

    def extract_infobox_death_date(self, text):
        matches = DATE_REGEXPS['infobox_death'].findall(text)
        if len(matches) > 0:
            stripped = self.extract_infobox_parameter(matches[0])
            self.end_date = DateParser.parse_flexi_date(stripped)

    @staticmethod
    def extract_infobox_parameter(parameter_str):
        stripped = parameter_str[1:-1]  # remove | signs
        stripped = stripped.split('=')[1]  # extract date only
        stripped = re.sub("\<.*", "", stripped)  # remove any additional stuff at the end
        stripped = stripped.replace('\\n', '')
        return stripped

    @staticmethod
    def extract_infobox_year(infobox_text):
        year_matches = re.findall("\|year=[^\|]*\|", infobox_text)
        for year in year_matches:
            stripped = year[1:-1]   # skip | signs at the begginning and the end
            stripped = stripped.replace('year=', '')
            return stripped

    def extract_from_infobox(self, node):
        text = self.preprocess_node_str(node)
        logger.debug('Infobox raw: {}'.format(text))

        if not self.is_filled_and_valid(self.start_date):
            self.extract_infobox_birth_date(text)
        if not self.is_filled_and_valid(self.end_date):
            self.extract_infobox_death_date(text)

        if self.start_date is not None and self.end_date is not None:
            return

        year = self.extract_infobox_year(text)

        matches = DATE_REGEXPS['infobox'].findall(text)
        if len(matches) == 0:
            matches = DATE_REGEXPS['infobox_signed'].findall(text)
            self.date_type = 'signed'

        for match in matches:
            stripped = self.extract_infobox_parameter(match)
            date_parser = DateParser()

            # fill year if lacking
            if self.is_contains_two_dates(stripped):
                from_date, till_date = self.get_two_dates_from_one_str(stripped)

                self.start_date = date_parser.parse_flexi_date(from_date)
                self.end_date = date_parser.parse_flexi_date(till_date)
                if self.start_date.year is None:
                    self.start_date.year = self.end_date.year
                elif self.end_date.year is None:
                    self.end_date.year = self.start_date.year
                elif year is not None:
                    if self.start_date.year is not None:
                        self.start_date.year = year
                    if self.end_date.year is not None:
                        self.end_date.year = year
                # logger.debug(self.start_date, self.end_date)
            elif self.date is None:
                stripped = self.remove_or_form(stripped)
                fd = date_parser.parse_flexi_date(stripped)
                self.date = fd
                if year is not None and fd is not None : # and DateParser.isValid(fd)
                    self.date.year = year

                    # logger.debug(self.date)
