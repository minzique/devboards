from datetime import datetime
from typing import List
import json
from src.utils.logger import get_logger
from src.services.scrapers.bs4_base import BaseBS4Scraper
from src.models.schemas import RemoteType, JobType
from src.models.job import Job
import html

logger = get_logger(__name__)

class IFSScraper(BaseBS4Scraper):
    BASE_URL = 'https://www.smartrecruiters.com/job-api/public/search/widgets/IFS1/postings'
    
    def scrape_listings(self) -> List[Job]:
        # Get API response
        params = {'fq': 'location:(Colombo)'}
        url = f"{self.BASE_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
        response_text = self.fetch_url(url)
        
        if not response_text:
            return []
            
        try:
            json_data = json.loads(response_text)
            raw_jobs = []
            
            for job in json_data.get('results', []):
                job_data = {
                    'job_id': job['jobVacancyId'],
                    'title': job['vacancyName'],
                    'location': job['location'],
                    'department': job['department'],
                    'country': job.get('countryName'),
                    'reference': job.get('refNumber'),
                    'remote_status': self._get_remote_status(job.get('customFieldValues', [])),
                    'job_type': self._get_job_type(job.get('customFieldValues', [])),
                }
                
                # Get job details page
                detail_url = f"https://www.smartrecruiters.com/IFS1/{job['publicationId']}-{job['urlJobName']}"
                job_details = self.get_soup(detail_url)
                
                if job_details:
                    description = job_details.select_one('meta[property="og:description"]')
                    description_text = description['content'] if description else None
                    
                    if description_text:
                        description_text = html.unescape(description_text)

                    location = job_data['location']
                    if job_data.get('country'):
                        location = f"{location}, {job_data['country']}"

                    raw_jobs.append({
                        'title': job_data['title'],
                        'company': 'IFS',
                        'description': description_text or f"Department: {job_data['department']}\nReference: {job_data['reference']}",
                        'location': location,
                        'job_type': job_data['job_type'],
                        'is_remote': job_data['remote_status'],
                        'apply_url': detail_url,
                        'date_posted': datetime.fromtimestamp(job['releasedDate']/1000),
                        'source': 'IFS Careers',
                    })
                    
            return self.process_listings(raw_jobs)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing API response: {e}")
            return []

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
