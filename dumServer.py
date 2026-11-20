'''
Date: 20-11-2026
Made by: Google Bard
Copied by: @billals351
Name: dumServer.py
Purpose: Made to test custom headers on requests sent by CURL.
and log headers.
'''

from datetime import datetime
import http.server
from pathlib import Path
import socketserver

PORT = 8000
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "server.log"


class LoggingHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        custom_header = self.headers.get("X-Custom-Header")
        all_headers = dict(self.headers)
        message = format % args

        entry = (
            f"[{timestamp}] {self.address_string()} - {message} | "
            f"X-Custom-Header={custom_header!r} | Headers={all_headers}"
        )

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(entry)

        print(entry, end="", flush=True)


with socketserver.TCPServer(("", PORT), LoggingHandler) as httpd:
    print(f"Serving at port {PORT}, logging to {LOG_FILE.resolve()}", flush=True)
    # Start the server and keep it running until you stop the script
    httpd.serve_forever()