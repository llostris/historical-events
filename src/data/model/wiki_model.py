"""
Model for keeping wikipedia related classes in database - categories and articles.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


article_to_category_table = Table('ArticleToCategory', Base.metadata,
                                  Column('category_id', Integer, ForeignKey('Categories.id')),
                                  Column('article_id', Integer, ForeignKey('Articles.id'))
                                  )


class Category(Base) :
    __tablename__ = "Categories"

    id = Column(Integer, primary_key = True)
    category_id = Column(Integer)
    name = Column(String(255))
    articles = relationship("Article", secondary = article_to_category_table, back_populates = "categories")

    def __repr__(self) :
        return "<Category(category_id='{0}', name='{1}')>".format(self.category_id, self.name.encode('utf-8'))


class Article(Base) :
    __tablename__ = "Articles"

    id = Column(Integer, primary_key = True)
    pageid = Column(Integer)
    title = Column(String)
    content = Column(String)
    categories = relationship("Category", secondary = article_to_category_table, back_populates = "articles")

    def __repr__(self):
        return "<Article(pageid='{0}', title='{1}')>".format(self.pageid, self.title.encode('utf'))
