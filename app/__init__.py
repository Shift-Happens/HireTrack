from flask import Flask
from config import Config
from app.extensions import db, login_manager, socketio, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    cors.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes import auth, jobs, api, bugs
    app.register_blueprint(auth.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(bugs.bp)
    
    return app
