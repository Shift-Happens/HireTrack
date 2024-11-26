from app import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    work_type = db.Column(db.String(20), default='Hybrid')  # Office, Hybrid, Remote
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    salary_currency = db.Column(db.String(3), default='PLN')
    job_link = db.Column(db.String(500))
    status = db.Column(db.String(20), default='Applied')
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contract_type = db.Column(db.String(20), default='UoP')