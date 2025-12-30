import time
import random
import os

# Define the log file path
log_file = "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\application.log"

# Ensure the log directory exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Sample data for logs
users = ["admin", "user1", "user2", "guest"]
ips = ["192.168.1.10", "192.168.1.25", "10.0.0.5", "172.16.0.100", "203.0.113.45"]
events = [
    "User logged in", "User logged out", "Invalid password attempt", 
    "Password changed", "Session timeout", "Two-factor authentication enabled",
    "Database connection failed", "SQL Injection attempt detected", 
    "Unauthorized API access attempt", "Application restarted",
    "Server overload detected", "App crashed due to memory leak", 
    "New user registered", "Database entry updated", "Data export initiated"
]

def generate_application_logs():
    """Continuously generate realistic application logs."""
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        user = random.choice(users)
        ip = random.choice(ips)
        event = random.choice(events)

        log_entry = f"{timestamp} | APPLICATION | USER: {user} | IP: {ip} | EVENT: {event}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

        print(log_entry.strip())  # Debugging
        time.sleep(random.randint(2, 5))  # Random delay between log entries

# Run the log generator
generate_application_logs()
