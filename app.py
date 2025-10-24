from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

latest_script = ""
log_lines = []

def append_log(msg):
    entry = f"{msg}"
    log_lines.append(entry)
    if len(log_lines) > 50:
        log_lines.pop(0)
    print(entry)

@app.route("/", methods=['GET'])
def home():
    return "Roblox Script Server Running"

@app.route("/current_script", methods=['POST'])
def upload_script():
    global latest_script
    try:
        data = request.get_json()
        script = data.get("script", "")
        if not script:
            return jsonify({"status": "error", "message": "No script provided"})
        latest_script = script
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/current_script", methods=['GET'])
def get_script():
    return jsonify({"script": latest_script})

@app.route("/roblox_log", methods=['POST'])
def roblox_log():
    try:
        data = request.get_json()
        log_msg = data.get("log", "")
        if log_msg:
            append_log(f"ROBLOX: {log_msg}")
        return jsonify({"status": "success"})
    except Exception as e:
        append_log(f"Error receiving log: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route("/logs", methods=['GET'])
def get_logs():
    return jsonify({"logs": log_lines})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
