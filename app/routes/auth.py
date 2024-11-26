from flask import Blueprint, render_template, redirect, url_for, flash, request, session  # Add session here
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('_flashes', None)  # Add this line
    
    if request.method == 'POST':
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=request.form['email']).first()
        if existing_user:
            flash('An account with this email already exists.', 'error')
            return render_template('auth/register.html')
            
        # Check if username already exists
        existing_username = User.query.filter_by(username=request.form['username']).first()
        if existing_username:
            flash('Username already taken.', 'error')
            return render_template('auth/register.html')

        # Create new user if checks pass
        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('auth/register.html')
            
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('jobs.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))