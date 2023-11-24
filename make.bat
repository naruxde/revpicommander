@echo off
set PACKAGE=revpicommander
set APP_NAME=RevPi Commander

set PYTHON=venv\\Scripts\\python.exe

if "%1" == "venv" goto venv
if "%1" == "test" goto test
if "%1" == "build" goto build
if "%1" == "app" goto app
if "%1" == "clean" goto clean
if "%1" == "distclean" goto distclean

echo Make script for "%APP_NAME%" on Windows
echo.
echo Need action:
echo     venv        Create your virtual environment for build process
echo     test        Run defined tests of the project
echo     build       Build PIP packages as source distribution and Wheel
echo     app         Build this application with PyInstaller
echo     clean       Clean up build artifacts after build process
echo     distclean   Same as clean plus removing virtual environment
goto end

:venv
    python -m venv venv
    venv\\Scripts\\pip.exe install -r requirements.txt
    goto end

:test
    set PYTHONPATH=src
    %PYTHON% -m pytest
    goto end

:build
    %PYTHON% -m setup sdist
    %PYTHON% -m setup bdist_wheel
    goto end

:app
    mkdir dist
    %PYTHON% -m piplicenses ^
        --format=markdown ^
        --output-file dist/bundled-libraries.md
    %PYTHON% -m piplicenses ^
        --with-authors ^
        --with-urls ^
        --with-description ^
        --with-license-file ^
        --no-license-path ^
        --format=json ^
        --output-file dist/open-source-licenses.json
    %PYTHON% -m piplicenses ^
        --with-authors ^
        --with-urls ^
        --with-description ^
        --with-license-file ^
        --no-license-path ^
        --format=plain-vertical ^
        --output-file dist/open-source-licenses.txt
    %PYTHON% -m PyInstaller -n "%APP_NAME%" ^
        --add-data="dist/bundled-libraries.md;%PACKAGE%\open-source-licenses" ^
        --add-data="dist/open-source-licenses.*;%PACKAGE%\open-source-licenses" ^
        --add-data="src\%PACKAGE%\locale;.\%PACKAGE%\locale" ^
        --add-data="data\%PACKAGE%.ico;." ^
        --icon=data\\%PACKAGE%.ico ^
        --noconfirm ^
        --clean ^
        --onedir ^
        --windowed ^
        src\\%PACKAGE%\\__main__.py
    goto end

:distclean
    rmdir /S /Q venv

:clean
    rmdir /S /Q .pytest_cache
    rmdir /S /Q build dist src\%PACKAGE%.egg-info
    del /Q *.spec

:end
