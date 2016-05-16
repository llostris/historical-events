from sqlalchemy import create_engine

import data.model.wiki_model as wiki_model

if __name__ == "__main__":
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/historicaldb')
    connection = engine.connect()
    wiki_model.Base.metadata.create_all(engine)