from basic_crawler import crawl_controller
from utils import execute_sql
from sql_queries import *

index = {}


def crawl_web(links):
    for link in links:
        crawl_controller(link, 0)
    write_index_to_db(index)


def write_index_to_db(data):
    write_keywords(data)
    # write_urls(data)


def write_keywords(data):
    keywords = [keyword for keyword in data]
    execute_sql(SQL_INSERT_KEYWORD_ROWS, keywords=keywords)


# def write_urls(data):
