import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from flask import Flask
from flask_socketio import SocketIO
import threading
import random  # For testing without a real database

# Flask App Setup
server = Flask(__name__)
socketio = SocketIO(server, cors_allowed_origins="*")

# Dash App Setup
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dashboard/")

# Live Data Storage
log_data = pd.DataFrame(columns=["timestamp", "ip", "event"])
alert_data = []

# Layout for Dashboard
app.layout = html.Div([
    html.H1("🔍 Real-Time Cybersecurity Dashboard"),
    
    dcc.Graph(id="live-log-chart"),
    dcc.Interval(id="interval-update", interval=2000, n_intervals=0),  # Auto-update every 2 sec
    
    html.H3("📢 Live Alerts"),
    html.Div(id="live-alerts", style={"whiteSpace": "pre-line", "fontSize": "16px"}),
])

# Function to Update Live Chart
@app.callback(
    dash.dependencies.Output("live-log-chart", "figure"),
    [dash.dependencies.Input("interval-update", "n_intervals")]
)
def update_chart(n):
    if log_data.empty:
        return px.bar(title="No Logs Yet", labels={"count": "Occurrences"})

    event_counts = log_data["event"].value_counts()
    fig = px.bar(
        x=event_counts.index, 
        y=event_counts.values, 
        labels={"x": "Event Type", "y": "Occurrences"},
        title="Threat Events Over Time",
        color=event_counts.index
    )
    return fig

# Function to Update Live Alerts
@app.callback(
    dash.dependencies.Output("live-alerts", "children"),
    [dash.dependencies.Input("interval-update", "n_intervals")]
)
def update_alerts(n):
    return "\n".join(alert_data[-5:])  # Show last 5 alerts


# WebSocket Listener for New Logs
@socketio.on("new_log")
def handle_new_log(log):
    global log_data
    timestamp, ip, message = log[1], log[2], log[3]
    
    # Identify Threat Type
    event_type = "Other"
    if "failed login" in message.lower():
        event_type = "Failed Login"
    elif "scan" in message.lower():
        event_type = "Port Scan"
    elif "iptables" in message.lower() or "firewall" in message.lower():
        event_type = "Firewall Change"
    
    # Update DataFrame
    log_data = pd.concat([log_data, pd.DataFrame([[timestamp, ip, event_type]], columns=log_data.columns)], ignore_index=True)

@socketio.on("new_alert")
def handle_new_alert(alert):
    alert_data.append(alert)


# Start Flask-SocketIO
def run_socketio():
    socketio.run(server, debug=True, port=8050, use_reloader=False)

# Run Everything
if __name__ == "__main__":
    threading.Thread(target=run_socketio).start()
    app.run_server(debug=True, port=8051, use_reloader=False)
