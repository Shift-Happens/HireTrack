import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hiretrack.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Settings
    API_KEY = os.environ.get('API_KEY') 
    CORS_HEADERS = 'Content-Type'
