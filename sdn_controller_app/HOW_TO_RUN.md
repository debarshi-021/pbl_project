# SDN Controller App: Setup and Packaging

## 1) Create trusted USB signature material (OpenSSL)

From `sdn_controller_app/`:

```bash
openssl genrsa -out shared/trusted_private.pem 2048
openssl rsa -in shared/trusted_private.pem -pubout -out shared/trusted_pub.pem
openssl dgst -sha256 -sign shared/trusted_private.pem -out sample_usb/trusted/sig.raw sample_usb/trusted/data.txt
python - <<'PY'
import base64
from pathlib import Path
raw = Path('sample_usb/trusted/sig.raw').read_bytes()
Path('sample_usb/trusted/sig.bin').write_text('BASE64:' + base64.b64encode(raw).decode() + '\n', encoding='utf-8')
Path('sample_usb/trusted/sig.raw').unlink(missing_ok=True)
PY
```

To simulate mounted USBs:

```bash
sudo mkdir -p /mnt/d /mnt/e
sudo cp sample_usb/trusted/data.txt /mnt/d/data.txt
sudo cp sample_usb/trusted/sig.bin /mnt/d/sig.bin
```

## 2) Create fake USB

```bash
printf "device_id=SW-FAKE-009\nrole=rogue-switch\n" > sample_usb/fake/data.txt
python - <<'PY'
import base64, os
from pathlib import Path
Path('sample_usb/fake/sig.bin').write_text('BASE64:' + base64.b64encode(os.urandom(256)).decode() + '\n', encoding='utf-8')
PY
sudo cp sample_usb/fake/data.txt /mnt/e/data.txt
sudo cp sample_usb/fake/sig.bin /mnt/e/sig.bin
```

## 3) Run project

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 4) Convert to EXE with PyInstaller

```bash
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" app.py
```
