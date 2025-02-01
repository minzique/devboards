from src.models.job import Job
from scrapy.signalmanager import dispatcher
from scrapy import Spider, Request, signals
from datetime import datetime
from typing import List
from src.utils.logger import get_logger
from src.services.scrapers.scrapy_base import BaseScrapyScraper, BaseSpider

logger = get_logger(__name__)

class WSO2Spider(BaseSpider):
    name = 'wso2'
    allowed_domains = ['wso2.com']
    start_urls = ["https://wso2.com/careers/"]

    def parse(self, response):
        for tile in response.css('div.vacancy_tile'):
            title = tile.css('h3::text').get()
            logger.debug(f"Processing job: {title}")
            team = tile.css('span.cTeam::text').get()
            location = tile.css('span.cCountry::text').getall()
            employment_type = tile.css('span.cArea::text').get()
            url = tile.css('a.cOrangeMore::attr(href)').get()
            
            if not title or not url:
                continue

            job = {
                'title': title.strip(),
                'team': team.strip() if team else "Unknown",
                'location': location,
                'employment_type': employment_type.strip() if employment_type else "Unknown",
                'url': response.urljoin(url)
            }


            yield Request(
                url=job['url'],
                callback=self.parse_job_details,
                cb_kwargs={'job': job},
                errback=self.handle_error
            )

    def parse_job_details(self, response, job):
        description = response.css('div.cDescription').get()
        about_role = response.css('div.cDescription h2:contains("About the Role") + p::text').get()
        responsibilities = response.css('h2:contains("Your Key Responsibilities") + ul.cTriangleBullet li::text').getall()
        qualifications = response.css('h2:contains("Qualifications and Skills") + ul.cTriangleBullet li::text').getall()
        
        full_description = '\n'.join([
            description.strip() if description else "No description available",
            about_role.strip() if about_role else "",
            "\nResponsibilities:\n" + '\n'.join(responsibilities) if responsibilities else "",
            "\nQualifications:\n" + '\n'.join(qualifications) if qualifications else ""
        ])

        yield {
            "title": job['title'],
            "description": full_description,
            "company": 'WSO2',
            "location": ', '.join(job['location']) if job['location'] else "Unknown",
            "job_type": job['employment_type'],
            "is_remote": 'remote' in full_description.lower(),
            "apply_url": job['url'],
            "date_posted": datetime.now().isoformat(),
            "source": 'WSO2 Careers'
        }

class WSO2Scraper(BaseScrapyScraper):
    def __init__(self):
        super().__init__()
        self.spider_class = WSO2Spider

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
                    date_posted=datetime.fromisoformat(item['date_posted']),
                    source=item['source']
                )
            )
        return processed_jobs


if __name__ == "__main__":
    scraper = WSO2Scraper()
    jobs = scraper.scrape_listings()

    for job in jobs:
        print(job)
