from http.server import BaseHTTPRequestHandler
import json, os

DB_FILE = os.path.join(os.path.dirname(__file__), "../db.json")

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def handler(request):
    length = int(request.headers.get("content-length", 0))
    body = json.loads(request.rfile.read(length))
    computer = body.get("computer")

    db = load_db()
    banned = computer in db.get("bans", [])
    response = {"banned": banned}

    request.send_response(200)
    request.send_header("Content-Type", "application/json")
    request.end_headers()
    request.wfile.write(json.dumps(response).encode())