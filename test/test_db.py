from src.db import Db
from sqlalchemy import text


def test_db():
    test_db = Db()
    
    with test_db.engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        assert result.all()
    
