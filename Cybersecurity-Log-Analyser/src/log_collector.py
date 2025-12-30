import os
import time
import threading
import logging

# Define project log directories
PROJECT_DIR = "D:\\Cybersecurity-Log-Analyser"
LOG_DIR = os.path.join(PROJECT_DIR, "Generated-Logs")
LOGW_DIR = os.path.join(PROJECT_DIR, "logs")

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(LOGW_DIR, exist_ok=True)

# Log files for each type of log (Generated Logs)
LOG_FILES = {
    "network": os.path.join(LOG_DIR, "network.log"),
    "application": os.path.join(LOG_DIR, "application.log"),
    "authentication": os.path.join(LOG_DIR, "authentication.log"),
    "firewall": os.path.join(LOG_DIR, "firewall.log"),
}

# Log files for collected logs (Saved Logs)
LOGW_FILES = {
    log_type: os.path.join(LOGW_DIR, f"{log_type}.log") for log_type in LOG_FILES
}




def read_logs(log_file, lines=20):
    """Read the last 'n' lines from a log file."""
    try:
        with open(log_file, "r") as file:
            return "".join(file.readlines()[-lines:])
    except FileNotFoundError:
        return f"Error: {log_file} not found."
    except Exception as e:
        return f"Error reading {log_file}: {str(e)}"


def collect_logs(log_type):
    """Collect logs from generated log files instead of system commands."""
    log_file = LOG_FILES.get(log_type)
    if not log_file:
        return f"Error: Log type {log_type} not found."

    return read_logs(log_file)


def save_logs(log_data, log_type):
    """Save logs to a specific file inside project/logs/."""
    log_file = LOGW_FILES.get(log_type)
    if not log_file:
        logging.error(f"Error: No log file defined for {log_type}")
        return

    try:
        with open(log_file, "a") as file:
            file.write(log_data + "\n")
    except Exception as e:
        logging.error(f"Error saving logs for {log_type}: {e}")


def schedule_log_collection(log_type, interval):
    """Continuously collect logs at a specified interval."""
    while True:
        print(f"🔍 Collecting {log_type} logs from file...")
        logs = collect_logs(log_type)
        if not logs.startswith("Error"):
            save_logs(logs, log_type)
            print(f"✅ {log_type.capitalize()} logs updated in: {LOGW_FILES[log_type]}")
        else:
            print(logs)  # Print errors
        time.sleep(interval)


if __name__ == "__main__":
    log_intervals = {
        "firewall": 10,
        "network": 10,
        "authentication": 10,
        "application": 10,
    }

    # Start threads for different log collections
    for log_type, interval in log_intervals.items():
        threading.Thread(target=schedule_log_collection, args=(log_type, interval), daemon=True).start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n❌ Log Collector Stopped.")
