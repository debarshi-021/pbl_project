@echo off
echo --- SDN Controller Build Script ---
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Generating EXE...
pyinstaller --noconsole --onefile --add-data "shared;shared" main.py --name SDN_Controller
echo.
echo Done! Check the 'dist' folder for SDN_Controller.exe
pause
