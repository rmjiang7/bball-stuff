import requests
import time
import sys
import json
import pandas as pd
import argparse
import pathlib
import os.path
import abc

class Client(object):

    def __init__(self):
        # Create the API request, spoof the header as necessary
        self.headers = {
            'Host': 'stats.nba.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-NewRelic-ID': 'VQECWF5UChAHUlNTBwgBVw==',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true',
            'Connection': 'keep-alive',
            'Referer': 'https://stats.nba.com/players/catch-shoot/',
            'Cache-Control': 'max-age=0, no-cache',
            'Pragma': 'no-cache'
        }

    def make_request(self, endpoint):
        url, params = endpoint.build_request()
        resp = requests.get(url, headers = self.headers, params = params)
        json_response = json.loads(resp.text)
        return endpoint.format_response(json_response)

class Endpoint(object):

    @abc.abstractmethod
    def build_request(self):
        """
        Builds the base url and the parameters for a requests Client.

        Returns
        ---------
        base_url : string
            Non-parameterized string of the base url
        params : dict[string : string]
            Parameters to pass with the base url
        """
        raise NotImplementedException

    @abc.abstractmethod
    def format_response(self, json_response):
        """
        Format the JSON response returned from the endpoint.

        Parameters
        ----------
        json_response : json.JSON
            JSON object of the response, error handling not implemented yet
        """
        raise NotImplementedException
