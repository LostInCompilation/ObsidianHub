#!/usr/bin/env python3

"""
System Monitor for ObsidianHub
Sends CPU, RAM, Disk, and Network metrics to individual MQTT topics for ObsidianHub device.
"""

import psutil
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import time
import platform
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================
MQTT_BROKER = "192.168.0.103"  # Change to your broker IP
MQTT_USERNAME = "mqtt-user"
MQTT_PASSWORD = "mqtt-user"
MQTT_PORT = 1883

MQTT_TOPIC_PREFIX = "obsidianhub/system_monitor"
MQTT_CLIENT_ID = "obsidianhub_system_monitor_script"
UPDATE_INTERVAL = 1  # seconds between updates

# ============================================================================
# DATA CLASSES
# ============================================================================
@dataclass
class SystemMetrics:
    """Container for system metrics"""
    cpu_percent: float = 0.0
    ram_percent: float = 0.0
    ram_used_gb: float = 0.0
    ram_total_gb: float = 0.0
    disk_percent: float = 0.0
    disk_used_gb: float = 0.0
    disk_free_gb: float = 0.0
    disk_total_gb: float = 0.0
    disk_read_mbps: float = 0.0   # Rate per second
    disk_write_mbps: float = 0.0  # Rate per second
    net_recv_mbps: float = 0.0    # Network receive rate (MB/s)
    net_sent_mbps: float = 0.0    # Network send rate (MB/s)
    timestamp: str = ""

# ============================================================================
# SYSTEM STATISTICS COLLECTOR
# ============================================================================
class SystemStats:
    """Collects system statistics"""
    def __init__(self):
        # Prime CPU percent
        psutil.cpu_percent(interval=1)
        # For disk I/O rates
        self.last_disk_io = psutil.disk_io_counters()
        self.last_io_time = time.time()
        # For network I/O rates
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()

    def collect(self) -> Optional[SystemMetrics]:
        """Collect all system metrics"""
        try:
            metrics = SystemMetrics()

            # CPU
            metrics.cpu_percent = round(psutil.cpu_percent(interval=None), 1)

            # RAM
            mem = psutil.virtual_memory()
            metrics.ram_percent = round(mem.percent, 1)
            metrics.ram_total_gb = round(mem.total / (1024 ** 3), 2)
            metrics.ram_used_gb = round((mem.total - mem.available) / (1024 ** 3), 2)

            # Disk usage for root
            disk = psutil.disk_usage('/')
            metrics.disk_percent = round(disk.percent, 1)
            metrics.disk_used_gb = round(disk.used / (1024 ** 3), 2)
            metrics.disk_free_gb = round(disk.free / (1024 ** 3), 2)
            metrics.disk_total_gb = round(disk.total / (1024 ** 3), 2)

            current_time = time.time()

            # Disk I/O rates (MB/s)
            current_disk_io = psutil.disk_io_counters()
            if self.last_disk_io and current_disk_io:
                time_diff = current_time - self.last_io_time
                if time_diff > 0:
                    read_bytes = current_disk_io.read_bytes - self.last_disk_io.read_bytes
                    write_bytes = current_disk_io.write_bytes - self.last_disk_io.write_bytes
                    metrics.disk_read_mbps = round(read_bytes / (1024 ** 2) / time_diff, 2)
                    metrics.disk_write_mbps = round(write_bytes / (1024 ** 2) / time_diff, 2)

            # Update last disk values
            self.last_disk_io = current_disk_io
            self.last_io_time = current_time

            # Network I/O rates (MB/s) - system-wide
            current_net_io = psutil.net_io_counters()
            if self.last_net_io and current_net_io:
                net_time_diff = current_time - self.last_net_time
                if net_time_diff > 0:
                    recv_bytes = current_net_io.bytes_recv - self.last_net_io.bytes_recv
                    sent_bytes = current_net_io.bytes_sent - self.last_net_io.bytes_sent
                    metrics.net_recv_mbps = round(recv_bytes / (1024 ** 2) / net_time_diff, 2)
                    metrics.net_sent_mbps = round(sent_bytes / (1024 ** 2) / net_time_diff, 2)

            # Update last network values
            self.last_net_io = current_net_io
            self.last_net_time = current_time

            metrics.timestamp = datetime.now().isoformat()
            return metrics
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR collecting metrics: {e}")
            return None

