SHELL        := bash
MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
PACKAGE = revpicommander

# If virtualenv exists, use it. If not, use PATH to find
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYTHON         = $(or $(wildcard venv/bin/python), $(SYSTEM_PYTHON))
SYSTEM_PYUIC5  = $(shell which pyuic5)
PYUIC5         = $(or $(wildcard venv/bin/pyuic5), $(SYSTEM_PYUIC5))
SYSTEM_PYRCC5  = $(shell which pyrcc5)
PYRCC5         = $(or $(wildcard venv/bin/pyrcc5), $(SYSTEM_PYRCC5))
SYSTEM_PYLUP5  = $(shell which pylupdate5)
PYLUP5         = $(or $(wildcard venv/bin/pylupdate5), $(SYSTEM_PYLUP5))

all: build_ui build_rc build

.PHONY: all

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

## Environment
venv:
	rm -rf venv
	$(SYSTEM_PYTHON) -m venv venv

deps:
	$(PYTHON) -m pip install --upgrade pip -r requirements.txt

.PHONY: venv deps

## Build, install
build: build_ui build_rc
	$(PYTHON) -m setup sdist
	$(PYTHON) -m setup bdist_wheel

install:
	$(PYTHON) -m pip install dist/$(PACKAGE)-*.whl

.PHONY: build install

## PyInstaller
installer_mac: build
	$(PYTHON) -m PyInstaller -n "RevPi Commander" \
		--add-data="src/$(PACKAGE)/locale:./revpicommander/locale" \
		--add-data="data/$(PACKAGE).icns:." \
		--icon=data/$(PACKAGE).icns \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
		src/$(PACKAGE)/__main__.py

installer_win: all
	make_installer_win.bat

.PHONY: installer_mac installer_win

## Clean
clean:
	rm -rf build dist src/*.egg-info *.spec

.PHONY: clean
