from app import create_app, db

app = create_app()

with app.app_context():
    # Add new columns
    with db.engine.connect() as conn:
        conn.execute('ALTER TABLE job ADD COLUMN salary_min INTEGER')
        conn.execute('ALTER TABLE job ADD COLUMN salary_max INTEGER')
        conn.execute('ALTER TABLE job ADD COLUMN job_link VARCHAR(500)')
    db.session.commit()