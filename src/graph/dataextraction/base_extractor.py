"""A base class for all extractors"""
import re

from graph.dataextraction.date_parser import DateParser

INFOBOX_REGEXP = re.compile(r"\{\{[Ii]infobox\}\}")
INFOBOX_DATE_REGEXP = re.compile(r"\{\{[Ii]nfobox.*\|.*date=.*\|")
TEMPLATES_REGEXP = re.compile(r"{{[^}]}}}")
REFERENCE_REGEXP = re.compile(r"\[\[[^\}]\]\]")

SPLIT_DATES_REGEX = re.compile(r"(?<!1st)(?<!nd)(?<!rd)(?<!th)-", re.UNICODE)   # capture '-' but NOT in case of 1-st,
THREE_FOUR_DIGIT_YEAR = re.compile(r"\b\d{3,4}")
YEAR_REGEXP = re.compile(r"\b\d{1,4}")
DAY_REGEXP = re.compile(r"\b\d{1,2}\b")
BC_YEAR_REGEXP = re.compile(r"(\b\d+ B\.C\.)|(\b\d+ BC)|(\b\d+B\.C\.)|(\b\d+BC)")

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

DATE_REGEXPS = {
    'date': re.compile(r"{{date\|.*\}\}"),
    'infobox': re.compile(r"\|date=[^\|]*\|"),
    'infobox_birth': re.compile(r"\|birth_date=[^\|]*\|"),
    'infobox_death': re.compile(r"\|death_date=[^\|]*\|"),
    'infobox_death_format': re.compile(r"\|death_date={{[^\}]*}}\|"),
    'infobox_designed': re.compile(r"\|design_date=[^\|]*\|"), # for weapons
    'infobox_signed': re.compile(r"\|date_signed=[^\|]*\|"),
    'infobox_effective': re.compile(r"\|date_effective=[^\|]*\|"),
}


def get_escaped_unicode(unicode_str):
    return "\\" + unicode_str


class BaseDateExtractor:

    OR_REGEXP = re.compile(r"\b\w+ or \w+\b")
    IN_REGEXP = re.compile(r"in .*", re.DOTALL)

    date_period_sign = "\u2013"

    def __init__(self):
        self.date = None
        self.start_date = None
        self.end_date = None

    def is_extraction_not_finished(self):
        return (self.date is None or not DateParser.is_valid_date(self.date)) \
                and (self.start_date is None or not DateParser.is_valid_date(self.start_date))

    def is_contains_two_dates(self, datestr):
        return SPLIT_DATES_REGEX.search(datestr) is not None \
               or get_escaped_unicode(self.date_period_sign) in datestr \
               or (' to ' in datestr and len(datestr.split(' to ')) == 2)

    def validate_dates(self):
        if not DateParser.is_valid_date(self.date):
            self.date = None
        if not DateParser.is_valid_date(self.start_date):
            self.start_date = None
        if not DateParser.is_valid_date(self.end_date):
            self.end_date = None

    def get_two_dates_from_one_str(self, orig_datestr):
        datestr = re.sub(r'\s+', ' ', orig_datestr).strip()  # orig_datestr.replace(',', '')
        datestr = re.sub(r'\-+', '-', orig_datestr)
        datestr = datestr.replace('–', '-')
        datestr = TEMPLATES_REGEXP.sub(' ', datestr)
        splitted = SPLIT_DATES_REGEX.split(datestr)
        if '\\u2013' in datestr:
            splitted = datestr.split('\\u2013')
        elif 'to ' in datestr:
            splitted = datestr.split('to')

        # year
        if len(splitted) > 1:
            splitted[0] = self.clean_date(splitted[0])
            splitted[1] = self.clean_date(splitted[1])
            from_date, till_date = self.fill_years(splitted[0].strip(), splitted[1].strip())
            from_date, till_date = self.fill_months(from_date, till_date)
            return from_date, till_date

        return datestr

    def fill_months(self, from_date, till_date):
        from_month = None
        till_month = None
        for month in MONTHS:
            if month in from_date:
                from_month = month
            if month in till_date:
                till_month = month

        if from_month is None and till_month is not None:
            from_date = self.join_date_and_month(from_date, till_month)
        if from_month is not None and till_month is None:
            till_date = self.join_date_and_month(till_date, from_month)

        return from_date, till_date

    @staticmethod
    def clean_date(datestr):
        cleaned = BaseDateExtractor.remove_or_form(datestr)
        cleaned = BaseDateExtractor.remove_in_place(cleaned)
        cleaned = re.sub(r"<ref></ref>", "", cleaned)
        removables = ['CE', 'late', 'Late', 'early', 'Early', 'summer', 'spring', 'winter', 'autumn', 'of', '\\n',
                      'born', 'died', 'death', 'sprg', 'Sprg', '?', '}', '{']
        for tag in removables:
            cleaned = cleaned.replace(tag, '')
        return cleaned

    @staticmethod
    def remove_or_form(datestr):
        return BaseDateExtractor.OR_REGEXP.sub('', datestr)

    @staticmethod
    def remove_in_place(datestr):
        return BaseDateExtractor.IN_REGEXP.sub('', datestr).strip()

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
            from_datestr += ' ' + till_year_list[0]   # year is the last one
        elif len(till_year_list) == 0 and not 'century' in till_datestr and not 'BC' in till_datestr and len(
                from_year_list) > 0:
            till_datestr += ' ' + from_year_list[0]

        return from_datestr, till_datestr

    @staticmethod
    def pad_year_with_zeros(year):
        return '0' * (4 - len(year)) + year

    @staticmethod
    def join_date_and_month(date, month):
        return month + ' ' + date

    # Static helper cleanup methods

    @staticmethod
    def preprocess_node_str(node):
        text = node.replace('\n', '')
        text = re.sub('\s+', ' ', text).strip()
        text = re.sub(r"<!--[\s\S]*?-->", '', text)     # clear comments
        # text = re.sub(r"\{\{Use dmy dates|[^\}]*\}\}", '', text)
        text = text.replace("| ", "|").replace("= ", "=").replace(" =", "=").replace('–', '-')
        text = text.replace("\\u2013", "-").replace("&ndash;", "-")
        text = text.replace("&quot;", "'")
        return text

    @staticmethod
    def remove_files_etc(node, left_sign='[', right_sign=']'):
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

    def is_filled_and_valid(self, date):
        return date is not None and DateParser.is_valid_date(date)