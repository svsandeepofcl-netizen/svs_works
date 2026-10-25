"""
SysInfo - Modern System Information Retrieval Package
"""

from .collector import collect_all_system_info
from .formatter import format_dashboard

__all__ = ["collect_all_system_info", "format_dashboard"]
