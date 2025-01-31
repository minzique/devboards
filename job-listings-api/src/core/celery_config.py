from celery.schedules import crontab
from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Redis as the message broker
    backend="redis://localhost:6379/0",  # Result backend
)
celery.conf.beat_schedule = {
    "scrape_jobs_every_hour": {
        "task": "tasks.aggregate_jobs",
        "schedule": crontab(minute=0, hour="*"),  # Runs every hour
    },
}
