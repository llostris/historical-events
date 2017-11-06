
from datetime import datetime
import re
from flexidate import parse, FlexiDate

from settings import graph_logger

NUMBER_REGEXP = re.compile("\d+")


class DateParser:
    pattern_day_month_year = "%d %B %Y"
    pattern_month_year = "%B %Y"
    pattern_year = "%Y"
    three_digit_year = r"\b\d{1,3}"
    arabic_year_regexp = re.compile(r"\b\d+ AH")

    def __init__(self):
        pass

    def parse_date(self, strdate):
        num_of_elements = len(strdate.split(' '))
        if num_of_elements == 3:
            return datetime.strptime(strdate, self.pattern_day_month_year), True
        elif num_of_elements == 2:
            return datetime.strptime(strdate, self.pattern_month_year), False
        else:
            return datetime.strptime(strdate, self.pattern_year), False

    @staticmethod
    def clean_date(strdate):
        strdate = DateParser.arabic_year_regexp.sub('', strdate)

        removables = [ 'in', 'of', 'CE', '}', '{' ]
        for tag in removables:
            strdate = strdate.replace(tag, '')

        return strdate

    @staticmethod
    def parse_flexi_date(strdate, dayfirst=True):
        """

        :param strdate:
        :param dayfirst:
        :return:
        """
        strdate = DateParser.clean_date(strdate)

        graph_logger.debug('DateParser.parse_flexi_date: {}'.format(strdate))
        strdate = DateParser.handle_century(strdate)
        if strdate is not None and strdate != '0000' and not 'INF' in strdate:
            try:
                fd = parse(strdate)
                if dayfirst:
                    fd = DateParser.handle_year(strdate, fd)
                return fd
            except TypeError:
                graph_logger.error('Invalid date: {}'.format(strdate))
                return None
        return None

    @staticmethod
    def handle_year(strdate, fd):
        is_bc = DateParser.is_before_christ(strdate)

        if is_bc:
            strdate = strdate.replace('BC', '')

        splitted = strdate.replace(',', '').split()
        if len(splitted) > 0:
            year = splitted[-1] # if there is a year, it's the last part
            if re.match(DateParser.three_digit_year, year) is not None:
                # it's a 1-3 digit year
                if is_bc:
                    year = '-' + year

                fd.year = fd._cvt(year, rjust = 4, force = False)

        return fd

    @staticmethod
    def handle_century(strdate):
        """ May be error-prone."""
        date = strdate
        if "century" in strdate:
            new_date = ''
            year = 100
            for number in NUMBER_REGEXP.findall(strdate):
                no_century = int(number)
                years = year * no_century
                print(years)
                new_date = str(years)
            if "BC" in strdate or "B.C." in strdate:
                new_date = str(new_date) + " BC"
            return new_date
        return date

    @staticmethod
    def is_before_christ(strdate):
        return 'BC' in strdate or 'B.C.' in strdate

    @staticmethod
    def is_valid_date(date) :
        if isinstance(date, FlexiDate):
            return date is not None and (len(date.year) > 0 or len(date.month) > 0 or len(date.day) > 0)
        else:
            return 'UNPARSED' not in str(date)


if __name__ == "__main__":
    century_string = 'Late 4th century BC'
    date_parser = DateParser()

    print(date_parser.parse_flexi_date(century_string))

    three_digit_year_full_date = 'April 19, 337'
    print(date_parser.parse_flexi_date(three_digit_year_full_date))

    three_digit_year_full_date = 'April, 0047 A.D.'
    print(date_parser.parse_flexi_date(three_digit_year_full_date))

    three_digit_year_full_date = 'April, 147 A.D.'
    print(date_parser.parse_flexi_date(three_digit_year_full_date))

    century_date_string = '5th-century - 562'
    print(date_parser.parse_flexi_date(century_date_string))
    century_date_string = '5th-century'
    print(date_parser.parse_flexi_date(century_date_string))
    century_date_string = '562'
    print(date_parser.parse_flexi_date(century_date_string))

    date_year = '48 BC'
    print(date_parser.parse_flexi_date(date_year))

    unparseable_date = 'January 1642  24 May 1714---'
    date = date_parser.parse_flexi_date(unparseable_date)
    print(date)
    print(date.isoformat())
    print (date.qualifier)

    circa_date = 'c. 1714'
    date = date_parser.parse_flexi_date(circa_date)
    print(date)
    print(date.isoformat())

    circa_date = '1714'
    date = date_parser.parse_flexi_date(circa_date)
    # print(date.qualifier)