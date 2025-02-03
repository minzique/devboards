from src.models.job import Job
from scrapy import Spider, Request
from datetime import datetime
from typing import List
from src.utils.logger import get_logger
from src.services.scrapers.scrapy_base import BaseScrapyScraper, BaseSpider
from src.models.schemas import RemoteType

logger = get_logger(__name__)

class NinetyNineXSpider(BaseSpider):
    name = '99x'
    allowed_domains = ['careers-page.com']
    start_urls = ['https://www.careers-page.com/99x-3']
    
    def parse(self, response):
        # Parse each job listing from the main page, excluding template sections
        for job in response.css('template[v-else-if="jobs && jobs.length == 0"] li.media'):
            title = job.css('h5.primary-color::text').get()
            if not title or title == '[[ job.position_name ]]':  # Skip template elements
                continue
                
            location = job.css('span.fas.fa-map-marker-alt').xpath('following-sibling::text()').get()
            url = response.urljoin(job.css('div.media-body a::attr(href)').get())
            
            if not url:
                continue

            job_data = {
                'title': title.strip(),
                'location': location.strip() if location else "Not specified",
                'url': url
            }
            
            yield Request(
                url=job_data['url'],
                callback=self.parse_job_details,
                cb_kwargs={'job': job_data},
                errback=self.handle_error
            )

    def parse_job_details(self, response, job):
        description = response.css('meta[property="og:description"]::attr(content)').get()
        
        remote_indicators = ['remote', 'work from home', 'wfh']
        is_remote = any(indicator in description.lower() for indicator in remote_indicators) if description else False

        yield {
            'title': job['title'],
            'description': description or "No description available",
            'company': '99x',
            'location': job['location'],
            'job_type': 'Full Time',  # Default as site doesn't specify
            'is_remote': is_remote,
            'apply_url': job['url'],
            'date_posted': datetime.now().isoformat(),
            'source': '99x Careers'
        }

class NinetyNineXScraper(BaseScrapyScraper):
    def __init__(self, *args, **kwargs):
        super(NinetyNineXScraper, self).__init__(*args, **kwargs)
        self.spider_class = NinetyNineXSpider

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
                    is_remote=self._parse_remote_type(item['is_remote']),
                    apply_url=item['apply_url'],
                    date_posted=datetime.fromisoformat(item['date_posted']),
                    source=item['source']
                )
            )
        return processed_jobs

    def _parse_remote_type(self, is_remote: bool) -> str:
        return RemoteType.REMOTE if is_remote else RemoteType.ONSITE

if __name__ == "__main__":
    scraper = NinetyNineXScraper()
    jobs = scraper.scrape_listings()
    for job in jobs:
        print(job)
