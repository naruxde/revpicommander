# -*- coding: utf-8 -*-
"""Open-Source softwrae licenses."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

from json import load
from logging import getLogger
from os.path import exists
from typing import List

from PyQt5 import QtCore, QtWidgets

from revpicommander.ui.oss_licenses_ui import Ui_diag_oss_licenses

log = getLogger(__name__)


class OssLicenses(QtWidgets.QDialog, Ui_diag_oss_licenses):
    def __init__(self, oss_license_file: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._lst_licenses: List[dict] = []
        self._oss_license_file = oss_license_file

        self.action_start.setVisible(exists(oss_license_file))

    def _load_license_file(self) -> None:
        if exists(self._oss_license_file):
            try:
                with open(self._oss_license_file) as fh:
                    self._lst_licenses = load(fh)
            except Exception as e:
                log.error("Could not load oss license file: '{0}'".format(e))

        for i in range(len(self._lst_licenses)):
            dict_license = self._lst_licenses[i]
            tb_item_name = QtWidgets.QTableWidgetItem(dict_license.get("Name", ""))
            tb_item_name.setData(QtCore.Qt.UserRole, i)
            tb_item_license = QtWidgets.QTableWidgetItem(dict_license.get("License", ""))
            tb_item_license.setToolTip(tb_item_license.text())
            tb_item_license.setData(QtCore.Qt.UserRole, i)

            self.tb_oss_licenses.insertRow(i)
            self.tb_oss_licenses.setItem(i, 0, tb_item_name)
            self.tb_oss_licenses.setItem(i, 1, tb_item_license)

        self.tb_oss_licenses.resizeColumnsToContents()

    def exec(self) -> int:
        # Prevent loading every time the program is starting
        if not self._lst_licenses:
            self._load_license_file()

        return super().exec()

    @QtCore.pyqtSlot(QtWidgets.QTableWidgetItem, QtWidgets.QTableWidgetItem)
    def on_tb_oss_licenses_currentItemChanged(
        self,
        current: QtWidgets.QTableWidgetItem,
        previous: QtWidgets.QTableWidgetItem,
    ):
        log.debug("Enter slot on_tb_oss_licenses_currentItemChanged")
        license_index = current.data(QtCore.Qt.UserRole)
        license_object = self._lst_licenses[license_index]
        license_object["LicenseText"] = license_object["LicenseText"].replace("\n", "<br>")
        self.txt_license.setHtml(
            """<h2>{Name}</h2>
<p>{Description}</p>
<p>
    <ul>
        <li>Version: {Version}</li>
        <li>Author: {Author}</li>
        <li>URL: <a href="{URL}">{URL}</a></li>
    </ul>
</p>
<h3>License: {License}</h3>
<p>
    <code>{LicenseText}</code>
</p>""".format(
                **license_object
            )
        )
