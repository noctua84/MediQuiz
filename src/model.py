import datetime

from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Question(Base):
    pass


class Stats(Base):
    pass


def init_orm(engine):
    Base.metadata.create_all(engine)
