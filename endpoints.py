# endpoints.py

import falcon
import json
from falcon_cors import CORS


from jobs import user_search, get_page_count
from utils import records_to_json, split_string


cors = CORS(allow_origins_list=['https://mchaperc.github.io/web_search_frontend'])
public_cors = CORS(allow_all_origins=True)


class SearchResource(object):
    cors = public_cors
    def on_get(self, req, resp, search_query, page_number):
        """Handles GET requests"""
        if search_query:
            search_query = split_string(search_query)
        search_results = user_search(search_query, page_number)
        results_package = {
            # 'pages': get_page_count(search_query),
            'search_results': records_to_json(search_results),
        }
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(results_package)
        print(resp.status, resp.body)


app = falcon.API(middleware=[cors.middleware])
search = SearchResource()


app.add_route('/search/{search_query}/{page_number}/', search)