SHELL        := bash
MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
PACKAGE       = revpicommander
APP_NAME      = RevPi\ Commander
APP_IDENT     = org.revpimodio.revpicommander
APPLE_SIG = "Developer ID Application: Sven Sager (U3N5843D9K)"

# Python interpreter to use for venv creation
SYSTEM_PYTHON = python3

# Set path to create the virtual environment with package name
ifdef PYTHON3_VENV
VENV_PATH = $(PYTHON3_VENV)/$(PACKAGE)
else
VENV_PATH = venv
endif

# Set targets for "all"-target
all: build-ui build-rc build
.PHONY: all

## Virtual environment creation with SYSTEM_PYTHON
venv:
	# Start with empty environment
	"$(SYSTEM_PYTHON)" -m venv "$(VENV_PATH)"
	"$(VENV_PATH)/bin/pip" install --upgrade pip
	"$(VENV_PATH)/bin/pip" install --upgrade -r requirements.txt

venv-ssp:
	# Include system installed site-packages and add just missing modules
	"$(SYSTEM_PYTHON)" -m venv --system-site-packages "$(VENV_PATH)"
	"$(VENV_PATH)/bin/pip" install --upgrade pip
	"$(VENV_PATH)/bin/pip" install --upgrade -r requirements.txt

.PHONY: venv venv-ssp

# Choose python interpreter from venv or system
PYTHON = $(or $(wildcard $(VENV_PATH)/bin/python), $(SYSTEM_PYTHON))

# Read app version from program
APP_VERSION = $(shell "$(PYTHON)" src/$(PACKAGE) --version | cut -d ' ' -f 2)

# Environment info
venv-info:
	@echo Environment for $(APP_NAME) $(APP_VERSION)
	@echo Using path: "$(VENV_PATH)"

.PHONY: venv-info

## Compile Qt UI files to python code
build-ui:
	cd ui_dev && for ui_file in *.ui; do \
		file_name=$${ui_file%.ui}; \
		"$(PYTHON)" -m PyQt5.uic.pyuic $${ui_file} -o ../src/$(PACKAGE)/ui/$${file_name}_ui.py -x --from-imports; \
		echo $${file_name}; \
	done

build-rc:
	cd ui_dev && for rc_file in *.qrc; do \
		file_name=$${rc_file%.qrc}; \
		"$(PYTHON)" -m PyQt5.pyrcc_main $${rc_file} -o ../src/$(PACKAGE)/ui/$${file_name}_rc.py; \
		echo $${file_name}; \
	done

update-translation:
	"$(PYTHON)" -m PyQt5.pylupdate_main translate.pro

.PHONY: build-ui build-rc update-translation

## Build steps
build:
	"$(PYTHON)" -m setup sdist
	"$(PYTHON)" -m setup bdist_wheel

install: build
	"$(PYTHON)" -m pip install dist/$(PACKAGE)-$(APP_VERSION)-*.whl

uninstall:
	"$(PYTHON)" -m pip uninstall --yes $(PACKAGE)

.PHONY: test build install uninstall

## PyInstaller
app-licenses:
	mkdir -p dist
	# Create a list of all installed libraries, their versions and licenses
	"$(PYTHON)" -m piplicenses \
		--format=markdown \
		--output-file dist/bundled-libraries.md
	# Create a list of installed libraries with complete project information
	"$(PYTHON)" -m piplicenses \
		--with-authors \
		--with-urls \
		--with-description \
		--with-license-file \
		--no-license-path \
		--format=json \
		--output-file dist/open-source-licenses.json
	"$(PYTHON)" -m piplicenses \
		--with-authors \
		--with-urls \
		--with-description \
		--with-license-file \
		--no-license-path \
		--format=plain-vertical \
		--output-file dist/open-source-licenses.txt

app: build-ui build-rc app-licenses
	"$(PYTHON)" -m PyInstaller -n $(APP_NAME) \
		--collect-submodules=zeroconf \
		--add-data="src/$(PACKAGE)/locale:./$(PACKAGE)/locale" \
		--add-data="dist/bundled-libraries.md:$(PACKAGE)/open-source-licenses" \
		--add-data="dist/open-source-licenses.*:$(PACKAGE)/open-source-licenses" \
		--add-data="data/$(PACKAGE).ico:." \
		--add-data="data/$(PACKAGE).png:." \
		--icon=data/$(PACKAGE).ico \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
		src/$(PACKAGE)/__main__.py

app-mac: build-ui build-rc app-licenses
	"$(PYTHON)" -m PyInstaller -n $(APP_NAME) \
		--collect-submodules=zeroconf \
		--add-data="src/$(PACKAGE)/locale:./$(PACKAGE)/locale" \
		--add-data="dist/bundled-libraries.md:$(PACKAGE)/open-source-licenses" \
		--add-data="dist/open-source-licenses.*:$(PACKAGE)/open-source-licenses" \
		--add-data="data/$(PACKAGE).icns:." \
		--icon=data/$(PACKAGE).icns \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
		--osx-bundle-identifier $APP_IDENT \
		--codesign-identity $(APPLE_SIG) \
		src/$(PACKAGE)/__main__.py

app-mac-dmg: app-mac
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

.PHONY: app-licenses app app-mac app-mac-dmg

## Clean
clean:
	# PyTest caches
	rm -rf .pytest_cache
	# Build artifacts
	rm -rf build dist src/*.egg-info
	# PyInstaller created files
	rm -rf *.spec
	# Pycaches
	find . -type d -name '__pycache__' -exec rm -r {} \+

distclean: clean
	# Virtual environment
	rm -rf "$(VENV_PATH)"

.PHONY: clean distclean
