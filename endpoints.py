# endpoints.py

import falcon
import json
from falcon_cors import CORS


from jobs import user_search
from utils import records_to_json


cors = CORS(allow_origins_list=['https://mchaperc.github.io/web_search_frontend'])
public_cors = CORS(allow_all_origins=True)


class SearchResource(object):
    cors = public_cors
    def on_get(self, req, resp, search_query):
        """Handles GET requests"""
        search_results = user_search(search_query)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(records_to_json(search_results))
        print(resp.status, resp.body)


app = falcon.API(middleware=[cors.middleware])
search = SearchResource()


app.add_route('/search/{search_query}', search)