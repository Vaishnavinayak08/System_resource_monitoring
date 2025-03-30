from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "System Resource Monitoring API is running. Use /stats to get system stats."

@app.route('/stats')
def get_stats():
    return jsonify({
        "cpu_usage": 10.5,  # Dummy values
        "memory_usage": 55.3,
        "disk_usage": 30.2,
        "upload_speed": 10,
        "download_speed": 50
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0")
