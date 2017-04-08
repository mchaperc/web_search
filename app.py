import schedule
import records

from jobs import crawl_web
from credentials import DB_URL
from constants import links

# schedule.every().weeks(4).do(crawl_web(links)

# db = records.Database(DB_URL)
#
# rows = db.query("SELECT * FROM keyword")
# for row in rows:
#     print(row)

crawl_web(links)