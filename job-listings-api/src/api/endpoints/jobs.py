from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.core.database import get_db
from src.models.db.job import JobModel

router = APIRouter()


@router.get("/jobs")
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    query: str = Query(None),
    location: str = Query(None)
):
    jobs_query = db.query(JobModel).order_by(desc(JobModel.date_posted))
    
    if query:
        jobs_query = jobs_query.filter(JobModel.title.ilike(f"%{query}%"))
    if location:
        jobs_query = jobs_query.filter(
            JobModel.location.ilike(f"%{location}%"))

    jobs = jobs_query.offset(skip).limit(limit).all()
    domain_jobs = []
    for job in jobs:
        domain_jobs.append(job.to_domain())
    return domain_jobs


@router.get("/jobs/{job_id}")
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    return db.query(JobModel).filter(JobModel.id == job_id).first()
