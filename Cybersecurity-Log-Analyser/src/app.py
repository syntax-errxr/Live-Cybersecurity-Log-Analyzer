import os
import logging
import sqlite3
from flask import Flask, render_template, jsonify, request
from db_manager import get_logs, get_alerts, get_total_logs, get_total_alerts, get_logs_per_minute  # Updated to use modular functions
from collections import defaultdict

# Database paths
DB_PATH = "D:\\Cybersecurity-Log-Analyser\\data\\logs.db"
ALERTS_DB_PATH = "D:\\Cybersecurity-Log-Analyser\\data\\alerts.db"

LOGS_FOLDER = "D:\\Cybersecurity-Log-Analyser\\logs"
DATA_DIR="D:\\Cybersecurity-Log-Analyser\\data"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# ------------------- UI ROUTES -------------------

@app.route('/')
def index():
    logs = get_logs_for_dashboard(limit=10)
    labels, data = get_log_chart_data()  # Existing log chart (maybe line graph)

    # Load real-time log type counts from c_{logtype}.txt files
    log_types = ['application', 'network', 'firewall', 'authentication']
    log_type_counts = {}

    for log_type in log_types:
        count_file = os.path.join(DATA_DIR, f'c_{log_type.lower()}.txt')
        if os.path.exists(count_file):
            with open(count_file, 'r') as f:
                try:
                    log_type_counts[log_type.capitalize()] = int(f.read().strip())
                except:
                    log_type_counts[log_type.capitalize()] = 0
        else:
            log_type_counts[log_type.capitalize()] = 0

    return render_template('index.html',
                           logs=logs,
                           log_chart_labels=labels,
                           log_chart_data=data,
                           log_type_counts=log_type_counts)

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')



@app.route('/api/overview')
def get_overview_data():
    return jsonify({
        'total_logs': get_total_logs(),  # Replace with your actual logic
        'total_alerts': get_total_alerts(),
    })

# ------------------- API ROUTES -------------------

@app.route('/get_alerts', methods=['GET'])
def get_alerts_route():
    try:
        alerts = []
        with sqlite3.connect(ALERTS_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, message FROM alerts ORDER BY timestamp DESC")
            alerts = [{"timestamp": row[0], "message": row[1]} for row in cursor.fetchall()]
        return jsonify(alerts)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_logs', methods=['GET'])
def get_logs_route():
    try:
        logs = []
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, ip, message FROM logs ORDER BY timestamp DESC")
            logs = [{"timestamp": row[0], "ip": row[1], "message": row[2]} for row in cursor.fetchall()]
        return jsonify(logs)
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/total_stats', methods=['GET'])
def get_total_stats():
    system_overview = get_system_overview()
    return jsonify(system_overview)

@app.route('/api/alerts', methods=['GET'])
def api_alerts():
    alerts = get_alerts()
    return jsonify(alerts)

@app.route('/api/logs', methods=['GET'])
def api_logs():
    logs = get_logs()
    return jsonify(logs)

@app.route('/api/log_chart', methods=['GET'])
def api_log_chart():
    labels, values = get_logs_per_minute()
    return jsonify({"labels": labels, "values": values})


# ------------------- INTERNAL DATA FUNCTIONS -------------------

def get_system_overview():
    total_logs = get_total_logs()
    total_alerts = get_total_alerts()
    active_ip_blocks = fetch_active_ip_blocks()
    return {
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "active_ip_blocks": active_ip_blocks
    }

def fetch_active_ip_blocks():
    # Placeholder logic, replace with actual blocklist checking
    return 5

def get_threat_category_breakdown():
    # Static data; update with real-time calculations if needed
    return {
        "Application Threat": 15,
        "Authentication Threat": 7,
        "Firewall Threat": 10,
        "Network Threat": 12
    }

def get_logs_for_dashboard(limit=10):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, ip, message FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [{"timestamp": row[0], "ip": row[1], "message": row[2]} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logging.error(f"Error fetching logs for dashboard: {e}")
        return []

def get_log_chart_data():
    # Get real-time data from get_logs_per_minute
    labels, values = get_logs_per_minute()
    return labels, values

def get_log_type_distribution():
    log_type_keywords = {
        "Application Threat": ["APPLICATION"],
        "Authentication Threat": ["AUTHENTICATION"],
        "Firewall Threat": ["FIREWALL"],
        "Network Threat": ["NETWORK"]
    }


    log_counts = defaultdict(int)

    try:
        for filename in os.listdir(LOGS_FOLDER):
            if filename.endswith(".txt"):
                file_path = os.path.join(LOGS_FOLDER, filename)
                with open(file_path, "r") as file:
                    for line in file:
                        line_upper = line.upper()
                        matched = False
                        for threat_type, keywords in log_type_keywords.items():
                            if any(keyword in line_upper for keyword in keywords):
                                log_counts[threat_type] += 1
                                matched = True
                                break
                        if not matched:
                            log_counts["Other"] += 1
    except Exception as e:
        logging.error(f"Error reading log types: {e}")

    # Convert to sorted dict
    return dict(sorted(log_counts.items(), key=lambda item: item[0]))


# ------------------- START SERVER -------------------

if __name__ == '__main__':
    logging.info("🚀 Starting Flask Web Server...")
    app.run(debug=True, port=5000)
