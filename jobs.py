from basic_crawler import crawl_controller
from utils import execute_sql, get_many, split_string
from sql_queries import *

index = {}


def crawl_web(links):
    for link in links:
        crawl_controller(link, 0)
    write_index_to_db(index)


def write_index_to_db(data):
    execute_sql(SQL_DROP_TABLES)
    execute_sql(SQL_ADD_KEYWORD_TABLE)
    execute_sql(SQL_ADD_URL_TABLE)
    write_keywords(data)
    keywords = get_many(SQL_GET_KEYWORDS)
    write_urls(keywords, data)


def write_keywords(data):
    keywords = [keyword for keyword in data]
    execute_sql(SQL_INSERT_KEYWORD_ROWS, keywords=keywords)


def write_urls(keywords, data):
    keyword_ids = []
    urls = []
    for keyword in keywords:
        if keyword.text in data:
            for url in data[keyword.text]:
                keyword_ids.append(keyword.id)
                urls.append(url)
    execute_sql(SQL_INSERT_URL_ROWS, keyword_ids=keyword_ids, urls_text=urls)


def user_search(search_query=''):
    if search_query:
        search_query = split_string(search_query)
        return get_many(SQL_GET_URLS_FROM_KEYWORDS, search_query=tuple(search_query))
    return get_many(SQL_GET_URLS_WITHOUT_KEYWORDS)