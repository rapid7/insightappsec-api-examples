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

    def submit_scan(self, body):
        url = self.url + "/scans"
        headers = self.headers
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            scan_id = self.get_url_id(response.headers.get("location"))
            logging.info(f"Launched new scan: {scan_id}")
            return scan_id
        except Exception as e:
            logging.error(f"Error in InsightAppSec API: Submit Scan\n{e}")
            raise e

    def get_scan(self, scan_id):
        url = self.url + "/scans/" + scan_id
        headers = self.headers

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            scan = response.json()
            return scan
        except Exception as e:
            logging.error("Error in InsightAppSec API: Get Scan", e)
            raise e

    def search(self, search_type, query):
        url = self.url + "/search"
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
            raise e

    def get_url_id(self, url):
        url_split = url.split("/")
        resource_id = url_split[-1]
        return resource_id
