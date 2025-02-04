from src.models.job import Job
from scrapy import Spider, Request
from datetime import datetime
from typing import List
import json
from src.utils.logger import get_logger
from src.services.scrapers.scrapy_base import BaseScrapyScraper, BaseSpider
from src.models.schemas import RemoteType, JobType
import html

logger = get_logger(__name__)

class AscenticSpider(BaseSpider):
    name = 'ascentic'
    allowed_domains = ['career.ascentic.se']
    start_urls = ['https://career.ascentic.se/jobs']

    def parse(self, response):
        for job in response.css('#jobs_list_container li'):
            title = job.css('.company-link-style::text').get()
            url = job.css('a::attr(href)').get()
            department = job.css('span span:first-child::text').get()
            location = job.css('span span:nth-child(3)::text').get()
            remote_text = job.css('span.inline-flex::text').get()

            if not url:
                continue

            job_data = {
                'title': title.strip() if title else None,
                'department': department.strip() if department else None,
                'location': location.strip() if location else None,
                'remote_text': remote_text.strip() if remote_text else None,
                'url': url
            }

            yield Request(
                url=job_data['url'],
                callback=self.parse_job_details,
                cb_kwargs={'job': job_data},
                errback=self.handle_error
            )

    def parse_job_details(self, response, job):
        # Extract JSON-LD data from script tag
        script = response.css('script[type="application/ld+json"]::text').get().replace('\n', '')
        if not script:
            return None

        try:

            job_data = json.loads(script)
            description = html.unescape(job_data.get('description', ''))
            date_posted = datetime.fromisoformat(job_data.get('datePosted', ''))
            
            remote_status = RemoteType.HYBRID if job['remote_text'] and 'hybrid' in job['remote_text'].lower() else RemoteType.ONSITE

            yield {
                'title': job_data.get('title'),
                'description': description,
                'company': job_data.get('hiringOrganization', {}).get('name', 'Ascentic'),
                'location': 'Colombo, Sri Lanka',
                'job_type': JobType.FULL_TIME,
                'is_remote': remote_status,
                'apply_url': job['url'],
                'date_posted': date_posted,
                'source': 'Ascentic Careers',
                'company_logo': job_data.get('hiringOrganization', {}).get('logo'),
                'company_website': job_data.get('hiringOrganization', {}).get('sameAs')
            }
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing job details JSON: {e}")
            return None

class AscenticScraper(BaseScrapyScraper):
    def __init__(self, *args, **kwargs):
        super(AscenticScraper, self).__init__(*args, **kwargs)
        self.spider_class = AscenticSpider

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
