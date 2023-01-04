SHELL := bash

build_ui:
	cd ui_dev && for ui_file in *.ui; do \
		file_name=$${ui_file%.ui}; \
		pyuic5 $${ui_file} -o ../src/revpicommander/ui/$${file_name}_ui.py -x --from-imports; \
		echo $${file_name}; \
	done
	cd ui_dev && for rc_file in *.qrc; do \
		file_name=$${rc_file%.qrc}; \
		pyrcc5 $${rc_file} -o ../src/revpicommander/ui/$${file_name}_rc.py; \
		echo $${file_name}; \
	done

update_translation:
	pylupdate5 translate.pro

installer_mac:
	pyinstaller -n "RevPi Commander" \
		--add-data="src/revpicommander/locale:locale" \
		--add-data="data/revpicommander.icns:." \
		--icon=data/revpicommander.icns \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
		src/revpicommander/__main__.py

installer_win:
	pyinstaller -n "RevPi Commander" \
		--add-data="src\\revpicommander\\locale;.\\locale" \
		--add-data="data\\revpicommander.ico;." \
		--icon=data\\revpicommander.ico \
		--noconfirm \
		--clean \
		--onedir \
		--windowed \
        src/revpicommander\__main__.py
