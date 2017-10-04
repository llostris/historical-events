import re

from graph.dataextraction.base_extractor import BaseDateExtractor
from graph.dataextraction.date_parser import DateParser


TEMPLATE_START_DATE_REGEXPS = {
    'start date': re.compile(r"{{start date\|[^}]*}}"),
    'birth date': re.compile(r"{{birth date[^\|]*\|[^}]*}}"),
    'bda': re.compile(r"{{bda[^\|]*\|[^}]*}}"),
}
TEMPLATE_END_DATE_REGEXPS = {
    'end date': re.compile(r"{{end date\|[^\}]*\}\}"),
    'death date': re.compile(r"{{death date[^\|]*\|[^\}]*\}\}"),
    'death date and age':re.compile(r"{{death date and age\|[^}]*}}"),
}


class TemplateDateExtractorMixin(BaseDateExtractor):

    def extract_date_from_templates(self, node, templates):
        date = None

        for key, regexp in templates.items():
            if key in node:
                date = self.extract_date_from_template(key, regexp, node)

            if self.is_filled_and_valid(date):
                return date

    def extract_start_date_from_templates(self, node_lowered):
        self.start_date = self.extract_date_from_templates(node_lowered, TEMPLATE_START_DATE_REGEXPS)

    def extract_end_date_from_templates(self, node_lowered):
        self.end_date = self.extract_date_from_templates(node_lowered, TEMPLATE_END_DATE_REGEXPS)

    def extract_date_from_template(self, date_tag, regexp, content):
        lowered = content.lower()
        lowered = self.preprocess_node_str(lowered)
        if '{{{0}'.format(date_tag) in lowered:
            result = regexp.findall(lowered)

            for match in result:
                print(match)
                without_braces = match[2:-2]
                splitted = without_braces.split("|")

                removables = ["df=y", "df=yes", "df=n", "df=no"]
                for tag in removables:
                    if tag in splitted:
                        splitted.remove(tag)

                str_date = ' '.join(splitted[1:4])  # skip type tag

                return DateParser().parse_flexi_date(str_date, dayfirst=False)

