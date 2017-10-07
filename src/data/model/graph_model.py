from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class UncertainDate(Base):
    __tablename__ = "uncertain_dates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    is_bc = Column(Boolean, default=False)
    is_circa = Column(Boolean, default=False)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    start_date_id = Column(Integer, ForeignKey('uncertain_dates.id'), nullable=True)
    # start_date = relationship("UncertainDate")
    end_date_id = Column(Integer, ForeignKey('uncertain_dates.id'), nullable=True)
    # end_date = relationship("UncertainDate")
    date_id = Column(Integer, ForeignKey('uncertain_dates.id'), nullable=True)
    # date = relationship("UncertainDate")
    wiki_id = Column(Integer, primary_key=True, unique=True)

    def __repr__(self):
        return "<Event(name='{0}')>".format(self.name)


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    edge_from = Column(Integer, ForeignKey('events.id'), nullable=False)
    edge_to = Column(Integer, ForeignKey('events.id'), nullable=False)
    count = Column(Integer, default=0, nullable=False)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # wiki_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'), unique=True)
    content = Column('content', LargeBinary)

