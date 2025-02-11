import pytest

@pytest.fixture(scope='session')
def sample_job_data():
    return {
        'title': 'Software Engineer',
        'description': 'Develop and maintain software applications.',
        'company': 'Tech Company',
        'location': 'Remote'
    }