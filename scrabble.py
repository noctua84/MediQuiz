import os

from src.db import Db
from src.model import init_orm

db = Db()

list_of_questions = db.get_questions()

for i in range(0, len(list_of_questions)):
    print(list_of_questions[0])
    print(i)
    print(list_of_questions[0].question_text)
    list_of_questions.pop(0)
    
    print(list_of_questions)
    print(i)
    
