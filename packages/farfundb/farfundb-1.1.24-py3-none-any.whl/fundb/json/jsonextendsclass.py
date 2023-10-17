"""
https://extendsclass.com/json-storage.openapi.json
"""
import json

import requests


class JSONStorage:
    def __init__(self):
        self.base_url = "https://json.extendsclass.com"

    def request(self, bin_id, security_key=None):
        url = f"{self.base_url}/bin/{bin_id}"
        headers = {"Security-key": security_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def update(self, bin_id, data, security_key=None):
        url = f"{self.base_url}/bin/{bin_id}"
        headers = {"Security-key": security_key}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        return response.json()

    def delete(self, bin_id, security_key=None):
        url = f"{self.base_url}/bin/{bin_id}"
        headers = {"Security-key": security_key}
        response = requests.delete(url, headers=headers)
        return response.json()

    def create(self, api_key, data, security_key=None, private='false'):
        url = f"{self.base_url}/bin"
        headers = {"Api-key": api_key, "Security-key": security_key, "Private": private}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

    def all_bins(self, api_key):
        url = f"{self.base_url}/bins"
        headers = {
            "Api-key": api_key,
        }
        response = requests.get(url, headers=headers)
        return response.json()
