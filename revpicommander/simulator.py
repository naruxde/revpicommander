# -*- coding: utf-8 -*-
"""Simulator for piControl."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2021 Sven Sager"
__license__ = "GPLv3"

from os import W_OK, access
from os.path import basename, dirname, exists, join

from PyQt5 import QtCore, QtGui, QtWidgets

import helper
from ui.simulator_ui import Ui_diag_simulator


class Simulator(QtWidgets.QDialog, Ui_diag_simulator):
    """
    This is a configuration dialog for the simulator of piControl. The
    selected values will be saved in QSettings section 'simulator' and can be
    accessed by simulator starting classes.
    """

    def __init__(self, parent=None):
        super(Simulator, self).__init__(parent)
        self.setupUi(self)
        self.clean_procimg = False
        self.max_items = 5

        self.cbb_history.addItem("", "")
        lst_configrsc = helper.settings.value("simulator/history_configrsc", [], list)
        lst_procimg = helper.settings.value("simulator/history_procimg", [], list)
        for i in range(len(lst_configrsc)):
            self.cbb_history.addItem(lst_configrsc[i], lst_procimg[i])

        self.cbx_stop_remove.setChecked(helper.settings.value("simulator/stop_remove", False, bool))
        self.rb_restart_pictory.setChecked(helper.settings.value("simulator/restart_pictory", False, bool))
        self.rb_restart_zero.setChecked(helper.settings.value("simulator/restart_zero", False, bool))

        self.btn_start_pictory.setEnabled(False)
        self.btn_start_empty.setEnabled(False)
        self.btn_start_nochange.setEnabled(False)

        self.txt_configrsc.textChanged.connect(self.on_txt_textChanged)
        self.txt_procimg.textChanged.connect(self.on_txt_textChanged)

    def _save_gui(self) -> None:
        helper.settings.setValue("simulator/stop_remove", self.cbx_stop_remove.isChecked())
        helper.settings.setValue("simulator/restart_pictory", self.rb_restart_pictory.isChecked())
        helper.settings.setValue("simulator/restart_zero", self.rb_restart_zero.isChecked())

    def accept(self) -> None:
        self.cbb_history.removeItem(0)
        if self.cbb_history.findText(self.txt_configrsc.text()) == -1:
            self.cbb_history.addItem(self.txt_configrsc.text(), self.txt_procimg.text())
        if self.cbb_history.count() > self.max_items:
            self.cbb_history.removeItem(self.max_items)

        helper.settings.setValue("simulator/configrsc", self.txt_configrsc.text())
        helper.settings.setValue("simulator/procimg", self.txt_procimg.text())
        self._save_gui()

        lst_configrsc = []
        lst_procimg = []
        for i in range(self.cbb_history.count()):
            lst_configrsc.append(self.cbb_history.itemText(i))
            lst_procimg.append(self.cbb_history.itemData(i))
        helper.settings.setValue("simulator/history_configrsc", lst_configrsc)
        helper.settings.setValue("simulator/history_procimg", lst_procimg)

        self.clean_procimg = self.sender() is self.btn_start_empty

        super(Simulator, self).accept()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._save_gui()

    @QtCore.pyqtSlot()
    def on_btn_configrsc_clicked(self) -> None:
        diag_open = QtWidgets.QFileDialog(
            self, self.tr("Select downloaded piCtory file..."),
            helper.settings.value("simulator/last_dir", ".", str),
            self.tr("piCtory file (*.rsc);;All files (*.*)")
        )
        diag_open.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        diag_open.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        diag_open.setDefaultSuffix("rsc")

        if diag_open.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_open.selectedFiles()) != 1:
            diag_open.deleteLater()
            return

        configrsc_file = diag_open.selectedFiles()[0]
        dir_name = dirname(configrsc_file)
        procimg_file = join(dir_name, "{0}.img".format(basename(configrsc_file).rsplit(".", maxsplit=1)[0]))
        self.txt_configrsc.setText(configrsc_file)
        self.txt_procimg.setText(procimg_file)

        helper.settings.setValue("simulator/last_dir", dir_name)
        diag_open.deleteLater()

    @QtCore.pyqtSlot(int)
    def on_cbb_history_currentIndexChanged(self, index: int) -> None:
        if index == 0:
            return
        self.txt_configrsc.setText(self.cbb_history.itemText(index))
        self.txt_procimg.setText(self.cbb_history.itemData(index))

    @QtCore.pyqtSlot(str)
    def on_txt_textChanged(self, text: str) -> None:
        configrsc_file = self.txt_configrsc.text()
        procimg_file = self.txt_procimg.text()
        if configrsc_file and procimg_file:
            file_access = access(procimg_file, W_OK)
            self.txt_info.setPlainText("configrsc=\"{0}\", procimg=\"{1}\"".format(configrsc_file, procimg_file))
            self.btn_start_pictory.setEnabled(file_access)
            self.btn_start_empty.setEnabled(file_access)
            self.btn_start_nochange.setEnabled(file_access and exists(procimg_file))
        else:
            self.txt_info.clear()
            self.btn_start_pictory.setEnabled(False)
            self.btn_start_empty.setEnabled(False)
            self.btn_start_nochange.setEnabled(False)
