import os
import sys
import logging
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = LOGS_DIR / "screenshots"


def setup_logger(name: str = "NaukriUpdater") -> logging.Logger:
    """Configures and returns a logger instance that outputs to both

    console and log files in the 'logs' directory.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if setup_logger is called repeatedly
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Main log file (persistent append across runs)
    main_log_file = LOGS_DIR / "naukri_updater.log"
    file_handler = logging.FileHandler(main_log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. Per-day log file for easy auditing
    date_str = datetime.now().strftime("%Y-%m-%d")
    daily_log_file = LOGS_DIR / f"naukri_{date_str}.log"
    daily_handler = logging.FileHandler(daily_log_file, encoding="utf-8")
    daily_handler.setLevel(logging.INFO)
    daily_handler.setFormatter(formatter)
    logger.addHandler(daily_handler)

    # 3. Stream / Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_screenshot_path(name: str) -> str:
    """Generates a timestamped screenshot path inside logs/screenshots/."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)
    return str(SCREENSHOTS_DIR / f"{timestamp}_{clean_name}.png")

