from celery import Celery
from datetime import datetime
import traceback
import argparse
from src.core.database import db_session
from src.models.db.job import save_jobs_to_db, archive_old_jobs
from src.core.celery_config import celery
from src.utils.logger import get_logger
from src.services.scrapers.codemite_scraper import CodemiteScraper
from src.services.scrapers.wso2_scraper import WSO2Scraper
from src.services.scrapers.rootcode_scraper import RootcodeScraper
logger = get_logger(__name__)

@celery.task
def aggregate_jobs():
    run_aggregator()

def run_aggregator(scraper_names=None):
    """Run aggregator directly for testing"""
    available_scrapers = {
        'wso2': WSO2Scraper,
        'codemite': CodemiteScraper,
        'rootcode': RootcodeScraper
    }
    
    scrapers = []
    if scraper_names:
        for name in scraper_names:
            if name in available_scrapers:
                scrapers.append(available_scrapers[name]())
    else:
        scrapers = [scraper() for scraper in available_scrapers.values()]

    with db_session() as db:
        all_new_jobs = []
        for scraper in scrapers:
            try:
                logger.info(f"Running scraper: {scraper.__class__.__name__}")
                jobs = scraper.scrape_listings()
                all_new_jobs.extend(jobs)
                save_jobs_to_db(jobs, db)
                logger.info(f"Saved {len(jobs)} jobs from {scraper.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error running {scraper.__class__.__name__}: {e}\n"
                            f"Traceback:\n{''.join(traceback.format_tb(e.__traceback__))}")
        
        # archive old jobs
        try: 
            num = archive_old_jobs(all_new_jobs, db)
            logger.info(f"Archived {num} old jobs")
        except Exception as e:
            logger.error(f"Error archiving old jobs: {str(e)}")
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job Aggregator Tester')
    parser.add_argument('--scrapers', nargs='+', help='Specific scrapers to run')
    args = parser.parse_args()
    
    run_aggregator(args.scrapers)

