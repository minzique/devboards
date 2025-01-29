from datetime import datetime
from enum import Enum
from typing import Optional


class JobType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class Job:
    def __init__(
        self,
        title: str,
        description: str,
        company: str,
        location: str,
        job_type: str = "full-time",
        remote_status: str = "in-office",
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        salary_currency: str = "USD",
        apply_url: str = "",
        date_posted: datetime = datetime.now(),
        source: str = "",
        
    ):
        self.title = title
        self.description = description
        self.company = company
        self.location = location
        self.job_type = job_type
        self.is_remote = remote_status
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.salary_currency = salary_currency
        self.apply_url = apply_url
        self.date_posted = date_posted
        self.source = source

    def __repr__(self):
        return f"Job(title='{self.title}', company='{self.company}', location='{self.location}', type='{self.job_type.value}')"

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
            "source": self.source
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
        """ 
