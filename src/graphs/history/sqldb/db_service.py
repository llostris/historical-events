from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tools.sqldb import model


class BaseService:
    engine = create_engine('mysql+pymysql://historical:@localhost/historical_events?charset=utf8mb4&use_unicode=True',
                           pool_recycle=3600)
    model.Base.metadata.bind = engine
    session_maker = sessionmaker(bind=engine)

    def __init__(self, echo=False):
        model.Base.metadata.bind = self.engine
        self.engine.echo = echo


if __name__ == "__main__":

    base_service = BaseService()
    model.Base.metadata.create_all(base_service.engine)
