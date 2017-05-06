from basic_crawler import crawl_controller
from utils import execute_sql, get_one, get_many
from sql_queries import *

index = {}


def crawl_web(links):
    for link in links:
        crawl_controller(link, 3)
    write_index_to_db(index)


def write_index_to_db(data):
    execute_sql(SQL_DROP_TABLES)
    execute_sql(SQL_ADD_KEYWORD_TABLE)
    execute_sql(SQL_ADD_URL_TABLE)
    execute_sql(SQL_ADD_URL_META_TABLE)
    write_keywords(data)
    keywords = get_many(SQL_GET_KEYWORDS)
    write_urls(keywords, data)
    urls = get_many(SQL_GET_URLS)
    write_url_meta(urls, data)


def write_keywords(data):
    keywords = [keyword.replace('\x00', '') for keyword in data]
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


def write_url_meta(urls, data):
    url_ids = []
    titles = []
    descriptions = []
    for url in urls:
        if url.url_text in data:
            url_ids.append(url.id)
            try:
                titles.append(data[url.url_text]['title'])
            except:
                titles.append(url.url_text)
            try:
                descriptions.append(data[url.url_text]['description'])
            except:
                descriptions.append(url.url_text)
    execute_sql(SQL_INSERT_URL_META, url_ids=url_ids, titles=titles, descriptions=descriptions)


def user_search(search_query='', page_number=1):
    if search_query:
        return get_many(SQL_GET_URLS_FROM_KEYWORDS, search_query=tuple(search_query), page_number=page_number)
    return get_many(SQL_GET_URLS_WITHOUT_KEYWORDS)


def get_page_count(search_query=''):
    return get_one(SQL_GET_PAGE_COUNT, search_query=search_query)

