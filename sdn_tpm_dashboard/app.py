import os
import time
from pathlib import Path

from flask import Flask, jsonify, render_template

from verifier import verify_device

app = Flask(__name__)

SCAN_PATHS = [Path("/media"), Path("/mnt")]


def scan_devices():
    """Scan mounted directories and verify each as a device."""
    print("[SCAN] Scanning devices...")
    devices = []

    for base in SCAN_PATHS:
        if not base.exists() or not base.is_dir():
            continue

        for entry in base.iterdir():
            if not entry.is_dir():
                continue

            start = time.perf_counter()
            print(f"[VERIFY] Checking device... {entry}")
            result = verify_device(entry)
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            device_info = {
                "id": entry.name,
                "path": str(entry),
                "status": result["status"],
                "reason": result["reason"],
                "time": elapsed_ms,
            }
            print(f"[RESULT] {device_info['status']} ({entry})")
            devices.append(device_info)

    return devices


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan")
def scan_route():
    return jsonify(scan_devices())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
