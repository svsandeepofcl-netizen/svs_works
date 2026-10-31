# Headless Naukri Profile Updater

An automated, headless Python bot powered by Playwright and Stealth to keep your Naukri profile active and updated.

## Features
- **Headless Execution**: Runs silently in the background.
- **Dedicated Virtual Environment**: Runs entirely inside `naukri_venv`.
- **Anti-Detection**: Built with `playwright-stealth` and real Chrome browser arguments.
- **Robust Profile Touching**: Updates the Resume Headline (safely toggling a trailing dot) or Profile Summary to refresh the "Profile last updated" timestamp on Naukri.
- **Automated Logging**:
  - `logs/naukri_updater.log`: Cumulative log of all executions.
  - `logs/naukri_YYYY-MM-DD.log`: Daily log file.
  - `logs/screenshots/`: Automated visual captures for login, profile state, and any errors.
- **One-Click Launchers**: `run.bat` and `run.ps1`.

## Project Structure
```
Naukri/
├── .credentials          # Stored login credentials (email & password)
├── config.py             # Configuration and environment loader
├── logger.py             # Dual console/file logger and screenshot manager
├── main.py               # CLI entrypoint
├── naukri_updater.py     # Playwright automation engine
├── requirements.txt      # Project dependencies
├── run.bat               # Windows batch launcher (uses naukri_venv)
├── run.ps1               # PowerShell launcher (uses naukri_venv)
├── naukri_venv/          # Dedicated Python virtual environment
└── logs/                 # Auto-generated runtime logs & screenshots
    ├── naukri_updater.log
    └── screenshots/
```

## How to Run

### Option 1: Quick Batch Script (Recommended for Windows / Task Scheduler)
Double-click `run.bat` or run in terminal:
```cmd
run.bat
```

### Option 2: Using the Dedicated Virtual Environment directly
```cmd
naukri_venv\Scripts\python.exe main.py
```

### Option 3: Debug Mode (Visible Browser)
If you want to watch the browser actions live:
```cmd
naukri_venv\Scripts\python.exe main.py --headful
```

