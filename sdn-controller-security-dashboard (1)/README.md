# SDN Controller Security Dashboard (Windows)

This project is a real-time USB authentication system designed for SDN Controller security. It uses cryptographic signatures to verify the identity of hardware devices (represented as USB drives).

## 🚀 How to Run (Desktop Version)

### 1. Prerequisites
- **Python 3.10+** installed on Windows.
- A USB drive for testing.

### 2. Setup
Open your terminal (CMD or PowerShell) in the project folder and run:
```bash
pip install -r requirements.txt
```

### 3. Generate Security Keys
Before running the app, you need to generate your RSA key pair:
```bash
python tools/generate_keys.py
```
This creates:
- `shared/private_key.pem`: Used to sign USB data (Keep this secret!).
- `shared/trusted_pub.pem`: Used by the app to verify signatures.

### 4. Create a Test USB
Plug in a USB drive and find its letter (e.g., `D:`). Then run:
```bash
python tools/create_test_usb.py
```
Follow the prompts to create either a **Trusted** or **Fake** device.

### 5. Launch the Dashboard
```bash
python main.py
```

---

## 📦 Building the .exe
To create a standalone Windows executable:
1. Run the `build_exe.bat` file.
2. Once finished, find your app in the `dist/SDN_Controller.exe` folder.

---

## 🛡️ Security Logic
1. **Detection**: The app polls Windows drive partitions every 1.5 seconds.
2. **Identification**: It looks for `data.txt` on the USB root.
3. **Verification**: It reads `sig.bin` and verifies it against `data.txt` using the RSA-2048 public key.
4. **Result**: 
   - ✅ **AUTHENTICATED**: Signature matches.
   - ❌ **REJECTED**: Signature mismatch or files missing.

---

## 📁 Project Structure
- `main.py`: Entry point for the application.
- `usb_detector.py`: Windows-native USB polling logic.
- `verifier.py`: RSA Cryptography implementation.
- `ui/dashboard.py`: Tkinter Classic GUI code.
- `tools/`: Scripts for key generation and USB testing.
- `shared/`: Storage for public/private keys.

## ⚠️ Troubleshooting
If you see an "ImportError" or "Failed to execute script", ensure you have:
1. Run `python tools/generate_keys.py` first.
2. Re-built the EXE after any code changes.
3. Included the `--add-data "shared;shared"` flag in PyInstaller.
