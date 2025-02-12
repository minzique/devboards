from hashlib import md5
from src.models.job import Job
from datetime import datetime
from typing import List
import re
from src.utils.logger import get_logger
from src.services.scrapers.bs4_base import BaseBS4Scraper
from src.models.schemas import RemoteType

logger = get_logger(__name__)

class NinetyNineXScraper(BaseBS4Scraper):
    BASE_URL = 'https://www.careers-page.com/99x-3'

    def scrape_listings(self) -> List[Job]:
        soup = self.get_soup(self.BASE_URL)
        if not soup:
            return []
            
        raw_jobs = []
        # Use the template that contains actual jobs (v-else-if="jobs && jobs.length == 0")
        for job in soup.select('template[v-else-if="jobs && jobs.length == 0"] li.media'):
            # Get job details
            
            title = job.select_one('h5.mt-0.mb-1.primary-color').string.strip()
            if not title or '[[ job.position_name ]]' in title:
                continue
                
            # Get job URL
            url_elem = job.select_one('div.media-body a')
            if not url_elem:
                continue
                
            url = url_elem.get('href')
            if not url.startswith('http'):
                url = f"https://www.careers-page.com{url}"
                
            # Get location
            location_span = job.select_one('span.text-secondary span[style="margin-right: 10px;"]')
            location = location_span.text.strip() if location_span else "Not specified"
            
            # Get job details page
            job_details = self.get_soup(url)
            if not job_details:
                continue
                
            description = job_details.select_one('meta[property="og:description"]')
            description_text = description['content'] if description else "No description available"
            
            # Determine remote status from description
            description_lower = description_text.lower()
            remote_indicators = ['remote', 'work from home', 'wfh']
            hybrid_indicators = ['hybrid', 'flexible']
            
            if any(indicator in description_lower for indicator in remote_indicators):
                remote_type = RemoteType.REMOTE
            elif any(indicator in description_lower for indicator in hybrid_indicators):
                remote_type = RemoteType.HYBRID
            else:
                remote_type = RemoteType.ONSITE

            raw_jobs.append({
                'title': title,
                'description': description_text,
                'company': '99x',
                'location': location,
                'job_type': 'Full Time',
                'remote_type': remote_type,
                'apply_url': url,
                'date_posted': datetime.now().isoformat(),
                'source': '99x Careers'
            })
            
        return self.process_listings(raw_jobs)

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
                    is_remote=item['remote_type'],
                    apply_url=item['apply_url'],
                    date_posted=datetime.fromisoformat(item['date_posted']),
                    source=item['source']
                )
            )
        return processed_jobs
    
    def generate_job_hash(self, job_data):
        hash_string = (
            f"{job_data.get('title', '')}"
            f"{job_data.get('apply_url', '')}"
            
        )
        return md5(hash_string.encode()).hexdigest()


if __name__ == "__main__":
    scraper = NinetyNineXScraper()
    jobs = scraper.scrape_listings()
    for job in jobs:
        print(job)
