import datetime

from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    section = Column(Integer, nullable=False)
    stats = relationship("Stats")
    
    created_at = Column(DateTime, default=datetime.date.today())


class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="SET NULL"), nullable=True)
    answered = Column(Boolean, nullable=False)
    session_id = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, default=datetime.date.today())


def init_orm(engine):
    Base.metadata.create_all(engine)