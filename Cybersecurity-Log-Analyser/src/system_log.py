import os
import time
import threading
import subprocess
import logging

# Define project log directory
PROJECT_DIR = "D:\\Cybersecurity-Log-Analyser"
LOG_DIR = os.path.join(PROJECT_DIR, "logs")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Log files for each type of log
LOG_FILES = {
    "system": os.path.join(LOG_DIR, "system.log"),
    "network": os.path.join(LOG_DIR, "network.log"),
    "application": os.path.join(LOG_DIR, "application.log"),
    "authentication": os.path.join(LOG_DIR, "authentication.log"),
    "firewall": os.path.join(LOG_DIR, "firewall.log"),
}

# Configure logging
logging.basicConfig(filename=LOG_FILES["system"], level=logging.INFO, format="%(asctime)s - %(message)s")

def run_command(command):
    """Run a shell command and return the output, handling errors."""
    try:
        return subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"

def collect_system_logs():
    """Collect system logs based on the OS."""
    command = "dmesg | tail -n 50" if os.name == "posix" else "wevtutil qe System /c:50 /rd:true /f:text"
    return run_command(command)

def collect_network_logs():
    """Collect network connection logs."""
    return run_command("netstat -an")

def collect_application_logs():
    """Collect logs from web servers (Apache, Nginx) or custom applications."""
    logs = []
    paths = {
        "posix": ["/var/log/apache2/access.log", "/var/log/nginx/access.log"],
        "nt": ["C:\\xampp\\apache\\logs\\access.log", "C:\\nginx\\logs\\access.log"]
    }
    for log_path in paths.get(os.name, []):
        if os.path.exists(log_path):
            with open(log_path, "r") as file:
                logs.extend(file.readlines()[-20:])  # Get last 20 logs
    return "".join(logs) if logs else "No application logs found."

def collect_authentication_logs():
    """Collect authentication logs (Failed logins, sudo attempts)."""
    command = "cat /var/log/auth.log | tail -n 50" if os.name == "posix" else "wevtutil qe Security /c:50 /rd:true /f:text"
    return run_command(command)

def collect_firewall_logs():
    """Collect firewall logs (iptables or Windows Firewall)."""
    command = "sudo iptables -L -v -n | tail -n 50" if os.name == "posix" else "netsh advfirewall monitor show currentprofile"
    return run_command(command)

def save_logs(log_data, log_file):
    """Save logs to a specific file inside project/logs/."""
    try:
        with open(log_file, "a") as file:
            file.write(log_data + "\n")
    except Exception as e:
        logging.error(f"Error saving logs: {e}")

def schedule_log_collection(log_type, log_function, interval, duration):
    """Collect logs at a specified interval for a fixed duration."""
    start_time = time.time()
    while time.time() - start_time < duration:
        print(f"Collecting {log_type} logs...")
        save_logs(log_function(), LOG_FILES[log_type])
        print(f"{log_type.capitalize()} logs collected. Logs stored in: {LOG_FILES[log_type]}")
        time.sleep(interval)
    print(f"Stopping {log_type} log collection after {duration} seconds.")

if __name__ == "__main__":
    DURATION = 3600  # Set duration in seconds (e.g., 1 hour = 3600s, 24 hours = 86400s)

    # Start threads for different log collections at optimized intervals
    threading.Thread(target=schedule_log_collection, args=("firewall", collect_firewall_logs, 10, DURATION), daemon=True).start()
    threading.Thread(target=schedule_log_collection, args=("network", collect_network_logs, 20, DURATION), daemon=True).start()
    threading.Thread(target=schedule_log_collection, args=("authentication", collect_authentication_logs, 30, DURATION), daemon=True).start()
    threading.Thread(target=schedule_log_collection, args=("system", collect_system_logs, 120, DURATION), daemon=True).start()
    threading.Thread(target=schedule_log_collection, args=("application", collect_application_logs, 300, DURATION), daemon=True).start()

    # Keep the main thread running
    time.sleep(DURATION)  # Main thread waits for logs to be collected
    print("Log collection completed. Exiting program.")
