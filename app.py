import time
from flask import Flask, jsonify, render_template
import psutil
from collections import deque

app = Flask(__name__)

# 🔥 Store last 10 values for stability
cpu_history = deque(maxlen=10)
memory_history = deque(maxlen=10)
disk_history = deque(maxlen=10)
upload_history = deque(maxlen=10)
download_history = deque(maxlen=10)

@app.route('/stats')
def get_stats():
    # Capture initial disk and network stats
    net1 = psutil.net_io_counters()
    disk1 = psutil.disk_io_counters()
    time.sleep(1)  # Wait 1 second
    net2 = psutil.net_io_counters()
    disk2 = psutil.disk_io_counters()

    # Calculate network speed (MB/s)
    upload_speed = (net2.bytes_sent - net1.bytes_sent) / (1024 * 1024)
    download_speed = (net2.bytes_recv - net1.bytes_recv) / (1024 * 1024)

    # ✅ Fix: Use read_time and write_time instead of busy_time
    disk_read_time = disk2.read_time - disk1.read_time
    disk_write_time = disk2.write_time - disk1.write_time
    disk_usage = min((disk_read_time + disk_write_time) / 10, 100)  # Convert ms to percentage

    # Capture CPU & Memory usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    stats = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "upload_speed": upload_speed,
        "download_speed": download_speed
    }
    return jsonify(stats)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
