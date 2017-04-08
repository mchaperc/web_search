import records

from credentials import DB_URL

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


def split_string(source, splitlist=' ,;?\n&'):
    result = []
    begin_index = 0
    end_index = 0
    for char in source:
        if char in splitlist:
            if end_index - begin_index > 0:
                result.append(source[begin_index:end_index])
                begin_index = end_index+1
            else:
                begin_index += 1
        elif len(source) == end_index+1:
            result.append(source[begin_index:])
        end_index += 1
    return result


def records_to_json(records, type='url'):
    body = []
    for record in records:
        body.append({'url': record.url})
    return body