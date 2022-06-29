from src.db import Db
from sqlalchemy import text


def test_db():
    db_test = Db()
    
    with db_test.engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        assert result.all()


def test_get_questions():
    assert False


def test_save_question():
    assert False


def test_save_stats():
    assert False
