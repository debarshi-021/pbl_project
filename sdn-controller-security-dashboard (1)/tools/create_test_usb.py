import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def create_test_usb(drive_letter, device_id, tamper=False):
    """
    Creates data.txt and sig.bin on the target drive.
    If tamper is True, the signature will be invalid.
    """
    drive_path = f"{drive_letter}:\\"
    if not os.path.exists(drive_path):
        print(f"[ERROR] Drive {drive_path} not found.")
        return

    # Load private key to sign
    try:
        with open("shared/private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    except FileNotFoundError:
        print("[ERROR] private_key.pem not found. Run generate_keys.py first.")
        return

    data_content = f"device_id={device_id}"
    
    # Sign the data
    signature = private_key.sign(
        data_content.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    if tamper:
        signature = b"INVALID_SIG" + signature[11:]

    # Write files to USB
    with open(os.path.join(drive_path, "data.txt"), "w") as f:
        f.write(data_content)
    
    with open(os.path.join(drive_path, "sig.bin"), "wb") as f:
        f.write(signature)

    print(f"[SUCCESS] Test files created on {drive_path}")
    if tamper:
        print("!!! This device is configured as a FAKE/TAMPERED device !!!")

if __name__ == "__main__":
    print("--- USB Test File Generator ---")
    letter = input("Enter USB Drive Letter (e.g., D): ").upper()
    dev_id = input("Enter Device ID (e.g., SW-CORE-001): ")
    is_fake = input("Make it a fake device? (y/n): ").lower() == 'y'
    
    create_test_usb(letter, dev_id, is_fake)
