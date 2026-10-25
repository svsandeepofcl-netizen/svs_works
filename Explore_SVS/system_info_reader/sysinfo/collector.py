"""
System Information Collector
Gathers comprehensive hardware, OS, memory, storage, network, and runtime metrics.
"""

import datetime
import getpass
import os
import platform
import socket
import sys
import time
from typing import Any, Dict, List, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from .utils import format_bytes, format_duration, format_frequency


def _get_cpu_brand_name() -> str:
    """Retrieve a clean, human-readable CPU brand string across platforms."""
    system = platform.system()
    if system == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            )
            processor_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            winreg.CloseKey(key)
            return processor_name.strip()
        except Exception:
            pass
    elif system == "Darwin":
        try:
            import subprocess
            res = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
    elif system == "Linux":
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass

    return platform.processor() or "Unknown Processor"


def _get_primary_ip() -> str:
    """Retrieve the primary local IP address routed outward."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable or send actual packets
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def get_os_info() -> Dict[str, Any]:
    """Retrieve operating system and machine information."""
    boot_time_ts = psutil.boot_time() if HAS_PSUTIL else None
    if boot_time_ts:
        boot_dt = datetime.datetime.fromtimestamp(boot_time_ts)
        boot_time_str = boot_dt.strftime("%Y-%m-%d %H:%M:%S")
        uptime_seconds = time.time() - boot_time_ts
        uptime_str = format_duration(uptime_seconds)
    else:
        boot_time_str = "N/A"
        uptime_seconds = None
        uptime_str = "N/A"

    try:
        username = getpass.getuser()
    except Exception:
        username = os.environ.get("USERNAME") or os.environ.get("USER") or "Unknown"

    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": f"{platform.architecture()[0]} ({platform.machine()})",
        "hostname": socket.gethostname(),
        "username": username,
        "boot_time": boot_time_str,
        "uptime": uptime_str,
        "uptime_seconds": uptime_seconds,
    }


def get_cpu_info(sample_interval: float = 0.3) -> Dict[str, Any]:
    """Retrieve CPU model, core counts, frequency, and current usage."""
    brand = _get_cpu_brand_name()
    physical_cores = psutil.cpu_count(logical=False) if HAS_PSUTIL else os.cpu_count()
    logical_cores = psutil.cpu_count(logical=True) if HAS_PSUTIL else os.cpu_count()

    freq_current = None
    freq_min = None
    freq_max = None
    if HAS_PSUTIL:
        try:
            freq = psutil.cpu_freq()
            if freq:
                freq_current = freq.current
                freq_min = freq.min
                freq_max = freq.max
        except Exception:
            pass

    usage_percent = 0.0
    per_core_usage = []
    if HAS_PSUTIL:
        try:
            usage_percent = psutil.cpu_percent(interval=sample_interval)
            per_core_usage = psutil.cpu_percent(interval=None, percpu=True)
        except Exception:
            pass

    return {
        "brand": brand,
        "physical_cores": physical_cores,
        "logical_cores": logical_cores,
        "frequency_current_mhz": freq_current,
        "frequency_current": format_frequency(freq_current),
        "frequency_max": format_frequency(freq_max) if freq_max else "N/A",
        "usage_percent": usage_percent,
        "per_core_percent": per_core_usage,
    }


def _get_windows_pagefile() -> Optional[Dict[str, Any]]:
    """Retrieve Windows pagefile / commit metrics directly via Win32 API without PDH counters."""
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            # On Windows, ullTotalPageFile represents the commit limit,
            # and (ullTotalPageFile - ullAvailPageFile) represents committed virtual memory.
            commit_limit = stat.ullTotalPageFile
            committed = max(0, commit_limit - stat.ullAvailPageFile)
            avail = stat.ullAvailPageFile
            percent = round((committed / commit_limit) * 100, 1) if commit_limit > 0 else 0.0
            return {
                "label": "Committed / Virtual",
                "total_bytes": commit_limit,
                "total": format_bytes(commit_limit),
                "used_bytes": committed,
                "used": format_bytes(committed),
                "free_bytes": avail,
                "free": format_bytes(avail),
                "percent": percent,
            }
    except Exception:
        pass
    return None


def get_memory_info() -> Dict[str, Any]:
    """Retrieve RAM and swap/page file usage."""
    ram_data = {
        "total_bytes": 0,
        "total": "N/A",
        "used_bytes": 0,
        "used": "N/A",
        "available_bytes": 0,
        "available": "N/A",
        "percent": 0.0,
    }
    swap_data = None

    if HAS_PSUTIL:
        try:
            vmem = psutil.virtual_memory()
            ram_data = {
                "total_bytes": vmem.total,
                "total": format_bytes(vmem.total),
                "used_bytes": vmem.used,
                "used": format_bytes(vmem.used),
                "available_bytes": vmem.available,
                "available": format_bytes(vmem.available),
                "percent": vmem.percent,
            }
        except Exception:
            pass

        try:
            swap = psutil.swap_memory()
            swap_data = {
                "total_bytes": swap.total,
                "total": format_bytes(swap.total),
                "used_bytes": swap.used,
                "used": format_bytes(swap.used),
                "free_bytes": swap.free,
                "free": format_bytes(swap.free),
                "percent": swap.percent,
            }
        except Exception:
            if platform.system() == "Windows":
                swap_data = _get_windows_pagefile()
    elif platform.system() == "Windows":
        swap_data = _get_windows_pagefile()

    return {
        "ram": ram_data,
        "swap": swap_data,
    }


def get_disk_info() -> Dict[str, Any]:
    """Retrieve mounted partitions and storage usage."""
    partitions_data = []

    if HAS_PSUTIL:
        try:
            partitions = psutil.disk_partitions(all=False)
        except Exception:
            partitions = []

        for p in partitions:
            # Skip virtual / inaccessible pseudo mounts
            if "cdrom" in p.opts or p.fstype == "":
                continue
            try:
                usage = psutil.disk_usage(p.mountpoint)
                partitions_data.append({
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype,
                    "total_bytes": usage.total,
                    "total": format_bytes(usage.total),
                    "used_bytes": usage.used,
                    "used": format_bytes(usage.used),
                    "free_bytes": usage.free,
                    "free": format_bytes(usage.free),
                    "percent": usage.percent,
                })
            except (PermissionError, OSError):
                continue
    else:
        # Standard library fallback using shutil
        import shutil
        root = "C:\\" if platform.system() == "Windows" else "/"
        try:
            usage = shutil.disk_usage(root)
            percent = round((usage.used / usage.total) * 100, 1) if usage.total else 0
            partitions_data.append({
                "device": root,
                "mountpoint": root,
                "fstype": "N/A",
                "total_bytes": usage.total,
                "total": format_bytes(usage.total),
                "used_bytes": usage.used,
                "used": format_bytes(usage.used),
                "free_bytes": usage.free,
                "free": format_bytes(usage.free),
                "percent": percent,
            })
        except Exception:
            pass

    # Disk I/O totals
    io_data = None
    if HAS_PSUTIL:
        try:
            io = psutil.disk_io_counters()
            if io:
                io_data = {
                    "read_bytes": io.read_bytes,
                    "read": format_bytes(io.read_bytes),
                    "write_bytes": io.write_bytes,
                    "write": format_bytes(io.write_bytes),
                }
        except Exception:
            pass

    return {
        "partitions": partitions_data,
        "io": io_data,
    }


def get_network_info() -> Dict[str, Any]:
    """Retrieve network interfaces, IP addresses, and throughput statistics."""
    primary_ip = _get_primary_ip()
    interfaces = []

    if HAS_PSUTIL:
        try:
            net_addrs = psutil.net_if_addrs()
            net_stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters(pernic=True)
        except Exception:
            net_addrs, net_stats, io_counters = {}, {}, {}

        for iface_name, addrs in net_addrs.items():
            stats = net_stats.get(iface_name)
            is_up = stats.isup if stats else False
            speed_mbps = stats.speed if stats and stats.speed > 0 else None

            ipv4_list = []
            ipv6_list = []
            mac = None

            for addr in addrs:
                fam = addr.family.name if hasattr(addr.family, "name") else str(addr.family)
                if fam in ("AF_INET", "2"):
                    ipv4_list.append(addr.address)
                elif fam in ("AF_INET6", "23", "10"):
                    # Exclude scope IDs for cleaner output
                    clean_v6 = addr.address.split("%")[0]
                    ipv6_list.append(clean_v6)
                elif fam in ("AF_LINK", "17"):
                    mac = addr.address

            iface_io = io_counters.get(iface_name)

            interfaces.append({
                "name": iface_name,
                "is_up": is_up,
                "speed_mbps": speed_mbps,
                "mac": mac or "N/A",
                "ipv4": ipv4_list,
                "ipv6": ipv6_list,
                "bytes_sent": format_bytes(iface_io.bytes_sent) if iface_io else "N/A",
                "bytes_recv": format_bytes(iface_io.bytes_recv) if iface_io else "N/A",
            })
    else:
        interfaces.append({
            "name": "Default",
            "is_up": True,
            "speed_mbps": None,
            "mac": "N/A",
            "ipv4": [primary_ip],
            "ipv6": [],
            "bytes_sent": "N/A",
            "bytes_recv": "N/A",
        })

    # Overall network I/O
    total_io = None
    if HAS_PSUTIL:
        try:
            total_net_io = psutil.net_io_counters()
            if total_net_io:
                total_io = {
                    "bytes_sent": format_bytes(total_net_io.bytes_sent),
                    "bytes_recv": format_bytes(total_net_io.bytes_recv),
                    "packets_sent": total_net_io.packets_sent,
                    "packets_recv": total_net_io.packets_recv,
                }
        except Exception:
            pass

    return {
        "hostname": socket.gethostname(),
        "primary_ip": primary_ip,
        "interfaces": interfaces,
        "total_io": total_io,
    }


def get_battery_info() -> Dict[str, Any]:
    """Retrieve battery status if supported on the system."""
    if not HAS_PSUTIL:
        return {"has_battery": False}

    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return {"has_battery": False}

        secs_left = battery.secsleft
        if secs_left == psutil.POWER_TIME_UNLIMITED:
            time_left_str = "Unlimited (Charging / Plugged in)"
        elif secs_left == psutil.POWER_TIME_UNKNOWN or secs_left < 0:
            time_left_str = "Calculating..."
        else:
            time_left_str = format_duration(secs_left)

        return {
            "has_battery": True,
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
            "time_left": time_left_str,
        }
    except Exception:
        return {"has_battery": False}


def get_environment_info() -> Dict[str, Any]:
    """Retrieve runtime and Python environment information."""
    process_count = len(psutil.pids()) if HAS_PSUTIL else "N/A"
    return {
        "python_version": platform.python_version(),
        "python_compiler": platform.python_compiler(),
        "python_executable": sys.executable,
        "working_directory": os.getcwd(),
        "active_processes": process_count,
    }


def collect_all_system_info() -> Dict[str, Any]:
    """
    Collect comprehensive system information into a structured dictionary.
    """
    return {
        "os": get_os_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
        "battery": get_battery_info(),
        "environment": get_environment_info(),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
