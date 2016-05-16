from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Date
from sqlalchemy.orm import relationship

Base = declarative_base()


class Vertex(Base):
    __tablename__ = "Vertex"
    id = Column(Integer, primary_key = True)
    name = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    date = Column(Date)

    def __repr__(self):
        return "<Vertex(name='{0}')>".format(self.name)


class Edge(Base):
    __tablename__ = "Edge"
    id = Column(Integer, primary_key = True)
    vertex1 = Column('vertex1', Integer, ForeignKey('Vertex.id'))
    vertex2 = Column('vertex2', Integer, ForeignKey('Vertex.id'))
