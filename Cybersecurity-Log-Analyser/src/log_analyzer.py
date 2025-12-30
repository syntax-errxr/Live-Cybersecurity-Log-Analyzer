import time
import re
import logging
import os
from db_manager import get_logs, insert_log_alert
from alert_system import send_email_alert, send_sms_alert
from auto_block import block_ip

# Project paths
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Threat detection patterns
PATTERNS = {
    "Application Threat": re.compile(r"Brute force attack detected|Malware uploaded via api|Unauthorized root access attempt|Phishing attempt via user input|DDos attack detected on web server|Password changed", re.IGNORECASE),
    "Authentication Threat": re.compile(r"Exploit Attempt|Unauthorized access attempt|Compromised Iot Device|MFA bypassed", re.IGNORECASE),
    "Firewall Threat": re.compile(r"Unexpected Packet Loss|Port scanning|Brute force|Unrecognized source|Malware Signature Detected|Phishing Attempt|SQL Injection", re.IGNORECASE),
    "Network Threat": re.compile(r"Disk read error on /dev/sda|CPU usage exceeded 97%| SSD wear level critical - Replace drive soon| System reboot initiated due to critical failure| High CPU usage detected on core 4", re.IGNORECASE),
}

THREAT_THRESHOLD = 5
ip_attempts = {}

# Initialize in-memory counter
log_type_counter = {
    "APPLICATION": 0,
    "AUTHENTICATION": 0,
    "FIREWALL": 0,
    "NETWORK": 0
}


def update_logtype_file(log_type):
    """Update the specific log type file with the new count."""
    try:
        log_type = log_type.upper()
        file_path = os.path.join(DATA_DIR, f"c_{log_type}.txt")
        log_type_counter[log_type] += 1
        with open(file_path, "w") as f:
            f.write(str(log_type_counter[log_type]))
    except Exception as e:
        print(f"❌ Error updating logtype file for {log_type}: {e}")
        logging.error(f"Error updating logtype file for {log_type}: {e}")


def detect_log_type(message):
    """Extract log type like | APPLICATION | from log message."""
    match = re.search(r"\|\s*(APPLICATION|AUTHENTICATION|FIREWALL|NETWORK)\s*\|", message, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None


def analyze_logs():
    """Continuously fetch and analyze logs in real-time."""
    last_id = 0
    sleep_time = 2
    print("🔍 Real-time log analysis started...")

    while True:
        try:
            logs = get_logs(last_id)
            if logs:
                for log_id, timestamp, ip, message in logs:
                    process_log(timestamp, ip, message)
                    last_id = log_id
                sleep_time = 2
            else:
                sleep_time = min(sleep_time * 2, 10)
        except Exception as e:
            print(f"⚠ Error fetching logs: {e}")
            logging.error(f"Error fetching logs: {e}")
            sleep_time = 5

        time.sleep(sleep_time)


def process_log(timestamp, ip, message):
    """Detect threats and trigger alerts & blocking in real time."""
    threat_detected = False

    # Count and update per-log-type file
    log_type = detect_log_type(message)
    if log_type and log_type in log_type_counter:
        update_logtype_file(log_type)

    for pattern_name, pattern in PATTERNS.items():
        if pattern.search(message):
            alert_message = f"[ALERT:{pattern_name.upper()}] detected on {message}"
            print(alert_message)
            insert_log_alert(timestamp, alert_message)

            if pattern_name == "failed_login":
                ip_attempts[ip] = ip_attempts.get(ip, 0) + 1
                print(f"⚠ Suspicious Activity: {ip} ({ip_attempts[ip]} failed attempts)")

                if ip_attempts[ip] >= THREAT_THRESHOLD:
                    try:
                        send_email_alert(ip, ip_attempts[ip])
                        send_sms_alert(ip, ip_attempts[ip])
                        block_ip(ip)
                        print(f"🚫 IP Blocked: {ip}")
                        insert_log_alert(timestamp, f"🚫 IP Blocked: {ip} after {THREAT_THRESHOLD} failed attempts")
                    except Exception as alert_error:
                        print(f"❌ Error sending alerts or blocking IP: {alert_error}")
                        logging.error(f"Error sending alerts or blocking IP: {alert_error}")
                    ip_attempts[ip] = 0

            threat_detected = True

    if threat_detected:
        print("✅ Threat processed successfully!")


if __name__ == "__main__":
    analyze_logs()
