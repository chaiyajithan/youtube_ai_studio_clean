
import json
from datetime import datetime
import os

LOG_FILE = "logs.json"

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def log_usage(username, feature_name):
    logs = load_logs()
    logs.append({
        "username": username,
        "feature": feature_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_logs(logs)
