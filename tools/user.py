#!/usr/bin/env python
from sqlalchemy import create_engine,Column, Integer, String,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy



from sqlalchemy import Sequence
Base = declarative_base()
class Factor(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

class dateMon(Base):
    __tablename__ = 'month'
    id = Column(DateTime, primary_key=True)
    date = Column(DateTime)
    def __repr__(self):
        return "<User(name='%s')>" % (self.date)

class report(Base):
    __tablename__ = 'report'
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))
    title = Column(String(200))
    date = Column(String(50))
    classes = Column(String(50))
    author = Column(String(50))
    score = Column(String(50))
    pages = Column(Integer)


class factor(Base):
