import time
import random
import os

# Define log file path
log_file = "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\network.log"

# Ensure the log directory exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Sample log messages (wrapped all in lambdas for consistency)
cpu_logs = [
    lambda: f"CPU usage exceeded {random.randint(90, 100)}%",
    lambda: f"High CPU usage detected on core {random.randint(0, 7)}",
    lambda: "CPU temperature exceeded safe limit"
]

memory_logs = [
    lambda: f"Memory usage crossed {random.randint(90, 99)}%",
    lambda: "Swap memory exhausted",
    lambda: "Process killed due to out-of-memory condition"
]

disk_logs = [
    lambda: "Disk read error on /dev/sda",
    lambda: "Filesystem corruption detected on /dev/sdb",
    lambda: "SSD wear level critical - Replace drive soon",
    lambda: "Unexpected disk disconnection detected"
]

kernel_logs = [
    lambda: "Kernel panic detected - System halted",
    lambda: "Unrecoverable hardware error encountered",
    lambda: "Unauthorized process execution detected",
    lambda: "System reboot initiated due to critical failure"
]

process_logs = [
    lambda: "Unauthorized process execution detected",
    lambda: "New process spawned: /usr/bin/unknown",
    lambda: "Service 'nginx' restarted due to failure",
    lambda: "Process 'python' consuming excessive resources"
]

def generate_system_logs():
    """Continuously generate realistic system logs."""
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_category = random.choice(["CPU", "MEMORY", "DISK", "KERNEL", "PROCESS"])

        if log_category == "CPU":
            message = random.choice(cpu_logs)()
        elif log_category == "MEMORY":
            message = random.choice(memory_logs)()
        elif log_category == "DISK":
            message = random.choice(disk_logs)()
        elif log_category == "KERNEL":
            message = random.choice(kernel_logs)()
        else:
            message = random.choice(process_logs)()

        log_entry = f"{timestamp} | NETWORK | {log_category} | {message}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

        print(log_entry.strip())  # Debugging
        time.sleep(random.randint(2, 5))  # Random delay between log entries

# Run the log generator
generate_system_logs()
