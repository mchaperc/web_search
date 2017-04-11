import schedule
import records

from jobs import crawl_web
from credentials import DB_URL
from constants import links

schedule.every().weeks(4).do(crawl_web(links))