import time
from flask import Flask, jsonify, render_template
import psutil
from collections import deque
import os

app = Flask(__name__)

# 🔥 Store last 10 values for stability
cpu_history = deque(maxlen=10)
memory_history = deque(maxlen=10)
disk_history = deque(maxlen=10)
upload_history = deque(maxlen=10)
download_history = deque(maxlen=10)

@app.route('/stats')
def get_stats():
    try:
        psutil.cpu_percent(interval=1)  # Warm-up to avoid zero values
        net1 = psutil.net_io_counters()
        time.sleep(1)  # Sleep to measure network speed
        net2 = psutil.net_io_counters()

        upload_speed = (net2.bytes_sent - net1.bytes_sent) / (1024 * 1024)
        download_speed = (net2.bytes_recv - net1.bytes_recv) / (1024 * 1024)

        stats = {
            "cpu_usage": psutil.cpu_percent(interval=1),  # Ensure a real value
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "upload_speed": round(upload_speed, 2),
            "download_speed": round(download_speed, 2)
        }
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Dynamically get PORT for deployment
    app.run(host="0.0.0.0", port=port, debug=True)
