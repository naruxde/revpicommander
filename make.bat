@echo off
pyinstaller --clean -D --windowed ^
    --add-data="data\revpipycontrol.ico;." ^
    --icon=data\\revpipycontrol.ico ^
    revpipycontrol\revpipycontrol.py
