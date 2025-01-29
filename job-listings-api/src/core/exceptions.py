class JobListingException(Exception):
    """Base exception class for job listing application"""
    pass

class ScrapingException(JobListingException):
    """Raised when scraping fails"""
    pass

class APIException(JobListingException):
    """Raised when API integration fails"""
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)

class ValidationException(JobListingException):
    """Raised when data validation fails"""
    def __init__(self, message, field=None):
        self.field = field
        super().__init__(message)

class AuthenticationException(JobListingException):
    """Raised when authentication fails"""
    pass

class RateLimitException(JobListingException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message, retry_after=None):
        self.retry_after = retry_after
        super().__init__(message)

class DatabaseException(JobListingException):
    """Raised when database operations fail"""
    pass