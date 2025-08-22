@echo off
pip install nuitka pyTelegramBotAPI tabulate PyAutoGUI numpy opencv-python Pillow psutil soundfile sounddevice
python -m nuitka --mingw64 --onefile --windows-disable-console --follow-imports --remove-output main.pyw