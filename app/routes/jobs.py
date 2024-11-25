from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models.job import Job
from app import db

bp = Blueprint('jobs', __name__)

@bp.route('/')
@login_required
def index():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    is_new_user = len(jobs) == 0
    return render_template('jobs/index.html', jobs=jobs, is_new_user=is_new_user)

@bp.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    if request.method == 'POST':
        job = Job(
            company=request.form['company'],
            position=request.form['position'],
            salary_min=request.form.get('salary_min'),
            salary_max=request.form.get('salary_max'),
            job_link=request.form.get('job_link'),
            status=request.form['status'],
            notes=request.form['notes'],
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('jobs.index'))
    return render_template('jobs/new.html')

@bp.route('/job/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    job = Job.query.get_or_404(id)
    # Ensure user can only edit their own jobs
    if job.user_id != current_user.id:
        return redirect(url_for('jobs.index'))
        
    if request.method == 'POST':
        job.company = request.form['company']
        job.position = request.form['position']
        job.salary_min = request.form.get('salary_min')
        job.salary_max = request.form.get('salary_max')
        job.job_link = request.form.get('job_link')
        job.status = request.form['status']
        job.notes = request.form['notes']
        
        db.session.commit()
        return redirect(url_for('jobs.index'))
        
    return render_template('jobs/edit.html', job=job)

@bp.route('/job/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    job = Job.query.get_or_404(id)
    if job.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    job.status = data.get('status')
    db.session.commit()
    return jsonify({'status': 'success'})