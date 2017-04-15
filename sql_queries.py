# In place of a better update of existing tables on each iteration of job to crawl web
SQL_DROP_TABLES = """
    DROP TABLE keyword, url, url_meta
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

SQL_ADD_URL_META_TABLE = """
    CREATE TABLE url_meta(
      id SERIAL PRIMARY KEY UNIQUE NOT NULL,
      url_id INT NOT NULL,
      title VARCHAR(100),
      description VARCHAR(138)
    )
"""

SQL_INSERT_KEYWORD_ROWS = """
    INSERT INTO keyword (keyword_text) VALUES
      (unnest(array[:keywords]))
"""

SQL_INSERT_URL_ROWS = """
    INSERT INTO url (keyword_id, url_text) VALUES
      (unnest(array[:keyword_ids]), unnest(array[:urls_text]))
"""

SQL_INSERT_URL_META = """
    INSERT INTO url_meta (url_id, title, description) VALUES
      (unnest(array[:url_ids]), unnest(array[:titles]), unnest(array[:descriptions]))
"""

SQL_GET_URLS_FROM_KEYWORDS = """
    SELECT
      url.url_text AS url,
      url_meta.title AS title,
      url_meta.description AS description
    FROM
      keyword,
      url,
      url_meta
    WHERE
      keyword.keyword_text IN :search_query
      AND url.keyword_id = keyword.id
      AND url.id = url_meta.url_id
"""

SQL_GET_URLS_WITHOUT_KEYWORDS = """
    SELECT
      url.url_text AS url,
      url_meta.title AS title,
      url_meta.description AS description
    FROM
      url,
      url_meta
    WHERE
      url.id = url_meta.url_id
"""

SQL_GET_KEYWORDS = """
    SELECT
      keyword.id AS id,
      keyword.keyword_text as text
    FROM
      keyword
"""

SQL_GET_URLS = """
    SELECT
      url.id AS id,
      url.url_text as url_text
    FROM
      url
"""