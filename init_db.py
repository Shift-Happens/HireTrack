import os
from app import create_app, db
from app.models.user import User
from app.models.job import Job

# Ensure instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

app = create_app()

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()
    print("Database initialized with new schema!")