import os
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

class Verifier:
    """Handles RSA signature verification for USB devices."""
    
    def __init__(self, public_key_path):
        self.public_key_path = public_key_path
        self.public_key = self._load_public_key()

    def _load_public_key(self):
        if not os.path.exists(self.public_key_path):
            return None
        with open(self.public_key_path, "rb") as key_file:
            return serialization.load_pem_public_key(key_file.read())

    def verify_device(self, drive_path):
        """
        Verifies data.txt against sig.bin on the given drive.
        Returns (is_valid, device_id, reason, verify_time_ms)
        """
        start_time = time.time()
        data_path = os.path.join(drive_path, "data.txt")
        sig_path = os.path.join(drive_path, "sig.bin")

        if not os.path.exists(data_path) or not os.path.exists(sig_path):
            duration = int((time.time() - start_time) * 1000)
            return False, "Unknown", "Missing authentication files", duration

        try:
            # Read data
            with open(data_path, "r") as f:
                content = f.read().strip()
                # Expecting device_id=SW-CORE-001
                if "device_id=" in content:
                    device_id = content.split("device_id=")[1]
                else:
                    device_id = "Malformed Data"

            # Read signature
            with open(sig_path, "rb") as f:
                signature = f.read()

            # Verify
            if self.public_key:
                self.public_key.verify(
                    signature,
                    content.encode(),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
                duration = int((time.time() - start_time) * 1000)
                return True, device_id, "Signature Valid", duration
            else:
                duration = int((time.time() - start_time) * 1000)
                return False, device_id, "Trusted Public Key Missing", duration

        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            return False, "Unknown", f"Verification Failed: {str(e)}", duration
