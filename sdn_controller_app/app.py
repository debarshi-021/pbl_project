from __future__ import annotations

import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template

from scanner import scan_usb_devices
from verifier import verify_device

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/scan")
def scan() -> Any:
    print("[SCAN LOOP RUNNING]")
    devices = scan_usb_devices()
    results: List[Dict[str, Any]] = []

    for device in devices:
        path = str(device["path"])
        print("[DEVICE DETECTED]", path)

        started = time.perf_counter()
        if bool(device.get("data_exists")) and bool(device.get("sig_exists")):
            result = verify_device(path)
        else:
            result = {
                "device_id": "UNKNOWN",
                "status": "REJECTED",
                "reason": "Missing files",
            }

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        response_item = {
            "path": path,
            "verification_time_ms": elapsed_ms,
            **result,
        }
        results.append(response_item)
        print("[RESULT]", response_item)

    return jsonify(results)


def _open_browser() -> None:
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.0, _open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
