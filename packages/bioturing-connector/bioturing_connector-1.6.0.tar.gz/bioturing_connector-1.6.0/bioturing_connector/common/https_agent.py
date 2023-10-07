"""A python class for performing HTTPS requests (GET, POST)"""

import requests


class HttpsAgent:
  """Wrapper class of requests"""
  def __init__(self, token: str, ssl: bool):
    self.__token = token
    self.__ssl = ssl


  def get(self, url: str, params: dict = None):
    """Perform GET request

      Args:
        url:
          An API endpoint
          Example: https://bioturing.com/api
        params:
          Params of the GET requests, will be encoded to URL's query string
          Example: {"param1": 0, "param2": true}
    """
    if params is None:
      params = {}

    try:
      res = requests.get(
        url=url,
        params=params,
        headers={'bioturing-api-token': self.__token},
        timeout=30000,
        verify=self.__ssl
      )
      return res.json()
    except requests.exceptions.RequestException as e:
      print(e)


  def post(self, url: str, body: dict = None):
    """
    Perform POST request

    Args:
      url:
        An API endpoint
        Example: https://bioturing.com/api

      body:
        Body of the request
        Example: {"param1": 0, "param2": true}
    """
    if body is None:
      body = {}

    try:
      res = requests.post(
        url=url,
        json=body,
        headers={'bioturing-api-token': self.__token},
        timeout=30,
        verify=self.__ssl
      )
      return res.json()
    except requests.exceptions.RequestException as e:
      print(e)
