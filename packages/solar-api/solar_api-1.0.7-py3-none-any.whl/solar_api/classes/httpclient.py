import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class HttpClient:
    """Client for handling requests to Tonic instance

    Parameters
    ----------
    base_url : str
        URL to Tonic instance
    api_key : str
        The API token associated with your workspace
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": api_key, "User-Agent": "solar-api-python-sdk"}

    def http_get(self, url: str, session: requests.Session, params: dict={}):
        """Make a get request.

        Parameters
        ----------
        url : str
            URL to make get request. Is appended to self.base_url.
        params: dict
            Passed as the params parameter of the requests.get request.

        """
        res = session.get(self.base_url + url, params=params, headers=self.headers, verify=False,)
        res.raise_for_status()
        return res.json()

    def http_post(self, url, params={}, data={}, files={}):
        """Make a post request.

        Parameters
        ----------
        url : str
            URL to make the post request. Is appended to self.base_url.
        params: dict
            Passed as the params parameter of the requests.post request.
        data: dict
            Passed as the data parameter of the requests.post request.
        """
        res = requests.post(
            self.base_url + url, params=params, json=data, headers=self.headers, verify=False, files=files
        )
        res.raise_for_status()
        return res.json()

    def http_put(self, url, params={}, data={}, files={}):
        """Make a out request.

        Parameters
        ----------
        url : str
            URL to make the post request. Is appended to self.base_url.
        params: dict
            Passed as the params parameter of the requests.post request.
        data: dict
            Passed as the data parameter of the requests.post request.
        """
        res = requests.put(
            self.base_url + url, params=params, json=data, headers=self.headers, verify=False
        )
        res.raise_for_status()
        return res.json()

    def http_delete(self, url, params={}):
        res = requests.delete(self.base_url + url, params = params, headers = self.headers, verify = False)
        res.raise_for_status()
        return res.json()