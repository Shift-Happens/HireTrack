from flask import Blueprint, render_template, redirect, url_for, request, jsonify, send_file, flash
from flask_login import login_required, current_user
from app.models.job import Job
from app import db
import csv
from io import StringIO, BytesIO
from datetime import datetime

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
            location=request.form['location'],
            work_type=request.form['work_type'],
            salary_min=request.form.get('salary_min'),
            salary_max=request.form.get('salary_max'),
            job_link=request.form.get('job_link'),
            status=request.form['status'],
            notes=request.form['notes'],
            user_id=current_user.id,
            salary_currency=request.form['salary_currency']
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
        job.location = request.form['location']
        job.work_type = request.form['work_type']
        job.salary_min = request.form.get('salary_min')
        job.salary_max = request.form.get('salary_max')
        job.job_link = request.form.get('job_link')
        job.status = request.form['status']
        job.notes = request.form['notes']
        job.salary_currency = request.form['salary_currency']
        
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

@bp.route('/export', methods=['GET'])
@login_required
def export_jobs():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['id', 'company', 'position', 'location', 'work_type', 
                    'salary_min', 'salary_max', 'salary_currency', 'job_link', 
                    'status', 'applied_date', 'notes'])
    
    # Write data
    for job in jobs:
        writer.writerow([
            job.id,
            job.company,
            job.position,
            job.location,
            job.work_type,
            job.salary_min,
            job.salary_max,
            job.salary_currency,
            job.job_link,
            job.status,
            job.applied_date.strftime('%Y-%m-%d'),
            job.notes
        ])
    
    # Convert to bytes
    output.seek(0)
    bytes_output = BytesIO()
    bytes_output.write(output.getvalue().encode('utf-8'))
    bytes_output.seek(0)
    
    return send_file(
        bytes_output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'hiretrack_export_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@bp.route('/import', methods=['POST'])
@login_required
def import_jobs():
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('jobs.index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('jobs.index'))
    
    if not file.filename.endswith('.csv'):
        flash('Only CSV files are allowed', 'error')
        return redirect(url_for('jobs.index'))
        
    try:
        # Read CSV file
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        imported = 0
        updated = 0
        errors = 0
        
        for row in csv_reader:
            try:
                # Check if job exists
                existing_job = Job.query.filter_by(
                    id=row.get('id'), 
                    user_id=current_user.id
                ).first()
                
                if existing_job:
                    # Update existing job
                    existing_job.company = row['company']
                    existing_job.position = row['position']
                    existing_job.location = row.get('location')
                    existing_job.work_type = row.get('work_type', 'Hybrid')
                    existing_job.salary_min = row.get('salary_min')
                    existing_job.salary_max = row.get('salary_max')
                    existing_job.salary_currency = row.get('salary_currency', 'PLN')
                    existing_job.job_link = row.get('job_link')
                    existing_job.status = row.get('status', 'Applied')
                    existing_job.notes = row.get('notes')
                    updated += 1
                else:
                    # Create new job
                    new_job = Job(
                        company=row['company'],
                        position=row['position'],
                        location=row.get('location'),
                        work_type=row.get('work_type', 'Hybrid'),
                        salary_min=row.get('salary_min'),
                        salary_max=row.get('salary_max'),
                        salary_currency=row.get('salary_currency', 'PLN'),
                        job_link=row.get('job_link'),
                        status=row.get('status', 'Applied'),
                        notes=row.get('notes'),
                        user_id=current_user.id
                    )
                    db.session.add(new_job)
                    imported += 1
                    
            except Exception as e:
                errors += 1
                continue
                
        db.session.commit()
        flash(f'Successfully imported {imported} jobs, updated {updated} jobs. {errors} errors occurred.', 'success')
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
    
    return redirect(url_for('jobs.index'))