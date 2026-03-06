from http.server import BaseHTTPRequestHandler
import json, os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "../db.json")

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def handler(request):
    db = load_db()
    users = db.get("users", [])
    now = datetime.now()
    for u in users:
        ts = datetime.fromisoformat(u["timestamp"])
        remaining = int(u["duration"]*3600 - (now - ts).total_seconds())
        u["status"] = "Active" if remaining > 0 else "Expired"
    request.send_response(200)
    request.send_header("Content-Type", "application/json")
    request.end_headers()
    request.wfile.write(json.dumps({"users": users}).encode())