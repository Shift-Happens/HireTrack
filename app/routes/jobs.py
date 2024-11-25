from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.job import Job
from app import db

bp = Blueprint('jobs', __name__)

@bp.route('/')
@login_required
def index():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('jobs/index.html', jobs=jobs)

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