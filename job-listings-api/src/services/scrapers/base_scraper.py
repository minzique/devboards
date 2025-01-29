class BaseScraper:
    def fetch_listings(self):
        raise NotImplementedError

    def process_listings(self, raw_data):
        raise NotImplementedError
