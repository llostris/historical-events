from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.model import graph_model


class BaseService:
    engine = create_engine('mysql+pymysql://historical:@localhost/historical_events?charset=utf8mb4&use_unicode=True',
                           pool_recycle=3600)
    graph_model.Base.metadata.bind = engine
    session_maker = sessionmaker(bind=engine)

    def __init__(self, echo=False):
        graph_model.Base.metadata.bind = self.engine
        self.engine.echo = echo
