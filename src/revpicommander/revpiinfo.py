# -*- coding: utf-8 -*-
"""Program information of local an remote system."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

from PyQt5 import QtCore, QtGui, QtWidgets

from . import helper
from .ui.revpiinfo_ui import Ui_diag_revpiinfo


class RevPiInfo(QtWidgets.QDialog, Ui_diag_revpiinfo):
    """Version information window."""

    def __init__(self, version: str, parent=None):
        super(RevPiInfo, self).__init__(parent)
        self.setupUi(self)

        self._debug_load = False

        self.lbl_version_control.setText(version)
        self.lbl_version_control.mousePressEvent = self.lbl_version_mousePressEvent

    def exec(self) -> int:
        self.lbl_version_pyload.setText(
            "{0}.{1}.{2}".format(*helper.cm.pyload_version)
            if helper.cm.connected else "-"
        )
        self._load_lst_files()
        return super(RevPiInfo, self).exec()

    def lbl_version_mousePressEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.MidButton:
            self._debug_load = not self._debug_load
            self._load_lst_files()

    def _load_lst_files(self):
        """Load files from working dir on Revolution Pi."""
        self.lst_files.clear()

        if self._debug_load:
            lst = helper.cm.xml_funcs
        elif helper.cm.connected:
            lst = helper.cm.call_remote_function(
                "get_filelist",
                default_value=[self.tr("Can not load file list")]
            )
        else:
            lst = [self.tr("Not connected")]

        lst.sort()
        self.lst_files.insertItems(0, lst)
