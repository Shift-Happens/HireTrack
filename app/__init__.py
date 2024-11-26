from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from app.routes import auth, jobs, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(api.bp)
    
    return app
