import os

from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session


class Db:
    def __init__(self):
        self.path = os.getcwd()
        self.engine = create_engine(f"sqlite+pysqlite:///{self.path}/quiz.sqlite3", echo=False, future=True)
