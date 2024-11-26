from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.models.job import Job
from app import db, socketio  # Import socketio directly from app
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

# Test API key - move this to config in production
TEST_API_KEY = "test_key_123"

def validate_api_key():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {TEST_API_KEY}":
        return False
    return True

@bp.route('/jobs', methods=['POST'])
def add_job():
    if not validate_api_key():
        return jsonify({"error": "Invalid API key"}), 401
        
    try:
        data = request.json
        
        job = Job(
            company=data['company'],
            position=data['position'],
            location=data.get('location', ''),
            work_type=data.get('work_type', 'Hybrid'),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            salary_currency=data.get('salary_currency', 'PLN'),
            job_link=data.get('job_link', ''),
            status='Applied',
            notes=data.get('notes', ''),
            user_id=1,  # Default user for extension
            contract_type=data.get('contract_type', 'UoP')
        )
        
        db.session.add(job)
        db.session.commit()

        # Prepare job data for emit
        job_data = {
            'id': job.id,
            'company': job.company,
            'position': job.position,
            'location': job.location,
            'work_type': job.work_type,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'salary_currency': job.salary_currency,
            'job_link': job.job_link,
            'status': job.status,
            'notes': job.notes,
            'contract_type': job.contract_type,
            'applied_date': job.applied_date.strftime('%d-%m-%y')
        }

        # Emit the event
        socketio.emit('new_job', job_data)
        
        return jsonify({
            "status": "success",
            "message": "Job added successfully",
            "job_id": job.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@bp.route('/jobs/test', methods=['GET'])
def test_connection():
    """Test endpoint for extension setup"""
    if not validate_api_key():
        return jsonify({"error": "Invalid API key"}), 401
    return jsonify({"status": "success", "message": "API connection successful"})