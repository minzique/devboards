import json
from datetime import datetime
from src.models.db.job import Job
from src.utils.logger import get_logger
from src.models.schemas import RemoteType, JobType
from src.services.scrapers.base_scraper import BaseScraper
from src.utils.requests_helper import RequestsHelper
from src.core.exceptions import ScrapingException
from hashlib import md5

logger = get_logger(__name__)

class RootcodeScraper(BaseScraper):
    """Scraper for Rootcode careers page"""
    
    BASE_URL = "https://rootcode.io/api/jobs"
    requests_helper = RequestsHelper()
    def scrape_listings(self) -> list[Job]:

        res = self.requests_helper.get(self.BASE_URL)
        if not res:
            raise ScrapingException("Failed to fetch job listings")
        processed_res = self.process_listings(res)
        return processed_res


    def process_listings(self, job_data: dict) -> Job:
        json_data = json.loads(job_data)['results']
        processed_job_list: list[Job] = []
        
        for job in json_data:
            url_slug = job['position_name'].replace(' ', '-').lower() + str(job['id'])
            processed_job_list.append(
            Job(
                title=job['position_name'],
                company='Rootcode',
                description=job['description'],
                location=job['location_display'],
                job_type=self._parse_job_type(job['contract_details']),
                is_remote=self._parse_remote_type(job['is_remote']),
                apply_url=f"https://rootcode.io/careers/{url_slug}/",
                date_posted=datetime.now(),
                source='rootcode',
                job_hash=self.generate_job_hash(job)
            ))
        return processed_job_list

    def generate_job_hash(self, job_data: dict) -> str:
        return md5(f"{job_data['hash']}".encode()).hexdigest()

    def _parse_job_type(self, contract_details: str) -> str:
        """Convert contract details to standardized job type"""
        contract_map = {
            'full_time': JobType.FULL_TIME,
            'part_time': JobType.PART_TIME,
            'internship': JobType.INTERNSHIP,
            'contract': JobType.CONTRACT
        }
        return contract_map.get(contract_details, JobType.FULL_TIME)


    def _parse_remote_type(self, is_remote: bool) -> str:
        """Convert remote status to standardized remote type"""
        if is_remote is True:
            return RemoteType.REMOTE
        elif is_remote is False:
            return RemoteType.ONSITE
        return RemoteType.ONSITE  # Default
        
