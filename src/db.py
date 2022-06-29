import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from src.model import Question, Stats


class Db:
    def __init__(self):
        self.path = os.getcwd()
        self.engine = create_engine(f"sqlite+pysqlite:///{self.path}/quiz.sqlite3", echo=False, future=True)
        self.session = (sessionmaker(bind=self.engine))()
        
    def get_questions(self):
        return [question.Question for question in self.session.execute(select(Question))]
    
    def save_question(self, question: Question):
        with Session(self.engine) as session:
            session.add(question)
            session.commit()
            
    def save_stats(self, question: Question, answered: bool, session_id: str):
        cur_stats = Stats()
        cur_stats.answered = answered
        cur_stats.question_id = question.id
        cur_stats.session_id = session_id
        
        self.session.add(cur_stats)
        self.session.commit()
        
    def delete_question(self, q_id: int):
        with Session(self.engine) as session:
            q = session.get(Question, q_id)
            session.delete(q)
            session.commit()
            
