# Live Cybersecurity Log Analyzer

A live web application to parse, analyze, and visualize log files for potential security threats. Designed to help users, including non-CS users, monitor their security posture effectively in real-time.

---

## Features
- **Real-time Log Analysis:** Parses generated log files and detects anomalies using Python and Regex.
- **Notifications:** Sends alerts via Email and SMS using Twilio when suspicious activity is detected.
- **Dynamic Dashboard:** Visualizes logs and alerts using graphs and pie charts; auto-refresh updates for real-time monitoring.
- **User-Friendly:** Simplifies security monitoring for non-technical users, improving engagement and awareness.
- **Impact:** Approximately 80% of monitored activities are analyzed for early threat detection.

---

## Technologies Used
- **Backend:** Python, Flask, SQLite, Regex
- **Frontend:** HTML, CSS, JavaScript
- **Notifications:** Twilio (Email & SMS)

---

## Installation & Setup
1. Clone the repository:
2. Make sure the project folder "Cybersecurity-Log-Analyser" is in D drive.
    ```bash
    git clone https://github.com/yourusername/live-cybersecurity-log-analyzer.git
    cd live-cybersecurity-log-analyzer
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up Twilio credentials and Email configuration (if applicable).
5. Run the Flask app:
    ```bash
    python app.py
    ```
6. Open your browser and navigate to:
    ```
    http://localhost:5000
    ```

---

## Usage
- Just run script from src folder 
- View real-time updates on the dashboard.
- Receive instant alerts for any detected anomalies via email or SMS.
- How to use your credentials for update? Just make .env file in src and paste this :-
    ```
    EMAIL_SENDER=
    EMAIL_PASSWORD=Test0125@
    EMAIL_RECEIVER=
    TWILIO_SID=
    TWILIO_AUTH_TOKEN=38d1a3cdda7755b6824120a1c6d4ffbb
    TWILIO_PHONE=
    ADMIN_PHONE=
    ```
  
---


## Contact
Rohit Singh - rohit_2401me24@iitp.ac.in  
[GitHub](https://github.com/syntax-errxr)
