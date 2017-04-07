import records

from constants import DB_URL

db = records.Database(DB_URL)

def get_one(SQL, **kwargs):
    rows = db.query(SQL, fetchall=True, **kwargs)
    if len(rows) == 0:
        return {}
    if len(rows) > 1:
        raise ValueError("Query returned multiple rows")
    return rows[0]


def get_many(SQL, **kwargs):
    rows = db.query(SQL, fetchall=True, **kwargs)
    return rows


def execute_sql(SQL, **kwargs):
    db.query(SQL, **kwargs)