import smtplib
import os
import dotenv
from email.mime.text import MIMEText
from twilio.rest import Client

# Load environment variables from .env file
dotenv.load_dotenv()

# Email credentials
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "rohitsingh30056@gmail.com")

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
ADMIN_PHONE = os.getenv("ADMIN_PHONE")

def send_email_alert(ip, count):
    """Send an email alert for suspicious activity."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("⚠️ Email credentials not set! Skipping email alert.")
        return
    
    subject = "⚠️ Security Alert: Suspicious IP Detected!"
    message = f"IP {ip} has attempted {count} failed logins!"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"📧 Email alert sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"❌ Email alert failed: {e}")
    finally:
        server.quit()

def send_sms_alert(ip, count):
    """Send an SMS alert for suspicious activity."""
    if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE, ADMIN_PHONE]):
        print("⚠️ Twilio credentials not set! Skipping SMS alert.")
        return

    message_body = f"⚠️ ALERT: IP {ip} attempted {count} failed logins!"

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE,
            to=ADMIN_PHONE
        )
        print(f"📲 SMS alert sent to {ADMIN_PHONE} (SID: {message.sid})")
    except Exception as e:
        print(f"❌ SMS alert failed: {e}")

if __name__ == "__main__":
    test_ip = "192.168.1.100"
    test_count = 10
    send_email_alert(test_ip, test_count)
    send_sms_alert(test_ip, test_count)
