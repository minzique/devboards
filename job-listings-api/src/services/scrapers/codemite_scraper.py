from .base_scraper import BaseScraper
from src.utils.requests_helper import RequestsHelper
from src.core.exceptions import ScrapingException
from src.models.job import Job
from datetime import datetime
import json 

class CodemiteScraper(BaseScraper):
    BASE_URL = "https://codimitepvt.bamboohr.com/careers/"
    requests_helper = RequestsHelper()
    
    def scrape_listings(self):
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
            job = json.loads(job_details)['result']

            remote_status = None
            if job['jobOpening']['locationType'] == "2":
                remote_status = "hybrid"
            elif job['jobOpening']['locationType'] == "0":
                remote_status = "in-office"
            elif job['jobOpening']['locationType'] == "1":
                remote_status = "remote"


            processed_job_list.append(
                Job(
                    title=job['jobOpening']['jobOpeningName'],
                    description=job['jobOpening']['description'],
                    location=f"{job['jobOpening']['location']['city']}, {job['jobOpening']['location']['state']}, {job['jobOpening']['location']['addressCountry']}",
                    company="Codemite",
                    job_type=job['jobOpening']['employmentStatusLabel'],
                    remote_status=remote_status,
                    apply_url=job['jobOpening']['jobOpeningShareUrl'],
                    date_posted=datetime.fromisoformat(job['jobOpening']['datePosted']),
                    source=self.BASE_URL
                )
            )
        
            
        return processed_job_list

if __name__ == "__main__":
    scraper = CodemiteScraper()
    jobs = scraper.scrape_listings()
    for job in jobs:
        print(job.pretty_print())
