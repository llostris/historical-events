from sqlalchemy import create_engine

from data.model import graph_model

if __name__ == "__main__":
    # engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/historicaldb')
    # connection = engine.connect()
    # wiki_model.Base.metadata.create_all(engine)

    engine = create_engine('mysql+pymysql://historical:@localhost/historical_events', pool_recycle=3600)
    connection = engine.connect()

    graph_model.Base.metadata.create_all(engine)
