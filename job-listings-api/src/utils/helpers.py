def validate_job_data(job_data):
    # Validate job data to ensure it meets the required format
    required_fields = ['title', 'description', 'company', 'location']
    for field in required_fields:
        if field not in job_data:
            raise ValueError(f"Missing required field: {field}")
    return True

def format_job_listing(job):
    # Format job listing for display or API response
    return {
        'title': job.title,
        'description': job.description,
        'company': job.company,
        'location': job.location
    }

def filter_jobs_by_location(jobs, location):
    # Filter job listings by location
    return [job for job in jobs if job.location == location]