# System Information Dashboard (`sysinfo`)

A modern, fast, cross-platform system metrics and hardware inspection tool built with Python. 

When you run `start.py`, it inspects your system and renders an informative, visual console dashboard featuring resource usage bars, network states, and hardware statistics.

---

## 🚀 Quick Start

### 1. Visual Terminal Dashboard
Run the entrypoint script directly from your terminal:

```bash
python start.py
```

### 2. Live Web Dashboard (Localhost)
Launch the modern glassmorphism web UI in your default browser at `http://localhost:5000`:

```bash
python start.py --web
# or
python web_server.py
```

Features real-time polling (1s, 2s, 5s), per-core thread gauges, storage meters, network traffic, and battery metrics.

---

## 📊 Metrics Collected & Displayed

1. **Operating System & Hardware Overview**
   - OS Name, Version, and Kernel Build (e.g., Windows 11, Build 10.0.26200)
   - System Architecture (e.g., 64-bit AMD64)
   - Hostname and Currently Logged-in User
   - Boot Time and System Uptime (Days, Hours, Minutes, Seconds)

2. **Processor (CPU)**
   - Exact Processor Model (e.g., 13th Gen Intel(R) Core(TM) i7-13620H)
   - Physical Core Count and Logical Thread Count
   - Current and Maximum Clock Frequency (GHz / MHz)
   - Real-time overall CPU usage bar
   - Individual per-core load breakdown (C00, C01, ...)

3. **Memory & RAM**
   - Total, Used, and Available Physical Memory
   - Visual RAM utilization percentage bar
   - Committed / Virtual Memory & Pagefile metrics

4. **Storage & Disks**
   - Partition drive letters and mount points (e.g., `C:\`, `D:\`)
   - File system types (e.g., NTFS)
   - Total, Used, and Free space per drive with visual progress bars
   - Cumulative disk read/write throughput

5. **Network Connectivity**
   - Primary outbound Local IP address
   - Interface statuses (`[UP]` / `[DOWN]`)
   - IPv4, IPv6, and hardware MAC addresses
   - Link speeds (Mbps) and live network traffic counters (sent/received)

6. **Battery & Power (Laptops / Supported Hardware)**
   - Charge percentage
   - AC power status (Plugged In vs On Battery)
   - Remaining time estimation

7. **Runtime Environment**
   - Python version, compiler, and binary path
   - Active process count

---

## 🛠️ CLI Options & Usage Flags

You can customize how metrics are retrieved and displayed:

| Command | Description |
| :--- | :--- |
| `python start.py` | Default dashboard with ANSI color indicators and progress bars |
| `python start.py --json` | Output machine-readable JSON (great for automation or piping) |
| `python start.py --save report.json` | Save system info snapshot directly to a JSON file |
| `python start.py --save report.txt` | Save formatted text dashboard to a text file |
| `python start.py --no-color` | Disable ANSI color codes (plain text mode) |
| `python start.py --interval 0.5` | Customize CPU sampling duration (seconds) |

---

## 📁 Project Architecture

```
Explore_SVS/
├── sysinfo/
│   ├── __init__.py      # Package export and initialization
│   ├── collector.py     # Hardware and OS data collection with platform fallbacks
│   ├── formatter.py     # ANSI styling, progress bars, and table formatting
│   └── utils.py         # Byte/frequency converters and duration formatters
├── start.py             # Main executable entrypoint
├── requirements.txt     # Python package dependencies (psutil)
└── README.md            # Documentation
```

---

## 📦 Requirements & Installation

The project uses Python 3.8+ and `psutil`.

To install dependencies:
```bash
pip install -r requirements.txt
```
*(If `psutil` is not installed, the tool gracefully falls back to built-in standard library utilities (`platform`, `socket`, `shutil`, `ctypes`, `os`).)*
