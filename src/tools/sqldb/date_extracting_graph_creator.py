import logging

from sqlalchemy.orm import Session

from tools.category_matcher import CategoryMatcher
from tools.data_extraction.date_extractor import DateExtractor
from tools.graph_creator import GraphCreator
from tools.sqldb.model import Event, Article, UncertainDate


class DateExtractingGraphCreator(GraphCreator):

    def __init__(self, data_dir: str, category_matcher: CategoryMatcher):
        super().__init__(data_dir, category_matcher)
        self.session = Session()

    def extract_attributes(self, article):
        date_extractor = DateExtractor(article.title, article.content)
        date_extractor.fill_dates()
        date_extractor.validate_dates()  # remove invalid dates

        attributes = {
            'start_date': date_extractor.start_date,
            'end_date': date_extractor.end_date,
            'date': date_extractor.date
        }

        if self.session:
            self.save_event_in_db(article.title, attributes, article.pageid, article.content)

        return attributes

    def save_event_in_db(self, name, attributes, page_id, article_content):
        event = Event(name=name, wiki_id=page_id)

        start_date = self.save_date_in_db(attributes['start_date'])
        if start_date is not None:
            event.start_date_id = start_date.id

        end_date = self.save_date_in_db(attributes['end_date'])
        if end_date is not None:
            event.end_date_id = end_date.id

        date = self.save_date_in_db(attributes['date'])
        if date is not None:
            event.date_id = date.id

        self.session.add(event)
        self.session.commit()

        article = Article(content=article_content, event_id=event.id)
        self.session.add(article)
        try:
            self.session.commit()
        except Exception as e:
            logging.error(e)
            logging.error("Could not save article {} content: {}".format(name, article_content))
            self.session.rollback()

    def save_date_in_db(self, flexi_date):
        if flexi_date is None:
            return None
        if DateExtractor.is_unparsed(flexi_date):
            return None

        year = self.get_int_from_value(flexi_date.year)
        month = self.get_int_from_value(flexi_date.month)
        day = self.get_int_from_value(flexi_date.day)
        is_bc = year < 0 if year is not None else False
        circa = 'circa' in flexi_date.qualifier

        date = UncertainDate(year=year, month=month, day=day, is_bc=is_bc, is_circa=circa)
        self.session.add(date)
        self.session.commit()
        return date

    @staticmethod
    def get_int_from_value(value):
        if isinstance(value, str) and value != '':
            try:
                return int(value)
            except ValueError as e:
                logging.error(e)
                return None
        else:
            return None
