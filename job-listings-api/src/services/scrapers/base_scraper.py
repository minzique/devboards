from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.db.company import CompanyModel
from sqlalchemy.orm import Session
from src.models.job import Job
from hashlib import md5

class BaseScraper(ABC):
    """Abstract base class for job scrapers"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_company_info(self, company_slug: str) -> CompanyModel:
        """Get company info from database"""
        return self.db.query(CompanyModel).filter(CompanyModel.slug == company_slug).first()

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