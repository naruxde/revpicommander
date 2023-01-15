@echo off
set PACKAGE=revpicommander
set APP_NAME=RevPi Commander

if "%1" == "venv" goto venv
if "%1" == "installer" goto installer
if "%1" == "clean" goto clean

echo Make script for "%APP_NAME%" on Windows
echo.
echo Need action:
echo     venv        Create / update your virtual environment for build process
echo     installer   Build this application with PyInstaller
echo     clean       Clean up your environment after build process
goto end

:venv
python -m venv venv
venv\\Scripts\\pip.exe install --upgrade -r requirements.txt
goto end

:installer
venv\\Scripts\\pyinstaller -n "%APP_NAME%" ^
	--add-data="src\%PACKAGE%\locale;.\%PACKAGE%\locale" ^
	--add-data="data\%PACKAGE%.ico;." ^
	--icon=data\\%PACKAGE%.ico ^
	--noconfirm ^
	--clean ^
	--onedir ^
	--windowed ^
	src\\%PACKAGE%\\__main__.py
goto end

:clean
rmdir /S /Q build dist
rmdir /S /Q src\%PACKAGE%.egg-info
del *.spec

:end
