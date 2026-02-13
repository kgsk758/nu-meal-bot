import requests
from config import constants
ScraperConfig = constants.ScraperConfig
class ScraperBase:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent":ScraperConfig.USER_AGENT
        })
    def _get(self, url):
        try:
            response = self.session.get(url, timeout=ScraperConfig.TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during GET {url}: {e}")
            return None
    def _post(self, url, data, params):
        try:
            response = self.session.post(url, data=data, params=params, timeout=ScraperConfig.TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during POST {url}: {e}")
            return None

