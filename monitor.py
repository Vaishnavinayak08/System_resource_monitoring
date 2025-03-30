import psutil
import time
import os

def clear_screen():
    """Clears the console screen for better visibility"""
    os.system("cls" if os.name == "nt" else "clear")

while True:
    clear_screen()
    
    # 🟢 CPU Usage (More Accurate)
    cpu_usage = psutil.cpu_percent(interval=1)  # Matches Task Manager update rate
    cpu_per_core = psutil.cpu_percent(percpu=True, interval=1)
    
    # 🟢 Memory Usage (Adjusted for Task Manager Calculation)
    memory = psutil.virtual_memory()
    memory_usage = (memory.used / memory.total) * 100  # Matches Task Manager

    # 🟢 Disk Activity (Read/Write in MB/s)
    disk_io = psutil.disk_io_counters()
    disk_read = disk_io.read_bytes / (1024 * 1024)  # Convert to MB
    disk_write = disk_io.write_bytes / (1024 * 1024)  # Convert to MB

    # 🟢 Network Speed (Real-time Upload/Download Speed in MB/s)
    prev_net = psutil.net_io_counters()
    time.sleep(1)  # Wait 1 second
    curr_net = psutil.net_io_counters()

    upload_speed = (curr_net.bytes_sent - prev_net.bytes_sent) / (1024 * 1024)  # MB/s
    download_speed = (curr_net.bytes_recv - prev_net.bytes_recv) / (1024 * 1024)  # MB/s

    # 📊 Display Results
    print(f"📌 CPU Usage: {cpu_usage:.2f}%")
    print(f"   Per Core Usage: {cpu_per_core}")  # List of per-core usages
    print(f"📌 Memory Usage: {memory_usage:.2f}%")
    print(f"📌 Disk Read: {disk_read:.2f} MB | Disk Write: {disk_write:.2f} MB")
    print(f"📌 Upload Speed: {upload_speed:.2f} MB/s | Download Speed: {download_speed:.2f} MB/s")
    
    time.sleep(5)  # Update every second
