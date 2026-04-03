import time
from pathlib import Path

from flask import Flask, jsonify, render_template

from verifier import verify_device

app = Flask(__name__)

SCAN_ROOTS = [Path("/media"), Path("/mnt"), Path("/run/media")]


def _decode_mount_path(raw_path: str) -> Path:
    """Decode escaped mount paths from /proc/mounts."""
    return Path(raw_path.replace("\\040", " "))


def discover_mounted_devices() -> list[Path]:
    """Discover mounted removable device paths with Linux-friendly fallbacks."""
    candidates: set[Path] = set()

    proc_mounts = Path("/proc/mounts")
    if proc_mounts.exists():
        try:
            with proc_mounts.open("r", encoding="utf-8") as mounts_file:
                for line in mounts_file:
                    parts = line.split()
                    if len(parts) < 2:
                        continue

                    mount_point = _decode_mount_path(parts[1])
                    if any(str(mount_point).startswith(str(root)) for root in SCAN_ROOTS):
                        if mount_point.exists() and mount_point.is_dir():
                            candidates.add(mount_point)
        except OSError:
            pass

    # Fallback scanning for environments where /proc/mounts is unavailable
    # or where mount metadata isn't exposed as expected.
    if not candidates:
        for root in SCAN_ROOTS:
            if not root.exists() or not root.is_dir():
                continue

            for child in root.iterdir():
                if child.is_dir():
                    candidates.add(child)
                    for grandchild in child.iterdir():
                        if grandchild.is_dir():
                            candidates.add(grandchild)

    return sorted(candidates)


def scan_devices():
    """Scan mounted directories and verify each as a device."""
    print("[SCAN] Scanning devices...")
    devices = []

    for entry in discover_mounted_devices():
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
