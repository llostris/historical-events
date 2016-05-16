from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.model import wiki_model as wiki_model


class BaseService:
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/historicaldb')
    wiki_model.Base.metadata.bind = engine
    session_maker = sessionmaker(bind=engine)

    def __init__(self, echo = False):
        wiki_model.Base.metadata.bind = self.engine
        self.engine.echo = echo