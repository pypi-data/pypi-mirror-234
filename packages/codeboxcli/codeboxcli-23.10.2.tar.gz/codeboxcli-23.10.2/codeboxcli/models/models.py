# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Snippet(Base):
    __tablename__ = 'snippets'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100))
    tags = Column(String(400))
    content = Column(String(1000))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.datetime.utcnow)
