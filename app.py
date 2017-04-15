import schedule
import records

from jobs import crawl_web
from credentials import DB_URL
from constants import links

# schedule.every().minutes(5).do(crawl_web(links))

crawl_web(links)