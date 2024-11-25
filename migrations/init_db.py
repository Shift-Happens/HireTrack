from app import create_app, db
from app.models.user import User
from app.models.job import Job

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized!")