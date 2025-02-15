import os
from celery.schedules import crontab
from celery import Celery

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(
    "job_listings",
    broker=redis_url,
    backend=redis_url,
)
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    beat_initial_task_count=1,  # Run immediately on startup
    beat_sync_every=0,
    timezone='UTC',
    enable_utc=True,
)
celery.conf.beat_schedule = {
    "scrape_jobs_every_hour": {
        "task": "src.tasks.aggregate_jobs",
        "schedule": crontab(minute=0, hour="*"),  # Runs every hour
    },
}
