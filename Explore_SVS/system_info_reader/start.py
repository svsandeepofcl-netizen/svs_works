#!/usr/bin/env python3
"""
SysInfo Entrypoint (start.py)
Run this script to retrieve and display system metrics and hardware details.

Usage:
    python start.py                 # Displays the visual terminal dashboard
    python start.py --web           # Launches modern live web dashboard in browser
    python start.py --json          # Outputs structured JSON to terminal
    python start.py --save report   # Saves report to a file (.txt or .json)
    python start.py --no-color      # Disables ANSI color output
"""

import argparse
import json
import os
import sys

# Ensure UTF-8 output on Windows consoles to prevent charmap UnicodeEncodeErrors
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from sysinfo.collector import collect_all_system_info
from sysinfo.formatter import format_dashboard


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect and display system hardware, OS, and resource metrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print system information in structured JSON format",
    )
    parser.add_argument(
        "--save",
        type=str,
        metavar="FILEPATH",
        help="Save the output to a file (saves as JSON if .json extension, otherwise text)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color formatting in terminal output",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.3,
        help="CPU sampling interval in seconds (default: 0.3)",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch the interactive web UI dashboard on localhost",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for the web UI server (default: 5000)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open default browser when starting web UI",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if args.web:
        from web_server import run_server
        run_server(port=args.port, open_browser=not args.no_browser)
        return

    # Determine color support
    use_color = not args.no_color and sys.stdout.isatty()

    # Collect data
    data = collect_all_system_info()

    if args.json:
        output_content = json.dumps(data, indent=2)
        print(output_content)
    else:
        output_content = format_dashboard(data, use_color=use_color)
        print(output_content)

    # Optional file export
    if args.save:
        save_path = os.path.abspath(args.save)
        try:
            # If saving to file and not --json, save clean text without ANSI codes
            if save_path.lower().endswith(".json"):
                file_text = json.dumps(data, indent=2)
            else:
                file_text = format_dashboard(data, use_color=False)

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(file_text)
            print(f"[✓] System report saved successfully to: {save_path}")
        except Exception as e:
            print(f"[!] Error saving report to '{save_path}': {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
