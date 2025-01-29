from flask import Blueprint, jsonify, request

jobs_bp = Blueprint('jobs', __name__)

# Sample job data
jobs = [
    {
        'id': 1,
        'title': 'Software Engineer',
        'description': 'Develop and maintain software applications.',
        'company': 'Tech Company',
        'location': 'Remote'
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'description': 'Analyze and interpret complex data.',
        'company': 'Data Corp',
        'location': 'On-site'
    }
]

@jobs_bp.route('/jobs', methods=['GET'])
def list_jobs():
    return jsonify(jobs)

@jobs_bp.route('/jobs', methods=['POST'])
def create_job():
    new_job = request.json
    new_job['id'] = len(jobs) + 1
    jobs.append(new_job)
    return jsonify(new_job), 201

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job is None:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job)