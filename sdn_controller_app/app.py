from __future__ import annotations

import logging
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("sdn-controller")


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/scan")
def scan() -> Any:
    logger.info("[SCAN STARTED]")
    devices = scan_usb_devices()
    output: List[Dict[str, Any]] = []

    for device in devices:
        path = device["path"]
        if not device["exists"]:
            continue

        logger.info("[DEVICE FOUND] %s", path)

        if not device["valid_files"]:
            output.append(
                {
                    "device_id": "UNKNOWN",
                    "path": path,
                    "status": "REJECTED",
                    "reason": "missing data.txt or sig.bin",
                    "verification_time_ms": 0,
                }
            )
            logger.info("[RESULT] %s -> REJECTED (missing files)", path)
            continue

        logger.info("[VERIFYING] %s", path)
        started = time.perf_counter()
        result = verify_device(path)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)

        entry = {
            "device_id": result["device_id"],
            "path": path,
            "status": result["status"],
            "reason": result["reason"],
            "verification_time_ms": elapsed_ms,
        }
        output.append(entry)
        logger.info("[RESULT] %s -> %s (%s ms)", path, result["status"], elapsed_ms)

    return jsonify(output)


def _open_browser() -> None:
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.0, _open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
