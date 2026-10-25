#!/usr/bin/env python3
"""
SysInfo Local Web Server (web_server.py)
Lightweight HTTP server serving the modern SysInfo dashboard and real-time JSON API.
No external web frameworks required (uses Python standard library ThreadingHTTPServer).
"""

import argparse
import json
import mimetypes
import os
import sys
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sysinfo.collector import collect_all_system_info

WEB_DIR = os.path.join(PROJECT_ROOT, "web")


class SysInfoWebHandler(SimpleHTTPRequestHandler):
    """Handles static web asset delivery and dynamic /api/stats JSON requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self) -> None:
        # Route: API stats
        if self.path == "/api/stats" or self.path.startswith("/api/stats?"):
            self.send_api_stats()
            return

        # Route: Default to index.html for root path
        if self.path in ("/", ""):
            self.path = "/index.html"

        super().do_GET()

    def send_api_stats(self) -> None:
        """Collect current system metrics and return as JSON."""
        try:
            data = collect_all_system_info()
            payload = json.dumps(data, default=str).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
        except Exception as e:
            err_msg = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(err_msg)))
            self.end_headers()
            self.wfile.write(err_msg)

    def log_message(self, format: str, *args) -> None:
        # Suppress verbose asset request logging to keep console clean; only log errors
        if len(args) > 1 and str(args[1]).startswith("4"):
            super().log_message(format, *args)


def run_server(host: str = "127.0.0.1", port: int = 5000, open_browser: bool = True) -> None:
    """Start the multi-threaded HTTP server and launch browser."""
    # Find next available port if port is already in use
    server = None
    target_port = port
    max_retries = 10

    for offset in range(max_retries):
        try_port = target_port + offset
        try:
            server = ThreadingHTTPServer((host, try_port), SysInfoWebHandler)
            target_port = try_port
            break
        except OSError:
            continue

    if server is None:
        print(f"[!] Could not bind to port {port} or next {max_retries} ports. Is another server running?", file=sys.stderr)
        sys.exit(1)

    url = f"http://localhost:{target_port}"
    print("=" * 64)
    print("           SYSINFO LIVE WEB DASHBOARD IS RUNNING")
    print("=" * 64)
    print(f"  • Local Web UI:    {url}")
    print(f"  • Live JSON API:   {url}/api/stats")
    print("  • Press Ctrl+C in terminal to stop the server.")
    print("=" * 64)

    if open_browser:
        def _launch():
            time.sleep(0.5)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=_launch, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[✓] Web server stopped cleanly.")
    finally:
        server.server_close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the SysInfo Local Web Server.")
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind the server on (default: 5000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind on (default: 127.0.0.1 / localhost)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open the default web browser",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    run_server(host=args.host, port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
