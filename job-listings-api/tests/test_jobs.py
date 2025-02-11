import pytest
from src.models.job import Job
from src.api.endpoints.jobs import list_jobs, create_job, get_job_details

@pytest.fixture
def sample_job():
    return Job(title="Software Engineer", description="Develop and maintain software applications.", company="Tech Corp", location="Remote")

def test_list_jobs():
    response = list_jobs()
    assert isinstance(response, list)

def test_create_job(sample_job):
    response = create_job(sample_job)
    assert response['title'] == sample_job.title
    assert response['company'] == sample_job.company

def test_get_job_details(sample_job):
    job_id = create_job(sample_job)['id']
    response = get_job_details(job_id)
    assert response['id'] == job_id
    assert response['title'] == sample_job.title