# ObsidianHub - System Monitor

Simpel tool to send the current PC statistic (CPU load, RAM, ...) to your ObsidianHub. This allows you to view your PC system stats on the display of your ObsidianHub.

## Quick Start

### 1. Create virtual environment
```bash
python3 -m venv venv
```

### 2. Activate it
#### Linux / macOS
```bash
# Linux / macOS
source venv/bin/activate
```

#### Windows
```bash
# Windows
venv\Scripts\activate
```

### 3. Install required packages
```bash
pip3 install psutil paho-mqtt
```

### 4. Run the system monitor
```bash
python3 system_monitor.py
```
