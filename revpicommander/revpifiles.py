# -*- coding: utf-8 -*-
"""File manager for up und download PLC program."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2020 Sven Sager"
__license__ = "GPLv3"

import gzip
import os
from enum import IntEnum
from os import DirEntry, scandir
from xmlrpc.client import Binary

from PyQt5 import QtCore, QtGui, QtWidgets

import helper
import proginit as pi
from helper import WidgetData
from ui.files_ui import Ui_win_files


class NodeType(IntEnum):
    FILE = 1000
    DIR = 1001


class RevPiFiles(QtWidgets.QMainWindow, Ui_win_files):

    def __init__(self, parent=None):
        super(RevPiFiles, self).__init__(parent)
        self.setupUi(self)

        self.tree_files_counter = 0
        self.tree_files_counter_max = 10000
        self.lbl_path_local.setText(helper.cm.develop_watch_path or self.tr("Please select..."))

        self.btn_all.setEnabled(False)
        self.btn_to_left.setEnabled(False)
        self.btn_to_right.setEnabled(False)
        self.btn_delete.setEnabled(False)

        if helper.cm.develop_watch_path:
            self._load_path_files(True)

    def __del__(self):
        pi.logger.debug("RevPiFiles.__del__")

    def _do_my_job(self, stop_restart=True):
        """
        Upload the selected files and do a optionally restart.

        :param stop_restart: True will restart program
        """
        if not helper.cm.connected:
            return

        if stop_restart and helper.cm.call_remote_function("plcstop") is None:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not stop plc program on Revolution Pi."
                )
            )
            return

        # Get config to find actual auto start program for warnings
        opt_program = helper.cm.call_remote_function("get_config", default_value={})
        opt_program = opt_program.get("plcprogram", "none.py")
        uploaded = True  # Will be False, when opt_program was found in files
        ec = 0

        for file_name in self.file_list():
            # todo: Check exception of local file
            with open(file_name, "rb") as fh:
                # Remove base dir of file to set relative for PyLoad
                send_name = file_name.replace(helper.cm.develop_watch_path, "")[1:]

                # Check whether this is the auto start program
                if send_name == opt_program:
                    uploaded = False

                # Transfer file
                try:
                    upload_status = helper.cm.call_remote_function(
                        "plcupload", Binary(gzip.compress(fh.read())), send_name,
                        default_value=False
                    )
                except Exception as e:
                    pi.logger.error(e)
                    ec = -2
                    break

                if not upload_status:
                    ec = -1
                    break

        if ec == 0:
            # Tell user, we did not find the auto start program in files
            if uploaded:
                QtWidgets.QMessageBox.information(
                    self, self.tr("Information..."), self.tr(
                        "A PLC program has been uploaded. Please check the "
                        "PLC options to see if the correct program is "
                        "specified as the start program."
                    )
                )

        elif ec == -1:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The Revolution Pi could not process some parts of the "
                    "transmission."
                )
            )

        elif ec == -2:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"),
                self.tr("Errors occurred during transmission")
            )

        if stop_restart and helper.cm.call_remote_function("plcstart", default_value=1) != 0:
            QtWidgets.QMessageBox.warning(
                self, self.tr("Warning"), self.tr(
                    "Could not start the plc program on Revolution Pi."
                )
            )

    def _set_gui_control_states(self):
        """Setup states of actions and buttons."""
        state = len(self.tree_files_local.selectedItems()) > 0
        self.btn_all.setEnabled(state)
        self.btn_to_left.setEnabled(state)
        self.btn_to_right.setEnabled(state)
        self.btn_delete.setEnabled(state)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Tree management

    def __insert_files(self, base_dir: str, child=None):
        """
        Recursively add files to tree view.

        :param base_dir: Directory to scan for files
        :param child: Child widget to add new widgets
        """
        for de in os.scandir(base_dir):  # type: DirEntry

            if self.tree_files_counter > self.tree_files_counter_max:
                return

            if de.is_dir(follow_symlinks=False):
                item = QtWidgets.QTreeWidgetItem(NodeType.DIR)
                item.setText(0, de.name)
                item.setIcon(0, QtGui.QIcon(":/main/ico/folder.ico"))
                if child:
                    child.addChild(item)
                else:
                    self.tree_files_local.addTopLevelItem(item)

                self.__insert_files(de.path, item)

            elif de.is_file(follow_symlinks=False):
                self.tree_files_counter += 1

                item = QtWidgets.QTreeWidgetItem(NodeType.FILE)
                item.setText(0, de.name)
                item.setData(0, WidgetData.file_name, de.path)
                item.setIcon(0, QtGui.QIcon(
                    ":/file/ico/file-else.ico" if de.name.find(".py") == -1 else
                    ":/file/ico/file-python.ico"
                ))
                if child:
                    child.addChild(item)
                else:
                    self.tree_files_local.addTopLevelItem(item)

                item.setSelected(de.path in helper.cm.develop_watch_files)
                self._parent_selected(item)

    def __select_children(self, top_item: QtWidgets.QTreeWidgetItem, value: bool):
        """Recursive select files from directory."""
        pi.logger.debug("RevPiFiles.__select_children")

        for i in range(top_item.childCount()):
            item = top_item.child(i)
            if item.type() == NodeType.DIR:
                self.__select_children(item, value)
            elif item.type() == NodeType.FILE:
                item.setSelected(value)

    def _load_path_files(self, silent=False):
        """
        Refresh the file list.

        :param silent: Do not show message boxes
        """
        pi.logger.debug("RevPiFiles._load_path_files")

        self.tree_files_counter = 0
        self.tree_files_local.blockSignals(True)
        self.tree_files_local.clear()
        self.tree_files_local.blockSignals(False)

        self.__insert_files(helper.cm.develop_watch_path)
        self.tree_files_local.sortItems(0, QtCore.Qt.AscendingOrder)

        if not silent and self.tree_files_counter > self.tree_files_counter_max:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Stop scanning for files, because we found more than {0} files."
                ).format(self.tree_files_counter_max)
            )

        self._set_gui_control_states()

    def _parent_selected(self, item: QtWidgets.QTreeWidgetItem):
        """Check all children of a parent are selected."""
        if item.parent():
            all_selected = True
            for i in range(item.parent().childCount()):
                if not item.parent().child(i).isSelected():
                    all_selected = False
                    break
            item.parent().setSelected(all_selected)

    def file_list(self):
        """Generate a file list with full path of selected entries."""
        pi.logger.debug("RevPiFiles.file_list")
        lst = []
        for item in self.tree_files_local.selectedItems():
            if item.type() == NodeType.DIR:
                continue
            lst.append(item.data(0, WidgetData.file_name))

        return lst

    @QtCore.pyqtSlot()
    def on_tree_files_local_itemSelectionChanged(self):
        item = self.tree_files_local.currentItem()
        if item is None:
            return

        pi.logger.debug("RevPiFiles.on_tree_files_itemSelectionChanged")

        # Block while preselect other entries
        self.tree_files_local.blockSignals(True)

        if item.type() == NodeType.DIR:
            self.__select_children(item, item.isSelected())

        elif item.type() == NodeType.FILE:
            self._parent_selected(item)

        self.tree_files_local.blockSignals(False)

        self._set_gui_control_states()

        helper.cm.develop_watch_files = self.file_list()

    # endregion # # # # #

    @QtCore.pyqtSlot()
    def on_btn_all_pressed(self):
        pi.logger.debug("RevPiDevelop.on_btn_all_pressed")
        self._do_my_job(True)

    @QtCore.pyqtSlot()
    def on_btn_select_local_pressed(self):
        pi.logger.debug("RevPiFiles.on_btn_select_pressed")

        diag_folder = QtWidgets.QFileDialog(
            self, self.tr("Select folder..."),
            helper.cm.develop_watch_path,
        )
        diag_folder.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if diag_folder.exec() != QtWidgets.QFileDialog.Accepted:
            return

        selected_dir = diag_folder.selectedFiles()[0]

        if not os.access(selected_dir, os.R_OK):
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not access the folder '{0}' to read files."
                )
            )
            helper.cm.develop_watch_files = []
            helper.cm.develop_watch_path = ""
            return

        self.lbl_path_local.setText(selected_dir)
        helper.cm.develop_watch_path = selected_dir
        helper.cm.develop_watch_files = []

        self._load_path_files(False)

    @QtCore.pyqtSlot()
    def on_btn_refresh_local_pressed(self):
        pi.logger.debug("RevPiDevelop.on_btn_refresh_pressed")
        self._load_path_files(False)