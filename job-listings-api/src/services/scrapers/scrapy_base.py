from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from src.models.job import Job
from src.utils.logger import get_logger
from src.services.scrapers.base_scraper import BaseScraper
from sqlalchemy.orm import Session

logger = get_logger(__name__)

class BaseSpider(Spider):
    """Base Spider class with common configuration"""
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 10,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        # 'DOWNLOAD_DELAY': 1,

    }

    def handle_error(self, failure):
        logger.error(f"Scraping failed: {failure.value}")

class BaseScrapyScraper(BaseScraper):
    """Base class for Scrapy-based scrapers"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs = []
        self.spider_class: Optional[BaseSpider] = None
        dispatcher.connect(self.collect_results, signal=signals.item_scraped)

    def collect_results(self, item, response, spider):
        """Collect results via Scrapy signals"""
        self.jobs.append(item)

    def get_spider_settings(self) -> dict:
        """Override to customize spider settings"""
        return {
            'LOG_ENABLED': False
        }

    def scrape_listings(self) -> List[Job]:
        if not self.spider_class:
            raise NotImplementedError("spider_class must be set")
            
        process = CrawlerProcess(settings=self.get_spider_settings())
        process.crawl(self.spider_class)
        process.start(stop_after_crawl=True)
        
        return self.process_listings(self.jobs)