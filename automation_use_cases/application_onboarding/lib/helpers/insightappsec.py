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

    def create_app(self, body):
        url = self.url + "/apps"
        headers = self.headers

        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            app_id = self.get_url_id(response.headers.get("location"))
            logging.info(f"Created new application: {app_id}")
            return app_id
        except Exception as e:
            logging.error("Error in InsightAppSec API: Create App", e)
            raise e

    def create_scan_config(self, body):
        url = self.url + "/scan-configs"
        headers = self.headers

        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            scan_config_id = self.get_url_id(response.headers.get("location"))
            logging.info(f"Created new scan config: {scan_config_id}")
            return scan_config_id
        except Exception as e:
            logging.error("Error in InsightAppSec API: Create Scan Config", e)
            raise e

    def create_target(self, body):
        url = self.url + "/targets"
        headers = self.headers

        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            target_id = self.get_url_id(response.headers.get("location"))
            logging.info(f"Created new target: {target_id}")
            return target_id
        except Exception as e:
            logging.error("Error in InsightAppSec API: Create Target", e)
            raise e

    def update_scan_config_options(self, scan_config_id, body):
        url = self.url + "/scan-configs/" + scan_config_id + "/options"
        headers = self.headers

        try:
            response = requests.put(url=url, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            logging.info(f"Updated scan config options: {scan_config_id}")
            return scan_config_id
        except Exception as e:
            logging.error("Error in InsightAppSec API: Update Scan Config Options", e)
            raise e

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
            logging.error("Error in InsightAppSec API: Submit Scan", e)
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
