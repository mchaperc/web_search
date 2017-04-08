# endpoints.py

import falcon
import json

from jobs import user_search
from utils import records_to_json

class SearchResource(object):
    def on_get(self, req, resp, search_query):
        """Handles GET requests"""
        search_results = user_search(search_query)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(records_to_json(search_results))


app = falcon.API()

search = SearchResource()

app.add_route('/search/{search_query}', search)