# ============================================================================
# MQTT CLIENT HANDLER (Upgraded to new callback API)
# ============================================================================
class MQTTHandler:
    """Handles MQTT connection and publishing"""
    def __init__(self, broker: str, port: int, client_id: str,
                 topic_prefix: str, username: str = "", password: str = ""):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.topic_prefix = topic_prefix
        self.username = username
        self.password = password
        self.client: Optional[mqtt.Client] = None
        self.connected = False

    def _on_connect(self, client, userdata, flags, reasoncode, properties):
        self.connected = (reasoncode == 0)
        timestamp = datetime.now().strftime("%H:%M:%S")
        if reasoncode == 0:
            print(f"[{timestamp}] Connected to MQTT broker")
        else:
            errors = {
                1: "Incorrect protocol version",
                2: "Invalid client ID",
                3: "Server unavailable",
                4: "Bad username/password",
                5: "Not authorized"
            }
            print(f"[{timestamp}] Connection failed: {errors.get(reasoncode.value, f'Unknown error ({reasoncode.value})')}")

    def _on_disconnect(self, client, userdata, flags, reasoncode, properties):
        self.connected = False
        timestamp = datetime.now().strftime("%H:%M:%S")
        if reasoncode != 0:
            print(f"[{timestamp}] Unexpected disconnection from MQTT broker (reasoncode: {reasoncode.value})")
        else:
            print(f"[{timestamp}] Gracefully disconnected from MQTT broker")

    def connect(self) -> bool:
        try:
            if self.client is None:
                self.client = mqtt.Client(
                    callback_api_version=CallbackAPIVersion.VERSION2,
                    client_id=self.client_id
                )
                self.client.on_connect = self._on_connect
                self.client.on_disconnect = self._on_disconnect
                if self.username and self.password:
                    self.client.username_pw_set(self.username, self.password)
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_start()
            return True
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Connection error: {e}")
            return False

    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.client = None

    def publish_metrics(self, metrics: SystemMetrics) -> bool:
        if not self.connected or not metrics:
            return False
        try:
            topics = {
                f"{self.topic_prefix}/cpu": metrics.cpu_percent,
                f"{self.topic_prefix}/ram/percent": metrics.ram_percent,
                #f"{self.topic_prefix}/ram/used": metrics.ram_used_gb,
                #f"{self.topic_prefix}/ram/total": metrics.ram_total_gb,
                #f"{self.topic_prefix}/disk/percent": metrics.disk_percent,
                #f"{self.topic_prefix}/disk/used": metrics.disk_used_gb,
                #f"{self.topic_prefix}/disk/free": metrics.disk_free_gb,
                #f"{self.topic_prefix}/disk/total": metrics.disk_total_gb,
                f"{self.topic_prefix}/disk/read": metrics.disk_read_mbps,
                f"{self.topic_prefix}/disk/write": metrics.disk_write_mbps,
                f"{self.topic_prefix}/net/recv": metrics.net_recv_mbps,
                f"{self.topic_prefix}/net/sent": metrics.net_sent_mbps,
            }
            for topic, value in topics.items():
                self.client.publish(topic, str(value), qos=0, retain=False)
            return True
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Publish error: {e}")
            return False

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] System Monitor starting...")
    print(f"Platform: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT} | Topic prefix: {MQTT_TOPIC_PREFIX}")

    stats = SystemStats()
    mqtt_handler = MQTTHandler(
        broker=MQTT_BROKER,
        port=MQTT_PORT,
        client_id=MQTT_CLIENT_ID,
        topic_prefix=MQTT_TOPIC_PREFIX,
        username=MQTT_USERNAME,
        password=MQTT_PASSWORD
    )

    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Connecting to MQTT broker...")
    mqtt_handler.connect()
    time.sleep(2)

    try:
        while True:
            if not mqtt_handler.connected:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Reconnecting to MQTT broker...")
                mqtt_handler.disconnect()
                time.sleep(2)
                mqtt_handler.connect()
                time.sleep(3)
                continue

            metrics = stats.collect()
            if metrics:
                success = mqtt_handler.publish_metrics(metrics)
                #if success:
                #    timestamp = datetime.now().strftime("%H:%M:%S")
                #    print(f"[{timestamp}] Metrics published | "
                #          f"CPU: {metrics.cpu_percent}% | "
                #          f"RAM: {metrics.ram_percent}% ({metrics.ram_used_gb}/{metrics.ram_total_gb} GB) | "
                #          f"Disk: {metrics.disk_percent}% | "
                #          f"Disk I/O: R {metrics.disk_read_mbps} MB/s W {metrics.disk_write_mbps} MB/s | "
                #          f"Net: ↓ {metrics.net_recv_mbps} MB/s ↑ {metrics.net_sent_mbps} MB/s")

            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] Shutting down...")
    finally:
        mqtt_handler.disconnect()
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Disconnected. Goodbye!")

if __name__ == "__main__":
    main()
