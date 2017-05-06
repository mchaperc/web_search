import requests, string
import jobs
import re

from utils import split_string, http_normalize_slashes

from bs4 import BeautifulSoup


def union(arr1, arr2):
    for el in arr2:
        if el not in arr1:
            arr1.append(el)
    return arr1


def get_keywords(page, current_url=''):
    metas = page.find_all('meta')
    keywords = []
    for meta in metas:
        if meta.get('name') == 'keywords':
            keywords += split_string(meta.get('content'))
        elif meta.get('name') == 'description':
            set_page_description(meta.get('content'), current_url)
    for elem in page.findAll(['script', 'style']):
        elem.extract()
    page = page.getText(separator=u' ').translate({ord(c): None for c in string.punctuation})
    keywords += split_string(page)
    return keywords


def get_links(page, current_url):
    links = page.find_all('a', href=True)
    result = []
    for link in links:
        if link.get('href').find('javascript') < 0:
            if link.get('href').find('http') < 0:
                result.append(current_url + '/' + link.get('href'))
            else:
                result.append(link.get('href'))
    return result


def get_page_title(page):
    try:
        return page.title.string.strip()
    except:
        return ''


def set_page_description(description, url):
    if len(description) > 135:
        jobs.index[url]['description'] = description[:135] + '...'
        return
    jobs.index[url]['description'] = description


def get_page(url):
    page_as_string = ''
    try:
        result = requests.get(url, allow_redirects=False, timeout=2)
        page_as_string = result.text
    except requests.exceptions.Timeout as err:
        print(err)
    except requests.exceptions.ConnectionError as err:
        print(err)
    except requests.exceptions.MissingSchema as err:
        print(err)
    except requests.exceptions.InvalidSchema as err:
        print(err)
    return BeautifulSoup(page_as_string, 'html.parser')


def crawl_controller(seed, max_depth=1):
    to_crawl = [seed]
    next_depth = []
    current_depth = 0
    while len(to_crawl) and current_depth <= max_depth:
        url = http_normalize_slashes(to_crawl.pop())
        if url not in jobs.index:
            page = get_page(url)
            next_depth = union(next_depth, get_links(page, url))
            jobs.index[url] = {
                'title': get_page_title(page),
            }
            keywords = get_keywords(page, url)
            for word in keywords:
                if word not in jobs.index:
                    jobs.index[word] = [url]
                elif url not in jobs.index[word]:
                    jobs.index[word].append(url)
            if not to_crawl:
                to_crawl, next_depth = next_depth, []
                current_depth += 1
                print('===========')
                print(current_depth)
                print(url)
            print('============')
            print(url)