import time
import subprocess
import platform
from db_manager import get_logs
from alert_system import send_email_alert, send_sms_alert

# 🚀 Configurations
THREAT_THRESHOLD = 5  # Block IP if failed logins exceed this count
CHECK_INTERVAL = 2  # How often to check logs (seconds)
ip_attempts = {}  # Stores failed login attempts per IP

def block_ip(ip):
    """Automatically block an IP using firewall rules."""
    system = platform.system()
    
    try:
        if system == "Linux":
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        elif system == "Windows":
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockIP", "dir=in", "action=block", f"remoteip={ip}"], check=True)
        print(f"🚨 IP {ip} has been BLOCKED!")
    except Exception as e:
        print(f"⚠ Failed to block {ip}: {e}")

def analyze_logs():
    """Continuously fetch logs and detect suspicious IPs in real time."""
    last_id = 0  # Keep track of the last processed log ID

    print("🔍 Real-time Auto-Blocking System Started...")

    while True:
        logs = get_logs(last_id)
        if logs:
            for log_id, timestamp, ip, message in logs:
                if "failed login" in message.lower():
                    ip_attempts[ip] = ip_attempts.get(ip, 0) + 1
                    print(f"⚠ Suspicious Activity: {ip} ({ip_attempts[ip]} failed attempts)")

                    if ip_attempts[ip] >= THREAT_THRESHOLD:
                        send_email_alert(ip, ip_attempts[ip])  # Send alert
                        send_sms_alert(ip, ip_attempts[ip])  # Send SMS alert
                        block_ip(ip)  # Block IP
                        ip_attempts[ip] = 0  # Reset after blocking

                last_id = log_id  # Update last processed log ID
        
        time.sleep(CHECK_INTERVAL)  # Adjust for real-time analysis

if __name__ == "__main__":
    analyze_logs()
