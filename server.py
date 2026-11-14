"""Minimal reference implementation of the Orqen external-capability contract.

Copy this file as the starting point for wrapping any repo as an Orqen
`tool.external` / `tool.custom.*` capability. Orqen's Rust engine will POST
here with `{"input": "<text>"}` and expects back `{"result": "<text>"}`.
Replace the body of `handle(text)` with a call into whatever the wrapped
repo actually does (import its library, shell out to its CLI, etc.) --
that logic runs inside this container, never inside Orqen itself.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

MAX_BODY_BYTES = 1_048_576


def handle(text: str) -> str:
    # Replace this with the wrapped repo's real logic.
    return text[::-1]


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY_BYTES:
            self.send_response(413)
            self.end_headers()
            return
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = handle(str(payload.get("input", "")))
            body = json.dumps({"result": result}).encode()
        except Exception as error:  # noqa: BLE001 - surface failure to Orqen as JSON
            body = json.dumps({"error": str(error)}).encode()
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Used by Orqen's "Test connection" probe -- any response counts as reachable.
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9321"))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
