# -*- coding: utf-8 -*-
import logging
import mwparserfromhell as hell
import re

from graph.dataextraction.date_parser import DateParser
from settings import get_graph_logger

# constants

WIKIPEDIA_SECTION_HEADER_REGEXP = re.compile(r"==.*==")
INFOBOX_REGEXP = re.compile(r"\{\{[Ii]infobox\}\}")
INFOBOX_DATE_REGEXP = re.compile(r"\{\{[Ii]nfobox.*\|.*date=.*\|")
CONTENT_TIME_PERIOD_REGEXP = re.compile(r"\([^\)]*\)")
TEMPLATES_REGEXP = re.compile(r"\{\{[^\}]}\}\}")
REFERENCE_REGEXP = re.compile(r"\[\[[^\}]\]\]")

THREE_FOUR_DIGIT_YEAR = re.compile(r"\b\d{3,4}")
YEAR_REGEXP = re.compile(r"\b\d{1,4}")
DAY_REGEXP = re.compile(r"\b\d{1,2}\b")
BC_YEAR_REGEXP = re.compile(r"(\b\d+ B\.C\.)|(\b\d+ BC)|(\b\d+B\.C\.)|(\b\d+BC)")
SPLIT_DATES_REGEX = re.compile(r"(?<!1st)(?<!nd)(?<!rd)(?<!th)-", re.UNICODE) # capture '-' but NOT in case of 1-st,
# 2-nd, 3-rd,
#  4-th

