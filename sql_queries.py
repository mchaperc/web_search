# In place of a better update of existing tables on each iteration of job to crawl web
SQL_DROP_TABLES = """
    DROP TABLE keyword, url
"""

SQL_ADD_KEYWORD_TABLE = """
    CREATE TABLE keyword(
      id SERIAL PRIMARY KEY UNIQUE NOT NULL,
      keyword_text VARCHAR(255) NOT NULL
    )
"""

SQL_ADD_URL_TABLE = """
    CREATE TABLE url(
      id SERIAL PRIMARY KEY UNIQUE NOT NULL,
      keyword_id INT NOT NULL,
      url_text VARCHAR(255) NOT NULL
    )
"""

SQL_INSERT_KEYWORD_ROWS = """
    INSERT INTO keyword (keyword_text) VALUES
      (unnest(array[:keywords]))
"""

SQL_INSERT_URL_ROWS = """
    INSERT INTO url (keyword_id, url_text) VALUES
      (unnest(array[:keyword_ids]), (unnest(array[:urls_text])))
"""

SQL_GET_KEYWORDS = """
    SELECT
      keyword.id as id,
      keyword.keyword_text as text
    FROM
      keyword
"""