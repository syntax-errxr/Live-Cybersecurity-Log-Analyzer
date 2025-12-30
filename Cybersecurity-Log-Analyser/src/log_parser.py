import os
import re
import time
import threading
from datetime import datetime
from db_manager import insert_log  # Import database function

# Define project log directory
PROJECT_DIR = "D:\\Cybersecurity-Log-Analyser"
PAR_DIR = "D:\\Cybersecurity-Log-Analyser\\data"
LOG_DIR = os.path.join(PROJECT_DIR, "logs")
PARSED_LOG_FILE = os.path.join(PAR_DIR, "parsed_summary.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Log files to monitor
LOG_FILES = {
    "network": os.path.join(LOG_DIR, "network.log"),
    "application": os.path.join(LOG_DIR, "application.log"),
    "authentication": os.path.join(LOG_DIR, "authentication.log"),
    "firewall": os.path.join(LOG_DIR, "firewall.log"),
}

# Ensure log files exist
for log_file in LOG_FILES.values():
    if not os.path.exists(log_file):
        open(log_file, "w").close()

# Ensure parsed log file exists
if not os.path.exists(PARSED_LOG_FILE):
    open(PARSED_LOG_FILE, "w").close()

# Patterns to detect threats
PATTERNS = {
    "Application Threat": re.compile(r"Brute force attack detected|Malware uploaded via api|Unauthorized root access attempt|Phishing attempt via user input|DDos attack detected on web server|Password changed", re.IGNORECASE),
    "Authentication Threat": re.compile(r"Exploit Attempt|Unauthorized access attempt|Compromised Iot Device|MFA bypassed", re.IGNORECASE),
    "Firewall Threat": re.compile(r"Unexpected Packet Loss|Port scanning|Brute force|Unrecognized source|Malware Signature Detected|Phishing Attempt|SQL Injection", re.IGNORECASE),
    "Network Threat": re.compile(r"Disk read error on /dev/sda|CPU usage exceeded 97%| SSD wear level critical - Replace drive soon| System reboot initiated due to critical failure| High CPU usage detected on core 4",re.IGNORECASE),
}

def tail_f(log_file):
    """Follow a log file for new lines, handling log rotation."""
    while True:
        try:
            with open(log_file, "r") as file:
                file.seek(0, os.SEEK_END)  # Move to end of file
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(1)  # Wait for new logs
                    else:
                        yield line.strip()
        except FileNotFoundError:
            time.sleep(1)  # Log rotation detected, retry opening

def parse_log_line(log_type, log_line):
    """Parse log lines, detect security alerts, and store them."""
    for pattern_name, pattern in PATTERNS.items():
        if pattern.search(log_line):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", log_line)
            ip = ip_match.group() if ip_match else "Unknown"
            alert = f"[{log_type.upper()}] {pattern_name.upper()}: {log_line}"

            print(alert)  # Show alert in console
            save_parsed_log(alert)  # Save to parsed_summary.log
            insert_log(timestamp, ip, log_line)  # Store in SQLite database

def save_parsed_log(alert):
    """Save security alerts to the parsed log file."""
    with open(PARSED_LOG_FILE, "a") as file:
        file.write(alert + "\n")
        file.flush()  # Ensure immediate writing

def watch_log(log_type, log_file):
    """Monitors a single log file in a separate thread."""
    for log_line in tail_f(log_file):
        parse_log_line(log_type, log_line)

def start_monitoring():
    """Starts monitoring logs in separate threads."""
    threads = []
    for log_type, path in LOG_FILES.items():
        thread = threading.Thread(target=watch_log, args=(log_type, path), daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("🚀 Monitoring logs in real-time...")
    start_monitoring()
