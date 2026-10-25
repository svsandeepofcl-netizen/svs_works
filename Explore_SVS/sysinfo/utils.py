"""
Utility functions for formatting and unit conversions.
"""

from typing import Union


def format_bytes(bytes_value: Union[int, float], precision: int = 2) -> str:
    """
    Format a byte count into a human-readable string (B, KB, MB, GB, TB, PB).
    """
    if bytes_value is None or bytes_value < 0:
        return "N/A"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    value = float(bytes_value)
    unit_index = 0
    while value >= 1024.0 and unit_index < len(units) - 1:
        value /= 1024.0
        unit_index += 1
    return f"{value:.{precision}f} {units[unit_index]}"


def format_duration(seconds: Union[int, float]) -> str:
    """
    Format a duration in seconds into human-readable string (days, hours, minutes, seconds).
    """
    if seconds is None or seconds < 0:
        return "N/A"
    seconds = int(seconds)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


def format_frequency(mhz: Union[int, float]) -> str:
    """
    Format a frequency in MHz into MHz or GHz.
    """
    if mhz is None or mhz <= 0:
        return "N/A"
    if mhz >= 1000:
        return f"{mhz / 1000:.2f} GHz"
    return f"{mhz:.0f} MHz"


def make_progress_bar(percent: float, width: int = 20, fill_char: str = "█", empty_char: str = "░") -> str:
    """
    Create a text-based progress bar.
    """
    if percent is None:
        return f"[{empty_char * width}] N/A"
    percent = max(0.0, min(100.0, float(percent)))
    filled_len = int(round(width * percent / 100.0))
    bar = fill_char * filled_len + empty_char * (width - filled_len)
    return f"[{bar}] {percent:5.1f}%"
