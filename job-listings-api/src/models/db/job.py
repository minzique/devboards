from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from src.models.job import Job
from src.models.schemas import RemoteType, JobType
from src.utils.logger import get_logger

logger = get_logger(__name__)

Base = declarative_base()

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, index=True)
    job_hash = Column(String, index=True, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    company = Column(String, index=True)
    location = Column(String)
    job_type = Column(String)
    is_remote = Column(String, default="in-office")
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String, default="USD")
    apply_url = Column(String)
    date_posted = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    date_fetched = Column(DateTime)
    
    def to_domain(self) -> Job:
        """Convert DB model to domain model"""
        return Job(
            title=self.title,
            description=self.description,
            company=self.company,
            location=self.location,
            job_type=self.job_type,
            is_remote=self.is_remote,
            salary_min=self.salary_min,
            salary_max=self.salary_max,
            salary_currency=self.salary_currency,
            apply_url=self.apply_url,
            date_posted=self.date_posted,
            source=self.source
        )


class ArchiveJobModel(Base):
    __tablename__ = "archive_jobs"
    
    id = Column(Integer, index=True)
    job_hash = Column(String, index=True, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    company = Column(String, index=True)
    location = Column(String)
    job_type = Column(String)
    is_remote = Column(String, default="in-office")
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String, default="USD")
    apply_url = Column(String)
    date_posted = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    date_fetched = Column(DateTime)
    date_archived = Column(DateTime, default=datetime.utcnow)


def save_jobs_to_db(jobs: list[Job], db: Session):
    for job in jobs:
        try:
            existing_job = db.query(JobModel).filter_by(job_hash=job.job_hash).first()  
            logger.info(f"Checking job: {job.title}")
            if existing_job:
                continue    
        except Exception as e:
            print(f"Error querying job: {e}")
            continue
        job_listing = job.to_db_model()
        db.add(job_listing)
    db.commit()

def archive_old_jobs(jobs: list, db: Session) -> int:
    """Move jobs not in current listings to archive table"""
    current_job_hashes = [job.job_hash for job in jobs]
    
    # Find jobs to archive
    jobs_to_archive = db.query(JobModel).filter(
        ~JobModel.job_hash.in_(current_job_hashes)
    ).all()

    count = 0
    for job in jobs_to_archive:
        archived_job = ArchiveJobModel()
        # Copy all attributes from original job
        for column in JobModel.__table__.columns:
            setattr(archived_job, column.name, getattr(job, column.name))
        # Add archive timestamp
        archived_job.date_archived = datetime.utcnow()
        
        db.add(archived_job)
        db.delete(job)  
        count += 1
    
    db.commit()
    return count