import json
import requests
import logging


class InsightAppSec:
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.api_key = kwargs.get("api_key")
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
        self.modules = {}

    def search(self, search_type, query, sort):
        url = self.url + "/search" + sort
        headers = self.headers
        body = {
            "type": search_type,
            "query": query
        }
        cont = True
        results = []

        try:
            while cont:
                response = requests.post(url=url, headers=headers, data=json.dumps(body))
                response.raise_for_status()

                response_dict = response.json()
                results.extend(response_dict.get("data"))

                if len(results) >= response_dict.get("metadata").get("total_data"):
                    cont = False
                else:
                    for link in response_dict.get("links"):
                        if link.get("rel") == "next":
                            url = link.get("href")
                            break
                del response
            return results
        except Exception as e:
            logging.error("Error in InsightAppSec API: Search", e)

    def get_module(self, module_id):
        url = self.url + "/modules/" + module_id
        headers = self.headers

        try:
            if module_id in self.modules:
                logging.info(f"Retrieving module from cache: {module_id}")
                return self.modules[module_id]["details"]

            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            module = response.json()
            self.modules[module_id] = {"details": module}
            logging.info(f"Added module to cache: {module_id}")
            return module
        except Exception as e:
            logging.error("Error in InsightAppSec API: Get Module", e)
