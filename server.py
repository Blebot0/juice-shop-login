#!/usr/bin/env python3
"""Login page server. Repeats the browser checks and never builds a SQL string."""

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8080


def validate(email, password):
    if not isinstance(email, str) or not isinstance(password, str):
        return "Email and password are required."
    email = email.strip()
    if email == "" or password == "":
        return "Email and password are required."
    if "@" not in email:
        return "Email must contain @."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; form-action 'self'",
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_POST(self):
        if self.path != "/login":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"ok": False, "message": "Invalid request."})
            return

        if not isinstance(data, dict):
            self._json(400, {"ok": False, "message": "Invalid request."})
            return

        error = validate(data.get("email", ""), data.get("password", ""))
        if error:
            self._json(400, {"ok": False, "message": error})
            return

        # No account database. Fail closed instead of trusting the client.
        self._json(401, {"ok": False, "message": "Invalid email or password."})

    def _json(self, status, body):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    print(f"Serving on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
