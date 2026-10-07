# Local Amazfit GTR Telemetry & Dashboard (Linux)

A lightweight, local, cloud-free CLI tool and automated background service for Linux to track, store, and visualize fitness telemetry (Battery, Steps, Distance, Calories) from an Amazfit GTR via Bluetooth Low Energy (BLE).

---

## Features
- **Pure Python BLE:** Connects directly using `bleak` without requiring heavy apps like Gadgetbridge or cloud logins (Zepp API).
- **Daily Upsert JSON Database:** Automatically maintains one definitive daily snapshot per calendar day, avoiding redundant logs.
- **Interactive Web Dashboard:** Compiles data into a sleek dark-mode HTML page powered by **Chart.js** for visual trend tracking.
- **Background Automation:** Uses a native **systemd user timer** to poll the watch hourly without taxing system resources or watch battery.

---

## Project Structure
- `amazfit_status.py` - Fetches BLE telemetry characteristics and updates `history.json`.
- `amazfit_info.py` - Reads device hardware and firmware information.
- `amazfit_dashboard.py` - Compiles `history.json` into `dashboard.html` with charts.
- `amazfit` - Master Bash wrapper script managing options (`-status`, `-web`, `-info`).
- `history.json` - Local lightweight JSON database storing daily snapshots.

---

## Installation & Setup

### 1. Requirements & Dependencies
Make sure you have Python 3, `bleak`, and system tools installed:
```bash
sudo apt update && sudo apt install python3-pip python3-venv bluez
