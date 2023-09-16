SHELL        := bash
MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
PACKAGE = revpicommander
APP_NAME = RevPi\ Commander
APP_IDENT = org.revpimodio.revpicommander
APPLE_SIG = "Developer ID Application: Sven Sager (U3N5843D9K)"

# Set path to create the virtual environment with package name
ifdef PYTHON3_VENV
VENV_PATH = $(PYTHON3_VENV)/$(PACKAGE)
else
VENV_PATH = venv
endif

# If virtualenv exists, use it. If not, use PATH to find commands
SYSTEM_PYTHON  = python3
PYTHON         = $(or $(wildcard $(VENV_PATH)/bin/python), $(SYSTEM_PYTHON))

APP_VERSION = $(shell $(PYTHON) src/$(PACKAGE) --version)

all: build_ui build_rc test build

.PHONY: all

## Environment
venv-info:
	echo Using path: "$(VENV_PATH)"
	exit 0

venv:
	$(SYSTEM_PYTHON) -m venv --system-site-packages "$(VENV_PATH)"
	source $(VENV_PATH)/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r requirements.txt
	exit 0

.PHONY: venv-info venv

## Compile Qt UI files to python code
build_ui:
	cd ui_dev && for ui_file in *.ui; do \
		file_name=$${ui_file%.ui}; \
		$(PYTHON) -m PyQt5.uic.pyuic $${ui_file} -o ../src/$(PACKAGE)/ui/$${file_name}_ui.py -x --from-imports; \
		echo $${file_name}; \
	done

build_rc:
	cd ui_dev && for rc_file in *.qrc; do \
		file_name=$${rc_file%.qrc}; \
		$(PYTHON) -m PyQt5.pyrcc_main $${rc_file} -o ../src/$(PACKAGE)/ui/$${file_name}_rc.py; \
		echo $${file_name}; \
	done

update_translation:
	$(PYTHON) -m PyQt5.pylupdate_main translate.pro

.PHONY: build_ui build_rc update_translation

## Build steps
build: build_ui build_rc
	$(PYTHON) -m setup sdist
	$(PYTHON) -m setup bdist_wheel

install: test build
	$(PYTHON) -m pip install dist/$(PACKAGE)-*.whl

uninstall:
	$(PYTHON) -m pip uninstall --yes $(PACKAGE)

.PHONY: test build install uninstall

## PyInstaller
installer_mac: build_ui build_rc
	$(PYTHON) -m PyInstaller -n $(APP_NAME) \
		--add-data="src/$(PACKAGE)/locale:./$(PACKAGE)/locale" \
		--add-data="data/$(PACKAGE).icns:." \
		--icon=data/$(PACKAGE).icns \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
		--osx-bundle-identifier $APP_IDENT \
		--codesign-identity $(APPLE_SIG) \
		src/$(PACKAGE)/__main__.py

installer_mac_dmg: installer_mac
	mkdir dist/dmg
	mv dist/$(APP_NAME).app dist/dmg
	create-dmg \
		--volname $(APP_NAME) \
		--background data/dmg_background.png \
		--window-pos 200 120 \
		--window-size 480 300 \
		--icon-size 64 \
		--icon $(APP_NAME).app 64 64 \
		--hide-extension $(APP_NAME).app \
		--app-drop-link 288 64 \
		--add-file LICENSE.txt LICENSE.txt 192 180 \
		--codesign $(APPLE_SIG) \
		--notarize AC_PASSWORD \
		dist/$(APP_NAME)\ $(APP_VERSION).dmg \
		dist/dmg

installer_linux: build_ui build_rc
	$(PYTHON) -m PyInstaller -n $(APP_NAME) \
		--add-data="src/$(PACKAGE)/locale:./$(PACKAGE)/locale" \
		--add-data="data/$(PACKAGE).ico:." \
		--add-data="data/$(PACKAGE).png:." \
		--icon=data/$(PACKAGE).ico \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
		src/$(PACKAGE)/__main__.py

.PHONY: installer_mac installer_mac_dmg installer_linux

## Clean
clean:
	rm -rf build dist src/*.egg-info *.spec

distclean: clean
	rm -rf $(VENV_PATH)

.PHONY: clean distclean
