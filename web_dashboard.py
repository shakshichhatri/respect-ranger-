"""
Guardify Web Dashboard
Simple web interface for viewing bot statistics and logs
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)

LOGS_DIR = "forensics_logs"


def get_statistics():
    """Get bot statistics from logs."""
    log_file = os.path.join(LOGS_DIR, "abuse_evidence.jsonl")
    
    if not os.path.exists(log_file):
        return {
            "total_cases": 0,
            "severity_breakdown": {"low": 0, "medium": 0, "high": 0},
            "unique_users": 0,
            "unique_guilds": 0,
            "recent_cases": []
        }
    
    cases = []
    users = set()
    guilds = set()
    severity_count = {"low": 0, "medium": 0, "high": 0}
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line)
                cases.append(record)
                users.add(record.get('author_id'))
                if record.get('guild_id'):
                    guilds.add(record.get('guild_id'))
                
                severity = record.get('analysis', {}).get('severity', 'low')
                severity_count[severity] += 1
            except:
                continue
    
    # Get 10 most recent cases
    recent_cases = sorted(cases, key=lambda x: x.get('logged_at', ''), reverse=True)[:10]
    
    return {
        "total_cases": len(cases),
        "severity_breakdown": severity_count,
        "unique_users": len(users),
        "unique_guilds": len(guilds),
        "recent_cases": recent_cases
    }


def get_warnings():
    """Get warning statistics."""
    warnings_file = os.path.join(LOGS_DIR, "warnings.json")
    
    if not os.path.exists(warnings_file):
        return []
    
    with open(warnings_file, 'r') as f:
        warnings = json.load(f)
    
    warning_list = []
    for key, warns in warnings.items():
        guild_id, user_id = key.split(':')
        warning_list.append({
            "user_id": user_id,
            "guild_id": guild_id,
            "count": len(warns),
            "last_warning": warns[-1]['timestamp'] if warns else None
        })
    
    return sorted(warning_list, key=lambda x: x['count'], reverse=True)


@app.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    stats = get_statistics()
    warnings = get_warnings()
    
    return jsonify({
        "stats": stats,
        "warnings": warnings[:10]  # Top 10 warned users
    })


if __name__ == '__main__':
    # Create templates folder
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
