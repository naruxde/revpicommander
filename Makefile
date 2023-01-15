SHELL        := bash
MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
PACKAGE = revpicommander
APP_NAME = RevPi\ Commander
APP_IDENT = org.revpimodio.revpicommander
APPLE_SIG = "Developer ID Application: Sven Sager (U3N5843D9K)"

# If virtualenv exists, use it. If not, use PATH to find, except python3
SYSTEM_PYTHON  = /usr/bin/python3
PYTHON         = $(or $(wildcard venv/bin/python), $(SYSTEM_PYTHON))
SYSTEM_PYUIC5  = $(shell which pyuic5)
PYUIC5         = $(or $(wildcard venv/bin/pyuic5), $(SYSTEM_PYUIC5))
SYSTEM_PYRCC5  = $(shell which pyrcc5)
PYRCC5         = $(or $(wildcard venv/bin/pyrcc5), $(SYSTEM_PYRCC5))
SYSTEM_PYLUP5  = $(shell which pylupdate5)
PYLUP5         = $(or $(wildcard venv/bin/pylupdate5), $(SYSTEM_PYLUP5))

APP_VERSION = $(shell $(PYTHON) src/$(PACKAGE) --version)

all: build_ui build_rc build

.PHONY: all

## Environment
venv:
	$(SYSTEM_PYTHON) -m venv venv
	source venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r requirements.txt
	exit 0

.PHONY: venv

## Compile Qt UI files to python code
build_ui:
	cd ui_dev && for ui_file in *.ui; do \
		file_name=$${ui_file%.ui}; \
		$(PYUIC5) $${ui_file} -o ../src/$(PACKAGE)/ui/$${file_name}_ui.py -x --from-imports; \
		echo $${file_name}; \
	done

build_rc:
	cd ui_dev && for rc_file in *.qrc; do \
		file_name=$${rc_file%.qrc}; \
		$(PYRCC5) $${rc_file} -o ../src/$(PACKAGE)/ui/$${file_name}_rc.py; \
		echo $${file_name}; \
	done

update_translation:
	$(PYLUP5) translate.pro

.PHONY: build_ui build_rc update_translation

## Build, install
build: build_ui build_rc
	$(PYTHON) -m setup sdist
	$(PYTHON) -m setup bdist_wheel

install:
	$(PYTHON) -m pip install dist/$(PACKAGE)-*.whl

.PHONY: build install

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

.PHONY: installer_mac installer_mac_dmg

## Clean
clean:
	rm -rf build dist src/*.egg-info *.spec

clean-all: clean
	rm -R venv

.PHONY: clean clean-all
