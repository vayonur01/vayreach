from http.server import BaseHTTPRequestHandler
import json, os

DB_FILE = os.path.join(os.path.dirname(__file__), "../db.json")

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def handler(request):
    length = int(request.headers.get("content-length", 0))
    body = json.loads(request.rfile.read(length))
    computer = body.get("computer")

    db = load_db()
    bans = db.get("bans", [])
    if computer not in bans:
        bans.append(computer)
    db["bans"] = bans
    save_db(db)

    request.send_response(200)
    request.send_header("Content-Type", "application/json")
    request.end_headers()
    request.wfile.write(json.dumps({"success": True}).encode())