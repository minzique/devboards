from hashlib import md5
class BaseScraper:
    def scrape_listings(self):
        raise NotImplementedError

    def process_listings(self, raw_data):
        raise NotImplementedError
    
    def generate_job_hash(self, job_data: dict) -> str:
        """Generate a consistent hash for a job listing"""
        # Default implementation using common fields
        hash_string = f"{job_data.get('title', '')}{job_data.get('company', '')}{
            job_data.get('url', '')}"
        return md5(hash_string.encode()).hexdigest()
