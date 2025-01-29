import requests
from requests.exceptions import RequestException
from src.core.exceptions import ScrapingException
from src.utils.logger import logger

class RequestsHelper:
    def __init__(self, user_agent=None):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent
                or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
            }
        )

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            logger.error(f"GET failed: {e}")
            return None

    def post(self, url, data=None, json=None, **kwargs):
        try:
            response = self.session.post(url, data=data, json=json, **kwargs)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            logger.error(f"POST failed: {e}")
            return None

    def close(self):
        self.session.close()

