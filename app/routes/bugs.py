from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from flask_login import current_user
import os
from datetime import datetime, timedelta
import json
import logging
from collections import defaultdict

bp = Blueprint('bugs', __name__)

# Store bug report counts per user per day
bug_counts = defaultdict(lambda: {'count': 0, 'reset_time': None})
BUG_LIMIT = 8

def check_bug_limit(user_id):
    now = datetime.now()
    user_bugs = bug_counts[user_id]
    
    # Reset counter if it's a new day
    if user_bugs['reset_time'] and now.date() > user_bugs['reset_time'].date():
        user_bugs['count'] = 0
        
    if user_bugs['count'] >= BUG_LIMIT:
        return False
        
    user_bugs['count'] += 1
    user_bugs['reset_time'] = now
    return True

@bp.route('/report-bug', methods=['GET', 'POST'])
def report_bug():
    if not current_user.is_authenticated:
        flash('You must be logged in to report bugs.', 'error')
        return redirect(url_for('auth.login'))

    # Clear existing flash messages only on GET request
    if request.method == 'GET':
        session.pop('_flashes', None)
        
    if request.method == 'POST':
        if not check_bug_limit(current_user.id):
            flash(f'You have exceeded the limit of {BUG_LIMIT} bug reports per day.', 'error')
            return redirect(url_for('bugs.report_bug'))
            
        title = request.form['title']
        description = request.form['description']
        
        # Create bug report with additional data
        report = {
            'title': title,
            'description': description,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'url': request.form.get('current_url', ''),
            'user_agent': request.headers.get('User-Agent'),
            'browser_info': {
                'language': request.headers.get('Accept-Language'),
                'platform': request.headers.get('Sec-Ch-Ua-Platform'),
                'mobile': request.headers.get('Sec-Ch-Ua-Mobile')
            },
            'app_version': '1.0.0'  # Add your version tracking
        }
        
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(current_app.root_path, 'bug_reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Save report with UTF-8 encoding
        filename = f"bug_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{title[:30]}.json"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        flash('Bug report submitted successfully! Thank you for helping improve HireTrack.', 'success')
        # Instead of redirecting, render the template directly
        return render_template('bugs/report.html',
            remaining_reports=BUG_LIMIT - bug_counts[current_user.id]['count'],
            bug_limit=BUG_LIMIT
        )
    
    return render_template('bugs/report.html',
        remaining_reports=BUG_LIMIT - bug_counts[current_user.id]['count'] if current_user.is_authenticated else 0,
        bug_limit=BUG_LIMIT
    )