import time
import random
import os

# Define log file path
log_file = "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\firewall.log"

# Ensure the log directory exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Sample data for logs
actions = ["ALLOWED", "BLOCKED", "MALICIOUS", "DROPPED", "INTRUSION DETECTED"]
ips = ["192.168.1.20", "203.0.113.45", "10.10.10.2", "8.8.8.8", "185.199.110.153", "45.33.29.10"]
ports = [22, 80, 443, 3389, 8080, 25, 3306, 53, 5353]
protocols = ["TCP", "UDP", "ICMP", "DNS", "HTTP", "HTTPS"]
block_reasons = [
    "DDoS Attack",
    "Brute Force",
    "Port Scanning",
    "Unusual Traffic",
    "Unrecognized Source",
    "Malware Signature Detected",
    "Phishing Attempt",
    "SQL Injection",
    "Cross-Site Scripting (XSS)",
    "Unauthorized Access Attempt",
    "Excessive Failed Logins",
    "Suspicious User Agent",
    "Blacklisted IP",
    "Abnormal Request Frequency",
    "Privilege Escalation Attempt",
    "Ransomware Activity",
    "Data Exfiltration Detected",
    "Botnet Communication",
    "Unencrypted Sensitive Data Transmission",
    "Use of Deprecated Protocols"
]


def generate_firewall_logs():
    """Continuously generate realistic firewall logs."""
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        action = random.choice(actions)
        ip = random.choice(ips)
        port = random.choice(ports)
        protocol = random.choice(protocols)

        # If action is BLOCKED or MALICIOUS, add a reason
        reason = f" | Reason: {random.choice(block_reasons)}" if action in ["BLOCKED", "MALICIOUS", "INTRUSION DETECTED"] else ""

        log_entry = (
            f"{timestamp} | FIREWALL | Action: {action} | IP: {ip} | Port: {port} | Protocol: {protocol}{reason}\n"
        )

        with open(log_file, "a") as f:
            f.write(log_entry)

        print(log_entry.strip())  # Debugging
        time.sleep(random.randint(2, 5))  # Random delay between log entries

# Run the log generator
generate_firewall_logs()
