from .base_scraper import BaseScraper
from src.utils.requests_helper import RequestsHelper
from src.core.exceptions import ScrapingException
from src.models.job import Job, RemoteType, JobType
from datetime import datetime
from hashlib import md5
from src.utils.logger import get_logger
import json

logger = get_logger(__name__)


class CodemiteScraper(BaseScraper):
    BASE_URL = "https://codimitepvt.bamboohr.com/careers/"
    requests_helper = RequestsHelper()
    
    def generate_job_hash(self, job_data):
        job_id = job_data['id']
        source = "codimite"
        return md5(f"{job_id}{source}".encode()).hexdigest()
    
    def scrape_listings(self) -> list[Job]:
        res = self.requests_helper.get(self.BASE_URL + "list") 
        if not res:
            raise ScrapingException("Failed to fetch job listings")
        processed_res = self.process_listings(res)
        return processed_res
    

    def process_listings(self, raw_data):
        json_data = json.loads(raw_data)['result']

        processed_job_list: list[Job] = []        
        for job in json_data:
            job_details = self.requests_helper.get(self.BASE_URL+ job['id'] + "/detail")    
            if not job_details:
                raise ScrapingException("Failed to fetch job details")
            job_details = json.loads(job_details)['result']
            job_details['id'] = job['id']
            remote_status = None
            if job_details['jobOpening']['locationType'] == "2":
                remote_status = RemoteType.HYBRID
            elif job_details['jobOpening']['locationType'] == "0":
                remote_status = RemoteType.ONSITE
            elif job_details['jobOpening']['locationType'] == "1":
                remote_status = RemoteType.HYBRID
            logger.debug(f"Processing job: {job_details['jobOpening']['jobOpeningName']}")
            job_hash = self.generate_job_hash(job_details)
            logger.debug(f"Generated hash: {job_hash}")
            processed_job_list.append(
                Job(
                    job_hash= job_hash,
                    title=job_details['jobOpening']['jobOpeningName'],
                    description=job_details['jobOpening']['description'],
                    location=f"{job_details['jobOpening']['location']['city']}, {job_details['jobOpening']['location']['state']}, {job_details['jobOpening']['location']['addressCountry']}",
                    company="Codemite",
                    job_type=job_details['jobOpening']['employmentStatusLabel'],
                    is_remote=remote_status,
                    apply_url=job_details['jobOpening']['jobOpeningShareUrl'],
                    date_posted=datetime.fromisoformat(job_details['jobOpening']['datePosted']),
                    source=self.BASE_URL
                )
            )
        
        return processed_job_list

if __name__ == "__main__":
    scraper = CodemiteScraper()
    jobs = scraper.scrape_listings()
    for job in jobs:
        print(job.pretty_print())
