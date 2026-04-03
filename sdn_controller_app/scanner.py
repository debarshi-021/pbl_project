from __future__ import annotations

from pathlib import Path
from typing import Dict, List

USB_PATHS = ["/mnt/d", "/mnt/e", "/mnt/f"]


def scan_usb_devices() -> List[Dict[str, object]]:
    """Safely scan fixed USB mount paths.

    Missing/disconnected mounts are ignored so hot-plug and unplug never crash scanning.
    """
    devices: List[Dict[str, object]] = []

    for path_str in USB_PATHS:
        try:
            mount_path = Path(path_str)

            # Safe existence check; skipped mounts are silently ignored.
            if not mount_path.exists():
                continue

            data_file = mount_path / "data.txt"
            sig_file = mount_path / "sig.bin"

            devices.append(
                {
                    "path": path_str,
                    "data_exists": data_file.exists(),
                    "sig_exists": sig_file.exists(),
                }
            )
        except Exception as exc:  # defensive by design for unstable mount states
            print(f"[WARNING] Skipping {path_str}: {exc}")
            continue

    return devices
