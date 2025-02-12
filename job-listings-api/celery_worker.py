from src.core.celery_config import celery
from src.services.job_aggregator import aggregate_jobs

# Register tasks
celery.tasks.register(aggregate_jobs)

if __name__ == '__main__':
    celery.start()
