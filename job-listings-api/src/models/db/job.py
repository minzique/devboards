from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from src.models.job import Job
from src.models.schemas import RemoteType, JobType
from src.utils.logger import get_logger
from src.models.db.company import Base, CompanyModel
import traceback
logger = get_logger(__name__)

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer)
    job_hash = Column(String, nullable=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String)
    job_type = Column(String)
    is_remote = Column(Integer, default=RemoteType.ONSITE)
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String)
    apply_url = Column(String)
    date_posted = Column(DateTime)
    source = Column(String)
    date_fetched = Column(DateTime)
    company_id = Column(Integer, ForeignKey('companies.id'))
    
    # Relationship
    company = relationship("CompanyModel", back_populates="jobs")

    def to_domain(self) -> Job:
        """Convert DB model to domain model"""
        return Job(
            title=self.title,
            description=self.description,
            company=self.company.name if self.company else "",
            location=self.location,
            job_type=self.job_type,
            is_remote=self.is_remote,
            salary_min=self.salary_min,
            salary_max=self.salary_max,
            salary_currency=self.salary_currency,
            apply_url=self.apply_url,
            date_posted=self.date_posted,
            source=self.source,
            job_hash=self.job_hash,
            company_id=self.company_id,
            company_logo=self.company.logo_url if self.company else None,
            company_website=self.company.website if self.company else None,
            date_fetched=self.date_fetched
        )


class ArchiveJobModel(Base):
    __tablename__ = "archive_jobs"
    
    id = Column(Integer, index=True)
    job_hash = Column(String, index=True, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    job_type = Column(String)
    is_remote = Column(Integer, default=RemoteType.ONSITE)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String, default="USD")
    apply_url = Column(String)
    date_posted = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    date_fetched = Column(DateTime)
    date_archived = Column(DateTime, default=datetime.utcnow)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("CompanyModel", backref="archive_jobs")


def save_jobs_to_db(jobs: list[Job], db: Session):
    for job in jobs:
        try:
            existing_job = db.query(JobModel).filter_by(job_hash=job.job_hash).first()  
            logger.debug(f"Checking job: {job.title}")
            if (existing_job):
                logger.debug(f"Job already exists: {job.title}")
                continue    
        except Exception as e:
            print(f"Error querying job: {e}")
            continue
        try:
            job_listing = job.to_db_model(db_session=db)
            db.add(job_listing)
            db.commit()
        except ValueError as e:
            logger.error(f"Error saving job {job.title}: {str(e)}")
            db.rollback()
            continue
        except Exception as e:
            logger.error(f"Unexpected error saving job {job.title}: {str(e)}\n"
                         f"traceback: {traceback.format_exc()}")
            db.rollback()
            continue


def archive_old_jobs(jobs: list, db: Session) -> int:
    """Move jobs not in current listings to archive table"""
    current_job_hashes = [job.job_hash for job in jobs]
    
    # Find jobs to archive
    companies = db.query(JobModel.company_id).filter(JobModel.job_hash.in_(current_job_hashes)).distinct().all()
    company_ids = [company[0] for company in companies]
    
    jobs_to_archive = db.query(JobModel).filter(
        JobModel.company_id.in_(company_ids),
        ~JobModel.job_hash.in_(current_job_hashes)
    ).all()

    count = 0
    for job in jobs_to_archive:
        # Check if job already exists in archive
        existing_archived = db.query(ArchiveJobModel).filter(
            ArchiveJobModel.job_hash == job.job_hash
        ).first()
        
        if existing_archived:
            # Job already archived, just delete from main table
            db.delete(job)
            continue
            
        try:
            archived_job = ArchiveJobModel()
            logger.debug(f"Archiving job: {job.title}")
            # Copy all attributes from original job 
            for column in JobModel.__table__.columns:
                setattr(archived_job, column.name, getattr(job, column.name))
            archived_job.date_archived = datetime.utcnow()
            
            db.add(archived_job)
            db.delete(job)
            count += 1
            db.commit()
            
        except Exception as e:
            logger.error(f"Error archiving job {job.job_hash}: {str(e)}")
            db.rollback()
            continue

    return count