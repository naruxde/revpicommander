@echo off
set PACKAGE=revpicommander

rem python -m venv venv
rem venv\\Scripts\\activate.bat
rem pip install -r requirements.txt

pyinstaller -n "RevPi Commander" ^
	--add-data="src\%PACKAGE%\locale;.\revpicommander\locale" ^
	--add-data="data\%PACKAGE%.ico;." ^
	--icon=data\\%PACKAGE%.ico ^
	--noconfirm ^
	--clean ^
	--onedir ^
	--windowed ^
	src\\%PACKAGE%\\__main__.py

rem deactivate