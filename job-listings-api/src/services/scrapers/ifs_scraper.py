from datetime import datetime
from src.utils.logger import get_logger
from src.models.schemas import RemoteType, JobType
from src.services.scrapers.scrapy_base import BaseScrapyScraper, BaseSpider
from src.models.job import Job
import json
from scrapy import Request
from typing import List
from bs4 import BeautifulSoup
import html

logger = get_logger(__name__)

class IFSSpider(BaseSpider):
    name = 'ifs'
    allowed_domains = ['smartrecruiters.com']
    base_url = 'https://www.smartrecruiters.com/job-api/public/search/widgets/IFS1/postings'
    
    def start_requests(self):
        # Start with API request
        params = {'fq': 'location:(Colombo)'}
        url = f"{self.base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
        yield Request(url, callback=self.parse_api)

    def parse_api(self, response):
        try:
            json_data = json.loads(response.text)
            for job in json_data.get('results', []):
                job_data = {
                    'job_id': job['jobVacancyId'],
                    'title': job['vacancyName'],
                    'location': job['location'],
                    'department': job['department'],
                    'country': job.get('countryName'),
                    'reference': job.get('refNumber'),
                    'publication_id': job['publicationId'],
                    'url_name': job['urlJobName'],
                    'released_date': job['releasedDate'],
                    'remote_status': self._get_remote_status(job.get('customFieldValues', [])),
                    'job_type': self._get_job_type(job.get('customFieldValues', []))
                }
                
                # Request job details page
                detail_url = f"https://www.smartrecruiters.com/IFS1/{job['publicationId']}-{job['urlJobName']}"
                yield Request(
                    detail_url,
                    callback=self.parse_job_details,
                    cb_kwargs={'job': job_data},
                    errback=self.handle_error
                )
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing API response: {e}")

    def parse_job_details(self, response, job):
        try:
            description = response.css('meta[property="og:description"]::attr(content)').get()
            if description:
                description = html.unescape(description)

            location = job['location']
            if job.get('country'):
                location = f"{location}, {job['country']}"

            yield {
                'title': job['title'],
                'company': 'IFS',
                'description': description or f"Department: {job['department']}\nReference: {job['reference']}",
                'location': location,
                'job_type': job['job_type'],
                'is_remote': job['remote_status'],
                'apply_url': response.url,
                'date_posted': datetime.fromtimestamp(job['released_date']/1000),
                'source': 'IFS Careers',
            }
        except Exception as e:
            logger.error(f"Error parsing job details: {e}")

    def _get_remote_status(self, custom_fields):
        """Extract remote status from custom fields"""
        for field in custom_fields:
            if field.get('fieldId') == '5ef4521cf523684c71779c53':
                if field.get('valueLabel') == 'On site':
                    return RemoteType.ONSITE
                elif field.get('valueLabel') == 'Hybrid':
                    return RemoteType.HYBRID
        return RemoteType.HYBRID  # Default

    def _get_job_type(self, custom_fields):
        """Extract job type from custom fields"""
        for field in custom_fields:
            if field.get('fieldId') == '5e67cbb7336cbf68dd5d5756':
                if field.get('valueLabel') == 'Student or Intern':
                    return JobType.INTERNSHIP
        return JobType.FULL_TIME  # Default

class IFSScraper(BaseScrapyScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spider_class = IFSSpider

    def process_listings(self, raw_data) -> List[Job]:
        processed_jobs = []
        seen_hashes = set()

        for item in raw_data:
            job_hash = self.generate_job_hash(item)
            logger.debug(f"Generated hash: {job_hash}")

            if job_hash in seen_hashes:
                logger.debug(f"Skipping duplicate job: {item['title']} - {item['apply_url']}")
                continue

            seen_hashes.add(job_hash)
            processed_jobs.append(
                Job(
                    job_hash=job_hash,
                    title=item['title'],
                    description=item['description'],
                    company=item['company'],
                    location=item['location'],
                    job_type=item['job_type'],
                    is_remote=item['is_remote'],
                    apply_url=item['apply_url'],
                    date_posted=item['date_posted'],
                    source=item['source']
                )
            )
        return processed_jobs

if __name__ == "__main__":
    scraper = IFSScraper()
    jobs = scraper.scrape_listings()
    for job in jobs:
        print(job.pretty_print())
