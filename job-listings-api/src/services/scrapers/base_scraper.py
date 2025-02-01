from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.job import Job
from hashlib import md5

class BaseScraper(ABC):
    """Abstract base class for job scrapers"""
    
    @abstractmethod
    def scrape_listings(self) -> List[Job]:
        """Fetch job listings from source
        Returns:
            List[Job]: List of scraped job listings
        """
        pass

    @abstractmethod
    def process_listings(self, raw_data: Any) -> List[Job]:
        """Process raw data into Job objects
        Args:
            raw_data: Raw data from scraping
        Returns:
            List[Job]: List of processed Job objects
        """
        pass
    
    def generate_job_hash(self, job_data: Dict) -> str:
        """Generate a consistent hash for a job listing
        Args:
            job_data: Dictionary containing job details
        Returns:
            str: MD5 hash of job details
        """
        hash_string = (
            f"{job_data.get('title', '')}"
            f"{job_data.get('company', '')}"
            f"{job_data.get('url', '')}"
            f"{job_data.get('location', '')}"
        )
        return md5(hash_string.encode()).hexdigest()