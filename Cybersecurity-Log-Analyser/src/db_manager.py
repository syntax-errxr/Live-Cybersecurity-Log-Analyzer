import sqlite3
import os
from collections import defaultdict
from datetime import datetime,timedelta

# Define project directories
PROJECT_DIR = "D:\\Cybersecurity-Log-Analyser"
DATA_DIR = os.path.join(PROJECT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "logs.db")
ALERT_PATH = os.path.join(DATA_DIR, "alerts.db")

os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data directory exists


def create_database():
    """Create logs table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ip TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        conn.commit()


def create_database_alert():
    """Create alert table if it doesn't exist."""
    with sqlite3.connect(ALERT_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        conn.commit()


def insert_log(timestamp, ip, message):
    """Insert a log entry into the database, handling missing IPs."""
    try:
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            ip_value = ip if ip else "N/A"
            cursor.execute("INSERT INTO logs (timestamp, ip, message) VALUES (?, ?, ?)",
                           (timestamp, ip_value, message))
            conn.commit()
    except sqlite3.Error as e:
        print(f"⚠ Database error (log insert): {e}")


def insert_log_alert(timestamp, message):
    """Insert an alert entry into the database."""
    try:
        with sqlite3.connect(ALERT_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO alerts (timestamp, message) VALUES (?, ?)",
                           (timestamp, message))
            conn.commit()
    except sqlite3.Error as e:
        print(f"⚠ Database error (alert insert): {e}")


def get_logs(last_id=0):
    """Fetch new logs from the database after the last processed ID."""
    try:
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, ip, message FROM logs WHERE id > ? ORDER BY id ASC", (last_id,))
            logs = cursor.fetchall()
            return logs
    except sqlite3.Error as e:
        print(f"⚠ Database error (get_logs): {e}")
        return []


def get_alerts(last_id=0):
    """Fetch new alerts from the database after the last processed ID."""
    try:
        with sqlite3.connect(ALERT_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, message FROM alerts WHERE id > ? ORDER BY id ASC", (last_id,))
            alerts = cursor.fetchall()
            return alerts
    except sqlite3.Error as e:
        print(f"⚠ Database error (get_alerts): {e}")
        return []


# 🔥 NEW FUNCTIONS for real-time dashboard

def get_total_logs():
    """Return total log count."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM logs")
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"⚠ Database error (get_total_logs): {e}")
        return 0


def get_total_alerts():
    """Return total alert count."""
    try:
        with sqlite3.connect(ALERT_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alerts")
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"⚠ Database error (get_total_alerts): {e}")
        return 0


def get_suspicious_ip_count():
    """Return count of IPs that appear more than once."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ip FROM logs")
            ip_list = [row[0] for row in cursor.fetchall()]
            freq = defaultdict(int)
            for ip in ip_list:
                freq[ip] += 1
            return sum(1 for ip in freq if freq[ip] > 1)
    except sqlite3.Error as e:
        print(f"⚠ Database error (get_suspicious_ip_count): {e}")
        return 0


def get_logs_per_minute():
    """Returns log count per minute for the last 60 minutes."""
    try:
        cutoff = datetime.now() - timedelta(minutes=60)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp FROM logs")
            raw = cursor.fetchall()
            minutes = defaultdict(int)

            for (ts,) in raw:
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                    if dt >= cutoff:
                        minute_label = dt.strftime("%H:%M")
                        minutes[minute_label] += 1
                except Exception:
                    continue

            sorted_data = sorted(minutes.items())
            labels = [item[0] for item in sorted_data]
            values = [item[1] for item in sorted_data]
            return labels, values

    except sqlite3.Error as e:
        print(f"⚠ Database error (get_logs_per_minute): {e}")
        return [], []


if __name__ == "__main__":
    create_database()
    create_database_alert()
    print("✅ Databases initialized successfully.")
