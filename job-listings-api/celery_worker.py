from src.core.celery_config import celery
from src.services.job_aggregator import run_aggregator

@celery.task(
    name='src.tasks.aggregate_jobs',
    bind=True,
    max_retries=3
)
def aggregate_jobs_task(self):
    try:
        return run_aggregator()
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

if __name__ == '__main__':
    celery.start()