DATE_REGEXPS = {
    'start date': re.compile(r"\{\{start date\|[^\}]*\}\}"),
    'birth date': re.compile(r"\{\{birth date[^\|]*\|[^\}]*\}\}"),
    'end date': re.compile(r"\{\{end date\|[^\}]*\}\}"), # TODO: add death date
    'death date': re.compile(r"\{\{death date[^\|]*\|[^\}]*\}\}"), # TODO: add death date
    'date': re.compile(r"\{\{date\|.*\}\}"),
    'infobox': re.compile(r"\|date=[^\|]*\|"),
    'infobox_birth': re.compile(r"\|birth_date=[^\|]*\|"),
    'infobox_death': re.compile(r"\|death_date=[^\|]*\|"),
    'infobox_designed': re.compile(r"\|design_date=[^\|]*\|"), # for weapons
    'infobox_signed': re.compile(r"\|date_signed=[^\|]*\|"),
    'infobox_effective': re.compile(r"\|date_effective=[^\|]*\|"),
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

# logger

logger = get_graph_logger()
logger.setLevel(logging.INFO)


def get_escaped_unicode(unicode_str):
    return "\\" + unicode_str


class DateExtractor:

    date_period_sign = "\u2013"

    OR_REGEXP = re.compile(r"\b\w+ or \w+\b")
    IN_REGEXP = re.compile(r"in .*", re.DOTALL)

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.date = None
        self.start_date = None
        self.end_date = None

    def get_dates(self):
        return self.date, self.start_date, self.end_date

    def get_isoformat(self, date):
        if date is not None and not 'UNPARSED' in date.qualifier:
            return date.isoformat()
        else:
            logger.error(u'Error parsing date for article: {} - {}'.format(self.title, self.date))
            return "None"

    def get_iso_dates(self):
        dates_map  = {}
        dates_map['date'] = self.get_isoformat(self.date)
        dates_map['start_date'] = self.get_isoformat(self.start_date)
        dates_map['end_date'] = self.get_isoformat(self.end_date)
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
                # for match in DATE_REGEXPS["infobox"].findall(x.encode('utf-8')):
                return True

        return False

    def fill_dates(self):
        page_tree = hell.parse(self.content)
        logger.info('Title: ' + self.title)
        # print(page_tree.get_tree())
        filtered = page_tree.filter(forcetype=hell.nodes.Node,
                                    matches=DateExtractor.date_matcher)

        for node in filtered:
            lowered = node.lower()
            if "{{start date" in lowered:
                self.start_date = self.extract_date_from_template("start date", node)
            if "{{end date" in lowered:
                self.end_date = self.extract_date_from_template("end date", node)

            if "{{birth date" in lowered:
                self.start_date = self.extract_date_from_template("birth date", node)
            if "{{death date" in lowered:
                self.end_date = self.extract_date_from_template("death date", node)

            if self.start_date is None and self.date is None and "infobox" in lowered:
                self.extract_from_infobox(node)
            # todo extract from other fields / content

        # if other means failed try to extract date (such as year) from content and/or title
        if self.is_extraction_not_finished():
            self.extract_from_content(self.content)

        if self.is_extraction_not_finished():
            self.extract_from_title(self.title)

        logger.info("Article: {} - Dates : {} {} {}".format(self.title, self.date, self.start_date, self.end_date))
        # print(self.date, self.start_date, self.end_date)

    def is_extraction_not_finished(self):
        return (self.date is None or not DateParser.is_valid_date(self.date)) \
                and (self.start_date is None or not DateParser.is_valid_date(self.start_date))

    def extract_date_from_template(self, date_tag, content) :
        lowered = content.lower()
        if '{{{0}'.format(date_tag) in lowered:
            regexp = DATE_REGEXPS[date_tag]
            result = regexp.findall(lowered)

            for match in result :
                # print match
                without_braces = match[2 :-2]
                splitted = without_braces.split("|")

                removables = [ "df=y", "df=yes", "df=n", "df=no" ]
                for tag in removables:
                    if tag in splitted:
                        splitted.remove(tag)

                strdate = ' '.join(splitted[1 : 4])  # skip type tag

                return DateParser().parse_flexi_date(strdate, dayfirst = False)

    def extract_from_infobox(self, node) :
        text = self.preprocess_node_str(node)
        logger.debug('Infobox raw: {}'.format(text))
        logger.info('Infobox raw: {}'.format(text))
        is_birth = False

        year = self.extract_infobox_year(text)

        matches = DATE_REGEXPS['infobox'].findall(text)
        if len(matches) == 0 :
            matches = DATE_REGEXPS['infobox_signed'].findall(text)
            self.date_type = 'signed'

        for match in matches :
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
                stripped = DateExtractor.remove_or_form(stripped)
                fd = date_parser.parse_flexi_date(stripped)
                self.date = fd
                if year is not None and fd is not None : # and DateParser.isValid(fd)
                    self.date.year = year

                    # logger.debug(self.date)

    def extract_from_content(self, node) :
        # print node
        text = self.preprocess_node_str(node)
        text = DateExtractor.remove_files_etc(text)
        text = DateExtractor.remove_files_etc(text, left_sign = '{', right_sign = '}')
        # logger.debug('Content: {}'.format(text))

        # use only first paragraph
        section_headers = WIKIPEDIA_SECTION_HEADER_REGEXP.findall(text)
        if len(section_headers) > 0 :
            text = text.split(section_headers[0])[0]

        print text
        date_found = self.extract_time_period_from_content(text)

        if not date_found:
            self.extract_from_raw_text(text)

    def extract_time_period_from_content(self, text):
        sentences = text.split(".")
        text = '. '.join(sentences[:2]) # ignore the rest

        matches = CONTENT_TIME_PERIOD_REGEXP.findall(text)

        for match in matches:
            stripped = match[1:-1]
            splitted = stripped.split(';')
            stripped = splitted[-1] # take the last one

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
        if len(years) > 0 :
            first_year = years[0]
        if year in years :
            first_year = year
        # create 3-grams around selected years
        tokens = re.sub(r"[,.!:-?]", "", text).split()
        trigrams = []
        for index in range(len(tokens) - 3) :
            trigram = tokens[index : index + 3]
            if first_year in trigram :
                trigrams.append(trigram)

        # print(trigrams)

        filtered = []
        for trigram in trigrams :
            for month in MONTHS :
                if month in trigram :
                    # check if the third value is a day
                    joined = ' '.join(trigram)
                    matches = DAY_REGEXP.findall(joined)
                    if len(matches) > 0 :
                        filtered.append(trigram)
                    else :
                        digram = self.get_2grams(joined)
                        filtered.append(digram)
                        # cut out one part of the 3-gram

        if len(filtered) == 0 and first_year is not None :
            # no month data, keep only year
            logger.debug(first_year)
            self.date = DateParser.parse_flexi_date(str(first_year))
        else :
            datestr = ' '.join(filtered[0])
            if self.is_contains_two_dates(datestr) :
                # print datestr
                from_datestr, till_datestr = self.get_two_dates_from_one_str(datestr)
                if till_datestr is not None :
                    self.start_date = DateParser.parse_flexi_date(from_datestr)
                    self.end_date = DateParser.parse_flexi_date(till_datestr)
            else :
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

    def extract_from_title(self, title) :
        # print('from title')
        years = YEAR_REGEXP.findall(title)
        for year in years :
            self.date = DateParser.parse_flexi_date(year)

            # TODO: try to extract full date

    def is_contains_two_dates(self, datestr) :
        return SPLIT_DATES_REGEX.search(datestr) is not None \
                     or get_escaped_unicode(self.date_period_sign) in datestr \
                     or (' to ' in datestr and len(datestr.split(' to ')) == 2 )

    def get_two_dates_from_one_str(self, orig_datestr) :
        datestr = re.sub(r'\s+', ' ', orig_datestr).strip() #orig_datestr.replace(',', '')
        datestr = re.sub(r'\-+', '-', orig_datestr)
        datestr = datestr.replace('–', '-')
        datestr = TEMPLATES_REGEXP.sub(' ', datestr)
        splitted = SPLIT_DATES_REGEX.split(datestr)
        if '\\u2013' in datestr :
            splitted = datestr.split('\\u2013')
        elif 'to ' in datestr :
            splitted = datestr.split('to')

        # year
        if len(splitted) > 1 :
            splitted[0] = DateExtractor.clean_date(splitted[0])
            splitted[1] = DateExtractor.clean_date(splitted[1])
            from_date, till_date = self.fill_years(splitted[0].strip(), splitted[1].strip())
            from_date, till_date = self.fill_months(from_date, till_date)
            return from_date, till_date

        return datestr

    def validate_dates(self):
        if not DateParser.is_valid_date(self.date):
            self.date = None
        if not DateParser.is_valid_date(self.start_date):
            self.start_date = None
        if not DateParser.is_valid_date(self.end_date):
            self.end_date = None

    @staticmethod
    def clean_date(datestr):
        cleaned = DateExtractor.remove_or_form(datestr)
        cleaned = DateExtractor.remove_in_place(cleaned)
        cleaned = re.sub(r"<ref></ref>", "", cleaned)
        removables = ['CE', 'late', 'Late', 'early', 'Early', 'summer', 'spring', 'winter', 'autumn', 'of', '\\n',
                      'born', 'died', 'death', 'sprg', 'Sprg', '?', '}', '{' ]
        for tag in removables :
            cleaned = cleaned.replace(tag, '')
        return cleaned

    @staticmethod
    def remove_or_form(datestr):
        return DateExtractor.OR_REGEXP.sub('', datestr)

    @staticmethod
    def remove_in_place(datestr):
        return DateExtractor.IN_REGEXP.sub('', datestr).strip()

    @staticmethod
    def fill_years(from_datestr, till_datestr):
        from_year_list = THREE_FOUR_DIGIT_YEAR.findall(from_datestr)
        till_year_list = THREE_FOUR_DIGIT_YEAR.findall(till_datestr)

        # BC dates
        from_year_BC_match = BC_YEAR_REGEXP.search(from_datestr)
        till_year_BC_match = BC_YEAR_REGEXP.search(till_datestr)

        if len(from_year_list) == 0 and from_year_BC_match is not None:
            from_year_list.append(from_year_BC_match.group())
        elif len(till_year_list) == 0 and till_year_BC_match is not None:
            till_year_list.append(till_year_BC_match.group())

        # 000 - 99 years
        if len(till_datestr.split()) == 3:
            year = till_datestr.split()[-1]
            till_year_list.append(year) # year is last
        elif len(from_datestr.split()) == 3:
            year = from_datestr.split()[-1]
            from_year_list.append(year)
            # it contains date

        if len(from_year_list) == 0 and not 'century' in from_datestr and not 'BC' in from_datestr and len(
                till_year_list) > 0:
            from_datestr += ' '  + till_year_list[0]   # year is the last one
        elif len(till_year_list) == 0 and not 'century' in till_datestr and not 'BC' in till_datestr and len(
                from_year_list) > 0:
            till_datestr += ' '  + from_year_list[0]

        return from_datestr, till_datestr

    def fill_months(self, from_date, till_date) :
        from_month = None
        till_month = None
        for month in MONTHS :
            if month in from_date :
                from_month = month
            if month in till_date :
                till_month = month

        if from_month is None and till_month is not None :
            from_date = self.join_date_and_month(from_date, till_month)
        if from_month is not None and till_month is None :
            till_date = self.join_date_and_month(till_date, from_month)

        return from_date, till_date

    # Static helper methods

    @staticmethod
    def pad_year_with_zeros(year):
        return '0' * (4 - len(year)) + year

    @staticmethod
    def join_date_and_month(date, month) :
        return month + ' ' + date

    @staticmethod
    def preprocess_node_str(node):
        text = node.encode('utf-8').replace('\n', '')
        text = re.sub('\s+', ' ', text).strip()
        text = re.sub(r"<!--[\s\S]*?-->", '', text) # clear comments
        # text = re.sub(r"\{\{Use dmy dates|[^\}]*\}\}", '', text)
        text = text.replace("| ", "|").replace("= ", "=").replace(" =", "=").replace('–', '-')
        text = text.replace("\\u2013", "-").replace("&ndash;", "-")
        text = text.replace("&quot;", "'")
        return text

    @staticmethod
    def remove_files_etc(node, left_sign = '[', right_sign = ']'):
        left_braces = []
        start_index = -1
        index = 0
        to_remove = []
        for char in node:
            if char == left_sign:
                if len(left_braces) == 0:
                    start_index = index
                left_braces.append(left_sign)

            if char == right_sign and len(left_braces) > 0:
                left_braces.pop()

            if start_index != -1 and len(left_braces) == 0:
                end_index = index
                substr = node[start_index:end_index + 1]
                to_remove.append(substr)
            index = index + 1

        text = node
        for removed in to_remove:
            text = text.replace(removed, '')

        return text

    @staticmethod
    def extract_infobox_parameter(parameter_str):
        stripped = parameter_str[1:-1] # remove | signs
        stripped = stripped.split('=')[1]  # extract date only
        stripped = re.sub("\<.*", "", stripped) # remove any additional stuff at the end
        stripped = stripped.replace('\\n', '')
        return stripped

    @staticmethod
    def extract_infobox_year(infobox_text):
        year_matches = re.findall("\|year=[^\|]*\|", infobox_text)
        for year in year_matches:
            stripped = year[1:-1] # skip | signs at the begginning and the end
            stripped = stripped.replace('year=', '')
            return stripped
