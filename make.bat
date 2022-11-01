@echo off
pyinstaller --noconfirm --clean -D --windowed ^
    --add-data="data\\revpicommander.ico;." ^
    --add-data="revpicommander\\locale;.\\locale" ^
    --icon=data\\revpicommander.ico ^
    --path=include ^
    revpicommander\revpicommander.py
