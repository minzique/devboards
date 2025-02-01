from datetime import datetime
from src.utils.logger import get_logger
from src.models.schemas import RemoteType, JobType
from src.services.scrapers.base_scraper import BaseScraper
from src.utils.requests_helper import RequestsHelper
from src.core.exceptions import ScrapingException
from src.models.db.job import Job
import json

logger = get_logger(__name__)

class ZebraScraper(BaseScraper):
    """Scraper for Zebra careers page"""
    
    BASE_URL = "https://careers.zebra.com/api/apply/v2/jobs"
    requests_helper = RequestsHelper()

    def scrape_listings(self) -> list[Job]:
        """Scrape job listings from Zebra careers API"""
        params = {
            'domain': 'zebra.com',
            'location': 'Colombo, WP, Sri Lanka'
        }

        res = self.requests_helper.get(self.BASE_URL, params=params)
        if not res:
            raise ScrapingException("Failed to fetch job listings")
        
        processed_res = self.process_listings(res)
        return processed_res

    def process_listings(self, job_data: str) -> list[Job]:
        """Process raw job listings into Job objects"""
        json_data = json.loads(job_data)['positions']
        processed_job_list: list[Job] = []

        for job in json_data:
            try:
                
                processed_job_list.append(
                    Job(
                        title=job['name'],
                        company='Zebra',
                        description=job['job_description'],
                        location=job['location'],
                        job_type=self._parse_job_type(job.get('work_location_option', 'onsite')),
                        is_remote=self._parse_remote_type(job.get('work_location_option') == 'remote'),
                        apply_url=job.get('canonicalPositionUrl', ''),
                        date_posted=datetime.fromtimestamp(job['t_create']),
                        source='zebra',
                        job_hash=self.generate_job_hash(job)
                    )
                )
            except Exception as e:
                logger.error(f"Error processing job {job.get('id')}: {str(e)}")
                continue

        return processed_job_list


    def _parse_job_type(self, work_location: str) -> str:
        """Convert work location to standard job type"""
        type_map = {
            'onsite': JobType.FULL_TIME,
            'remote': JobType.FULL_TIME,
            'hybrid': JobType.FULL_TIME
        }
        return type_map.get(work_location, JobType.FULL_TIME)

    def _parse_remote_type(self, is_remote: bool) -> str:
        """Convert remote status to standard remote type"""
        if is_remote:
            return RemoteType.REMOTE
        return RemoteType.ONSITE