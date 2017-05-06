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
                result.append(str.lower(source[begin_index:end_index]))
                begin_index = end_index+1
            else:
                begin_index += 1
        elif len(source) == end_index+1:
            result.append(str.lower(source[begin_index:]))
        end_index += 1
    return result


def records_to_json(records, type='url'):
    body = []
    for record in records:
        body.append({'url': record.url, 'title': record.title, 'description': record.description})
    return body

def http_normalize_slashes(url):
    url = str(url)
    segments = url.split('/')
    correct_segments = []
    for segment in segments:
        if segment != '':
            correct_segments.append(segment)
    first_segment = str(correct_segments[0])
    if first_segment.find('http') == -1:
        correct_segments = ['http:'] + correct_segments
    correct_segments[0] = correct_segments[0] + '/'
    normalized_url = '/'.join(correct_segments)
    return normalized_url