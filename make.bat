@echo off
pyinstaller --clean -D --windowed ^
    --add-data="data\revpicommander.ico;." ^
    --icon=data\\revpicommander.ico ^
    revpipycontrol\revpicommander.py
