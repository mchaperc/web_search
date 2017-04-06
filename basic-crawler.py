import requests, string

from bs4 import BeautifulSoup

link1 = "https://news.ycombinator.com/"
link2 = "https://www.yahoo.com"
link3 = "http://stackexchange.com/"
link4 = "http://dmoztools.net/"
link5 = "https://twitter.com/"

index = {}

def union(arr1, arr2):
    for el in arr2:
        if el not in arr1:
            arr1.append(el)
    return arr1

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


def get_keywords(page):
    metas = page.find_all('meta')
    keywords = []
    for meta in metas:
        if meta.get('name') == 'keywords':
            keywords += split_string(meta.get('content'))
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
        url = to_crawl.pop()
        if url not in index:
            page = get_page(url)
            keywords = get_keywords(page)
            next_depth = union(next_depth, get_links(page, url))
            for word in keywords:
                if word not in index:
                    index[word] = [url]
                elif url not in index[word]:
                    index[word].append(url)
            if not to_crawl:
                print('going next level deep')
                to_crawl, next_depth = next_depth, []
                current_depth += 1

crawl_controller(link1, 1)
crawl_controller(link2, 1)
crawl_controller(link3, 1)
crawl_controller(link4, 1)
crawl_controller(link5, 1)