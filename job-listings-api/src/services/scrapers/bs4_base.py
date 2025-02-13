from abc import abstractmethod
from typing import List, Any
from bs4 import BeautifulSoup
import requests
from src.utils.logger import get_logger
from src.services.scrapers.base_scraper import BaseScraper
from src.models.job import Job

logger = get_logger(__name__)

class BaseBS4Scraper(BaseScraper):
    """Base class for BS4-based scrapers"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_soup(self, url: str) -> BeautifulSoup:
        """Get BeautifulSoup object for given URL"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def fetch_url(self, url: str) -> str:
        """Fetch raw content from URL"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    @abstractmethod
    def scrape_listings(self) -> List[Job]:
        """Implement scraping logic"""
        pass
