import subprocess
from pathlib import Path

TRUSTED_PUBKEY = Path(__file__).resolve().parent / "shared" / "trusted_pub.pem"


def verify_device(device_path: Path):
    """Verify a mounted device directory using OpenSSL signature check."""
    data_file = device_path / "data.txt"
    sig_file = device_path / "sig.bin"

    if not data_file.exists() or not sig_file.exists():
        return {"status": "REJECTED", "reason": "No signature"}

    if not TRUSTED_PUBKEY.exists():
        return {"status": "REJECTED", "reason": "Trusted public key missing"}

    cmd = [
        "openssl",
        "dgst",
        "-sha256",
        "-verify",
        str(TRUSTED_PUBKEY),
        "-signature",
        str(sig_file),
        str(data_file),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = (result.stdout + result.stderr).strip()

        if "Verified OK" in output:
            return {"status": "AUTHENTICATED", "reason": "Signature valid"}

        return {"status": "REJECTED", "reason": "Signature verification failed"}
    except Exception as exc:
        return {"status": "REJECTED", "reason": f"Verification error: {exc}"}
