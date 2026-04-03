from __future__ import annotations

import base64
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_PATH = BASE_DIR / "shared" / "trusted_pub.pem"


def _extract_device_id(data_text: str) -> str:
    for line in data_text.splitlines():
        if line.lower().startswith("device_id="):
            return line.split("=", 1)[1].strip()
    return "UNKNOWN"


def _normalize_signature_file(sig_file: Path) -> Path:
    """Return a filesystem path to raw signature bytes for OpenSSL.

    Supports:
    - native binary signature file
    - text format: BASE64:<base64-signature>
    """
    raw = sig_file.read_bytes()

    try:
        text = raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        return sig_file

    if not text.startswith("BASE64:"):
        return sig_file

    b64_data = text.split("BASE64:", 1)[1].strip()
    decoded = base64.b64decode(b64_data, validate=True)
    tmp = NamedTemporaryFile(delete=False, suffix=".sig")
    tmp.write(decoded)
    tmp.flush()
    tmp.close()
    return Path(tmp.name)


def verify_device(path: str) -> Dict[str, str]:
    device_path = Path(path)
    data_file = device_path / "data.txt"
    sig_file = device_path / "sig.bin"

    if not data_file.is_file() or not sig_file.is_file():
        return {
            "device_id": "UNKNOWN",
            "status": "REJECTED",
            "reason": "missing required files",
        }

    try:
        data_text = data_file.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {
            "device_id": "UNKNOWN",
            "status": "REJECTED",
            "reason": f"failed to read data.txt: {exc}",
        }

    device_id = _extract_device_id(data_text)

    try:
        signature_path = _normalize_signature_file(sig_file)
    except (OSError, ValueError, base64.binascii.Error) as exc:
        return {
            "device_id": device_id,
            "status": "REJECTED",
            "reason": f"invalid signature format: {exc}",
        }

    cmd = [
        "openssl",
        "dgst",
        "-sha256",
        "-verify",
        str(PUBLIC_KEY_PATH),
        "-signature",
        str(signature_path),
        str(data_file),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if signature_path != sig_file:
        signature_path.unlink(missing_ok=True)

    if result.returncode == 0:
        return {
            "device_id": device_id,
            "status": "AUTHENTICATED",
            "reason": "signature valid",
        }

    stderr = (result.stderr or "").strip()
    stdout = (result.stdout or "").strip()
    detail = stderr or stdout or "signature invalid"

    return {
        "device_id": device_id,
        "status": "REJECTED",
        "reason": detail,
    }
