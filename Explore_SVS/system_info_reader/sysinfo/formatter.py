"""
Terminal Formatter
Formats system information into a rich, structured dashboard with ANSI colors,
tables, and visual progress indicators.
"""

import os
import sys
from typing import Any, Dict

from .utils import make_progress_bar


class Style:
    """ANSI color and styling codes with automatic disable support."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    @classmethod
    def enable_windows_ansi(cls) -> None:
        """Enable ANSI escape sequences on Windows consoles."""
        if os.name == "nt":
            os.system("")


def _color_percent(percent: float, text: str, use_color: bool = True) -> str:
    """Colorize a string based on threshold (green < 60, yellow 60-85, red > 85)."""
    if not use_color or percent is None:
        return text
    if percent < 60:
        return f"{Style.BRIGHT_GREEN}{text}{Style.RESET}"
    if percent < 85:
        return f"{Style.BRIGHT_YELLOW}{text}{Style.RESET}"
    return f"{Style.BRIGHT_RED}{text}{Style.RESET}"


def _badge(text: str, color: str, use_color: bool = True) -> str:
    """Format a styled badge."""
    if not use_color:
        return f"[{text}]"
    return f"{color}{Style.BOLD}[{text}]{Style.RESET}"


def format_dashboard(data: Dict[str, Any], use_color: bool = True, term_width: int = 76) -> str:
    """
    Generate the complete terminal dashboard string.
    """
    if use_color:
        Style.enable_windows_ansi()

    c_cyan = Style.BRIGHT_CYAN if use_color else ""
    c_blue = Style.BRIGHT_BLUE if use_color else ""
    c_bold = Style.BOLD if use_color else ""
    c_white = Style.BRIGHT_WHITE if use_color else ""
    c_dim = Style.DIM if use_color else ""
    c_green = Style.BRIGHT_GREEN if use_color else ""
    c_reset = Style.RESET if use_color else ""

    lines = []
    bar = "=" * term_width
    subbar = "-" * term_width

    # Header Banner
    lines.append(f"{c_cyan}{bar}{c_reset}")
    header_text = "SYSTEM INFORMATION DASHBOARD"
    lines.append(f"{c_bold}{c_white}{header_text.center(term_width)}{c_reset}")
    lines.append(f"{c_dim}{f'Generated on: {data.get('timestamp', '')}'.center(term_width)}{c_reset}")
    lines.append(f"{c_cyan}{bar}{c_reset}")

    # Section 1: OS & System Overview
    os_info = data.get("os", {})
    lines.append(f"\n{c_blue}{c_bold}  [1] OPERATING SYSTEM & HARDWARE OVERVIEW{c_reset}")
    lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")
    lines.append(f"    {c_bold}OS Name:{c_reset}         {os_info.get('system')} {os_info.get('release')} (Build {os_info.get('version')})")
    lines.append(f"    {c_bold}Architecture:{c_reset}    {os_info.get('architecture')}")
    lines.append(f"    {c_bold}Computer Name:{c_reset}   {os_info.get('hostname')}")
    lines.append(f"    {c_bold}Logged-in User:{c_reset}  {os_info.get('username')}")
    lines.append(f"    {c_bold}System Boot:{c_reset}     {os_info.get('boot_time')}")
    lines.append(f"    {c_bold}System Uptime:{c_reset}   {c_green}{os_info.get('uptime')}{c_reset}")

    # Section 2: CPU & Processor
    cpu_info = data.get("cpu", {})
    cpu_usage = cpu_info.get("usage_percent", 0.0)
    cpu_bar = make_progress_bar(cpu_usage, width=22)
    colored_cpu_bar = _color_percent(cpu_usage, cpu_bar, use_color)

    lines.append(f"\n{c_blue}{c_bold}  [2] PROCESSOR (CPU){c_reset}")
    lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")
    lines.append(f"    {c_bold}Model:{c_reset}           {cpu_info.get('brand')}")
    lines.append(f"    {c_bold}Cores & Threads:{c_reset} {cpu_info.get('physical_cores')} Physical Cores | {cpu_info.get('logical_cores')} Logical Threads")
    lines.append(f"    {c_bold}Clock Speed:{c_reset}     {cpu_info.get('frequency_current')} (Max: {cpu_info.get('frequency_max')})")
    lines.append(f"    {c_bold}Overall Usage:{c_reset}   {colored_cpu_bar}")

    # Per-core breakdown
    per_core = cpu_info.get("per_core_percent", [])
    if per_core and len(per_core) <= 16:
        core_chunks = []
        for idx, pct in enumerate(per_core):
            pct_str = f"C{idx:02d}: {pct:5.1f}%"
            colored_pct = _color_percent(pct, pct_str, use_color)
            core_chunks.append(colored_pct)
        # Format 4 cores per line
        lines.append(f"    {c_bold}Core Loads:{c_reset}")
        for i in range(0, len(core_chunks), 4):
            chunk = "   ".join(core_chunks[i:i + 4])
            lines.append(f"      {chunk}")

    # Section 3: Memory & RAM
    mem_info = data.get("memory", {})
    ram = mem_info.get("ram", {})
    swap = mem_info.get("swap", {})

    ram_pct = ram.get("percent", 0.0)
    ram_bar = make_progress_bar(ram_pct, width=22)
    colored_ram_bar = _color_percent(ram_pct, ram_bar, use_color)

    lines.append(f"\n{c_blue}{c_bold}  [3] MEMORY & STORAGE (RAM / SWAP){c_reset}")
    lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")
    lines.append(
        f"    {c_bold}Physical RAM:{c_reset}    {colored_ram_bar}  "
        f"({ram.get('used', '0 B')} used / {ram.get('total', '0 B')} total, {ram.get('available', '0 B')} free)"
    )

    if swap and swap.get("total_bytes", 0) > 0:
        swap_label = swap.get("label", "Swap / Pagefile")
        swap_pct = swap.get("percent", 0.0)
        swap_bar = make_progress_bar(swap_pct, width=22)
        colored_swap_bar = _color_percent(swap_pct, swap_bar, use_color)
        lines.append(
            f"    {c_bold}{swap_label}:{c_reset} {colored_swap_bar}  "
            f"({swap.get('used', '0 B')} used / {swap.get('total', '0 B')} total)"
        )

    # Section 4: Disk & Storage Drives
    disk_info = data.get("disk", {})
    partitions = disk_info.get("partitions", [])
    lines.append(f"\n{c_blue}{c_bold}  [4] DISK DRIVES & STORAGE{c_reset}")
    lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")

    if partitions:
        header_row = f"    {'Drive':<8} {'Type':<6} {'Total':<10} {'Used':<10} {'Free':<10} {'Usage'}"
        lines.append(f"{c_dim}{header_row}{c_reset}")
        for p in partitions:
            p_pct = p.get("percent", 0.0)
            p_bar = make_progress_bar(p_pct, width=12)
            colored_p_bar = _color_percent(p_pct, p_bar, use_color)
            lines.append(
                f"    {p.get('mountpoint', ''):<8} "
                f"{p.get('fstype', 'N/A'):<6} "
                f"{p.get('total', ''):<10} "
                f"{p.get('used', ''):<10} "
                f"{p.get('free', ''):<10} "
                f"{colored_p_bar}"
            )
    else:
        lines.append("    No disk partition information available.")

    disk_io = disk_info.get("io")
    if disk_io:
        lines.append(f"    {c_dim}Disk I/O Totals: Read {disk_io.get('read')} | Written {disk_io.get('write')}{c_reset}")

    # Section 5: Network Interfaces
    net_info = data.get("network", {})
    interfaces = net_info.get("interfaces", [])
    lines.append(f"\n{c_blue}{c_bold}  [5] NETWORK CONFIGURATION{c_reset}")
    lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")
    lines.append(f"    {c_bold}Hostname:{c_reset}         {net_info.get('hostname')}")
    lines.append(f"    {c_bold}Primary Local IP:{c_reset} {c_green}{net_info.get('primary_ip')}{c_reset}")

    # Prioritize active, connected interfaces
    up_ifaces = [iface for iface in interfaces if iface.get("is_up") and not iface.get("name", "").startswith("Loopback")]
    other_ifaces = [iface for iface in interfaces if iface not in up_ifaces and any(not ip.startswith("169.254.") for ip in iface.get("ipv4", []))]
    display_ifaces = up_ifaces + other_ifaces
    if not display_ifaces:
        display_ifaces = [iface for iface in interfaces if iface.get("is_up")][:3]

    if display_ifaces:
        lines.append(f"    {c_bold}Active Interfaces:{c_reset}")
        for iface in display_ifaces:
            status_badge = _badge("UP", Style.BRIGHT_GREEN, use_color) if iface.get("is_up") else _badge("DOWN", Style.DIM, use_color)
            speed_str = f"({iface.get('speed_mbps')} Mbps)" if iface.get("speed_mbps") else ""
            ipv4_str = ", ".join(iface.get("ipv4", [])) or "None"
            mac_str = iface.get("mac") or "N/A"

            lines.append(f"      • {c_bold}{iface.get('name')}{c_reset} {status_badge} {speed_str}")
            lines.append(f"          IPv4: {ipv4_str}  |  MAC: {mac_str}")
            if iface.get("bytes_sent") != "N/A" and iface.get("bytes_recv") != "N/A":
                lines.append(f"          Traffic: Sent {iface.get('bytes_sent')} / Recv {iface.get('bytes_recv')}")

    total_net_io = net_info.get("total_io")
    if total_net_io:
        lines.append(f"    {c_dim}Total Network Traffic: Sent {total_net_io.get('bytes_sent')} | Recv {total_net_io.get('bytes_recv')}{c_reset}")

    # Section 6: Battery & Power Status
    battery = data.get("battery", {})
    if battery.get("has_battery"):
        b_pct = battery.get("percent", 0.0)
        plugged = battery.get("power_plugged")
        plugged_str = "Plugged In (AC Power)" if plugged else "On Battery"
        time_left = battery.get("time_left", "N/A")
        b_bar = make_progress_bar(b_pct, width=16)
        colored_b_bar = _color_percent(100.0 - b_pct, b_bar, use_color)

        lines.append(f"\n{c_blue}{c_bold}  [6] POWER & BATTERY{c_reset}")
        lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")
        lines.append(f"    {c_bold}Charge Level:{c_reset}    {colored_b_bar}")
        lines.append(f"    {c_bold}Power Source:{c_reset}    {plugged_str}")
        lines.append(f"    {c_bold}Time Remaining:{c_reset}  {time_left}")

    # Section 7: Runtime Environment
    env = data.get("environment", {})
    lines.append(f"\n{c_blue}{c_bold}  [7] RUNTIME ENVIRONMENT{c_reset}")
    lines.append(f"{c_dim}  {subbar[2:]}{c_reset}")
    lines.append(f"    {c_bold}Python Version:{c_reset}   {env.get('python_version')} ({env.get('python_compiler')})")
    lines.append(f"    {c_bold}Python Path:{c_reset}      {env.get('python_executable')}")
    lines.append(f"    {c_bold}Project Path:{c_reset}     {env.get('working_directory')}")
    lines.append(f"    {c_bold}Active Processes:{c_reset} {env.get('active_processes')}")

    # Footer
    lines.append(f"\n{c_cyan}{bar}{c_reset}\n")

    return "\n".join(lines)
