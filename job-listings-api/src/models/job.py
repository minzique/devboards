from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from src.models.schemas import RemoteType, JobType
from src.models.db.company import CompanyModel
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Job:
    """Core domain model used across the application"""

    def __init__(
        self,
        title: str,
        company: str,
        location: str,
        description: str = "",
        job_type: str = JobType.FULL_TIME,
        is_remote: RemoteType = RemoteType.ONSITE,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        salary_currency: str = "USD",
        apply_url: str = "",
        date_posted: datetime = datetime.utcnow(),
        source: str = "",
        job_hash: Optional[str] = None,
        company_id: Optional[int] = None,
        company_logo: Optional[str] = None,
        company_website: Optional[str] = None,
        date_fetched: Optional[datetime] = None
    ):
        self.title = title
        self.description = description
        self.company = company
        self.location = location
        self.job_type = job_type
        self.is_remote = is_remote
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.salary_currency = salary_currency
        self.apply_url = apply_url
        self.date_posted = date_posted
        self.source = source
        self.job_hash = job_hash
        self.company_id = company_id
        self.company_logo = company_logo
        self.company_website = company_website
        self.date_fetched = date_fetched

    def to_db_model(self, db_session=None) -> 'JobModel':
        """Convert domain model to DB model"""
        from src.models.db.job import JobModel
        if db_session:
            company = db_session.query(CompanyModel).filter_by(name=self.company).first()
            # logger.debug(f"Company: {company}")
            if not company:
                logger.info(f"Creating new company: {self.company}")
                slug = self.company.lower().replace(" ", "-")
                new_company = CompanyModel(name=self.company, logo_url=f"/logos/{slug}.png", website=self.company_website)
                db_session.add(new_company)
                db_session.commit()
                
            company_id = company.id if company else None
        else:
            company_id = None

        return JobModel(
            job_hash=self.job_hash,
            title=self.title,
            description=self.description,
            location=self.location,
            job_type=self.job_type,
            is_remote=self.is_remote,
            salary_min=self.salary_min,
            salary_max=self.salary_max,
            salary_currency=self.salary_currency,
            apply_url=self.apply_url,
            date_posted=self.date_posted,
            source=self.source,
            date_fetched=self.date_fetched or datetime.utcnow(),
            company_id=company_id
        )

    def __repr__(self):
        return f"Job(title='{self.title}', company='{self.company}', location='{self.location}', type='{self.job_type}')"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "company": self.company,
            "location": self.location,
            "job_type": self.job_type,
            "is_remote": self.is_remote,
            "salary_range": {
                "min": self.salary_min,
                "max": self.salary_max,
                "currency": self.salary_currency
            } if self.salary_min or self.salary_max else None,
            "apply_url": self.apply_url,
            "date_posted": self.date_posted.isoformat(),
            "source": self.source,
            "company_id": self.company_id,
            "company_logo": self.company_logo,
            "company_website": self.company_website
        }
        
    def pretty_print(self):
        return f"""
        Title: {self.title}
        Company: {self.company}
        Location: {self.location}
        Type: {self.job_type}
        Remote: {self.is_remote}
        Salary: {self.salary_min} - {self.salary_max} {self.salary_currency}
        Apply: {self.apply_url}
        Date: {self.date_posted}
        Source: {self.source}
        Company ID: {self.company_id}
        Company Logo: {self.company_logo}
        Company Website: {self.company_website}
        """
