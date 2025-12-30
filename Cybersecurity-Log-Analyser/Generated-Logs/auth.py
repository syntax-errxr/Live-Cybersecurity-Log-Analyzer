import time
import random
import os

# Define the log file path
log_file = "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\authentication.log"

# Ensure the log directory exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Sample data for logs
users = ["admin", "root", "guest", "user1", "devops", "support"]
ips = ["192.168.1.5", "10.0.0.3", "203.0.113.10", "8.8.4.4", "45.33.29.100", "185.199.108.153"]
statuses = ["SUCCESS", "FAILED", "INVALID PASSWORD", "ACCOUNT LOCKED", "MFA REQUIRED"]
methods = [
    "Exploit Attempt",
    "Unauthorized Access Attempt",
    "Compromised IoT Device",
    "MFA Bypassed",
    "SQL Injection",
    "Cross-Site Scripting (XSS)",
    "Brute Force Attack",
    "Phishing Attempt",
    "Ransomware Detected",
    "Malware Execution",
    "DDoS Attack",
    "Privilege Escalation",
    "Zero-Day Exploit",
    "Insider Threat",
    "Suspicious Network Activity",
    "Anomalous Login Location",
    "Data Exfiltration",
    "Unpatched Vulnerability",
    "Command and Control (C2) Communication",
    "Suspicious File Upload"
]

devices = ["Windows 10", "Ubuntu 22.04", "iPhone", "Android", "MacOS", "Unknown Device"]
mfa_status = ["MFA Passed", "MFA Failed", "MFA Not Configured"]

def generate_auth_logs():
    """Continuously generate realistic authentication logs."""
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        user = random.choice(users)
        ip = random.choice(ips)
        status = random.choice(statuses)
        method = random.choice(methods)
        device = random.choice(devices)
        mfa = random.choice(mfa_status)

        log_entry = (
            f"{timestamp} | AUTHENTICATION | User: {user} | IP: {ip} | Method: {method} \n"
        )

        with open(log_file, "a") as f:
            f.write(log_entry)

        print(log_entry.strip())  # Debugging
        time.sleep(random.randint(2, 5))  # Random delay between log entries

# Run the log generator
generate_auth_logs()
