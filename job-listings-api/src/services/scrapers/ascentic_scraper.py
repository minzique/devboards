from datetime import datetime
from typing import List
import json
from src.utils.logger import get_logger
from src.services.scrapers.bs4_base import BaseBS4Scraper
from src.models.schemas import RemoteType, JobType
from src.models.job import Job
import html

logger = get_logger(__name__)

class AscenticScraper(BaseBS4Scraper):
    BASE_URL = 'https://career.ascentic.se/jobs'

    def scrape_listings(self) -> List[Job]:
        soup = self.get_soup(self.BASE_URL)
        if not soup:
            return []
            
        raw_jobs = []
        for job in soup.select('#jobs_list_container li'):
            title = job.select_one('.company-link-style')
            url = job.select_one('a')['href']
            department = job.select('span span')[0] if job.select('span span') else None
            location = job.select('span span')[2] if len(job.select('span span')) > 2 else None
            remote_text = job.select_one('span.inline-flex')

            if not url or not title:
                continue

            job_details = self.get_soup(url)
            if not job_details:
                continue
            logger.debug(f"Processing job: {title.text} - {url}")
            # logger.debug(f"Job details: {job_details}")
            script = job_details.select_one('script[type="application/ld+json"]').string
            if not script:
                continue

            try:
                job_data = json.loads(script.strip().replace('\n', ''))
                description = html.unescape(job_data.get('description', ''))
                date_posted = datetime.fromisoformat(job_data.get('datePosted', ''))
                
                remote_text_value = remote_text.text.strip() if remote_text else ''
                remote_status = RemoteType.HYBRID if 'hybrid' in remote_text_value.lower() else RemoteType.ONSITE

                raw_jobs.append({
                    'title': job_data.get('title'),
                    'description': description,
                    'company': job_data.get('hiringOrganization', {}).get('name', 'Ascentic'),
                    'location': 'Colombo, Sri Lanka',
                    'job_type': JobType.FULL_TIME,
                    'is_remote': remote_status,
                    'apply_url': url,
                    'date_posted': date_posted,
                    'source': 'Ascentic Careers',
                    'company_logo': job_data.get('hiringOrganization', {}).get('logo'),
                    'company_website': job_data.get('hiringOrganization', {}).get('sameAs')
                })
            except (json.JSONDecodeError, AttributeError) as e:
                logger.error(f"Error parsing job details: {e}")
                raise e
            
        return self.process_listings(raw_jobs)

    def process_listings(self, raw_data) -> List[Job]:
        processed_jobs = []
        seen_hashes = set()

        for item in raw_data:
            job_hash = self.generate_job_hash(item)
            logger.debug(f"Generated hash: {job_hash}")
            logger.debug(f"Job data: {item}")
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
                    source=item['source'],
                    company_logo=item.get('company_logo'),
                    company_website=item.get('company_website')
                )
            )
        return processed_jobs

if __name__ == "__main__":
    scraper = AscenticScraper()
    jobs = scraper.scrape_listings()
    for job in jobs:
        print(job)
