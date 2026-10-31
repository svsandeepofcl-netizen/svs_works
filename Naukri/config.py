import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / ".credentials"

# Load .credentials if it exists
if CREDENTIALS_FILE.exists():
    load_dotenv(dotenv_path=CREDENTIALS_FILE)

# Credentials extraction with fallback
def get_credentials():
    email = os.getenv("NAUKRI_EMAIL") or os.getenv("NAUKRI_USERNAME")
    password = os.getenv("NAUKRI_PASSWORD")

    # Manual fallback parser for .credentials file if dotenv didn't catch it
    if (not email or not password) and CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip().upper()
                    val = val.strip().strip("'\"")
                    if key in ("NAUKRI_EMAIL", "NAUKRI_USERNAME", "EMAIL", "USERNAME") and not email:
                        email = val
                    elif key in ("NAUKRI_PASSWORD", "PASSWORD") and not password:
                        password = val

    return email, password

# URLs
LOGIN_URL = "https://www.naukri.com/nlogin/login"
HOMEPAGE_URL = "https://www.naukri.com/mnjuser/homepage"
PROFILE_URL = "https://www.naukri.com/mnjuser/profile"

# Target Resume Headline
TARGET_RESUME_HEADLINE = os.getenv("TARGET_RESUME_HEADLINE", "Python Developer")

# Browser Configuration
HEADLESS = True
BROWSER_TIMEOUT_MS = 45000
NAVIGATION_TIMEOUT_MS = 60000
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

