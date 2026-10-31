#!/usr/bin/env python3
"""
Jungle Viper - Launcher (start.py)
Starts the local game server and opens the browser to play.
Supports:
    python start.py          # Launches browser game at http://localhost:5500
    python start.py --gui    # Launches native desktop Tkinter game window
"""

import argparse
import os
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

GAME_DIR = os.path.dirname(os.path.abspath(__file__))


class GameHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=GAME_DIR, **kwargs)

    def log_message(self, format, *args):
        # Keep terminal clean
        pass


def run_web_game(port: int = 5500, open_browser: bool = True) -> None:
    server_address = ("127.0.0.1", port)
    
    # Try preferred port, increment if busy
    actual_port = port
    server = None
    for attempt in range(10):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", actual_port), GameHTTPHandler)
            break
        except OSError:
            actual_port += 1

    if not server:
        print(f"[!] Could not bind to port {port} or next 10 ports.", file=sys.stderr)
        return

    url = f"http://localhost:{actual_port}/index.html"
    print("=" * 64)
    print("             🌿 JUNGLE VIPER - SNAKE GAME 🌿")
    print("=" * 64)
    print(f"  • Local Game URL:  {url}")
    print("  • Controls:        Arrow Keys (Up, Down, Left, Right)")
    print("  • Goal:            Eat tropical fruit, grow longer, don't bite tail!")
    print("  • Press Ctrl+C in terminal to stop the server.")
    print("=" * 64)

    if open_browser:
        def _open():
            threading.Event().wait(0.5)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[✓] Jungle Viper game server stopped.")
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Jungle Viper Snake Game Launcher")
    parser.add_argument("--port", type=int, default=5500, help="Port to run web server on (default: 5500)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    parser.add_argument("--gui", action="store_true", help="Launch native desktop Tkinter GUI game")

    args = parser.parse_args()

    if args.gui:
        import desktop_game
        desktop_game.main()
    else:
        run_web_game(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
