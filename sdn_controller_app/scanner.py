from __future__ import annotations

from pathlib import Path
from typing import Dict, List

USB_PATHS = ["/mnt/d", "/mnt/e", "/mnt/f"]


def scan_usb_devices() -> List[Dict[str, object]]:
    """Scan fixed USB mount paths and detect required files."""
    devices: List[Dict[str, object]] = []

    for path in USB_PATHS:
        mount_path = Path(path)
        exists = mount_path.is_dir()
        has_data = (mount_path / "data.txt").is_file() if exists else False
        has_sig = (mount_path / "sig.bin").is_file() if exists else False

        devices.append(
            {
                "path": path,
                "exists": exists,
                "valid_files": has_data and has_sig,
            }
        )

    return devices
