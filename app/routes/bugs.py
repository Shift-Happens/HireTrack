from flask import Blueprint, render_template, request, flash, current_app
from flask_login import current_user
import os
from datetime import datetime
import json
import logging

bp = Blueprint('bugs', __name__)

@bp.route('/report-bug', methods=['GET', 'POST'])
def report_bug():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        # Create bug report
        report = {
            'title': title,
            'description': description,
            'user': current_user.username if not current_user.is_anonymous else 'Anonymous',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'url': request.form.get('current_url', ''),
            'user_agent': request.headers.get('User-Agent'),
        }
        
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(current_app.root_path, 'bug_reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Save report
        filename = f"bug_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{title[:30]}.json"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
            
        flash('Bug report submitted successfully. Thank you!', 'success')
        
    return render_template('bugs/report.html')