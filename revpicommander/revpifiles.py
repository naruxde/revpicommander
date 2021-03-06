# -*- coding: utf-8 -*-
"""File manager for up und download PLC program."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2020 Sven Sager"
__license__ = "GPLv3"

import gzip
import os
from enum import IntEnum
from xmlrpc.client import Binary

from PyQt5 import QtCore, QtGui, QtWidgets

import helper
import proginit as pi
from backgroundworker import BackgroundWorker
from helper import WidgetData
from ui.files_ui import Ui_win_files


class NodeType(IntEnum):
    FILE = 1000
    DIR = 1001


class UploadFiles(BackgroundWorker):

    def __init__(self, file_list: list, parent):
        super(UploadFiles, self).__init__(parent)
        self.ec = 1
        self.file_list = file_list
        self.plc_program_included = False  # Will be True, when opt_program was found in files

    def run(self) -> None:
        self.steps_todo.emit(len(self.file_list))

        # Get config to find actual auto start program for warnings
        opt_program = helper.cm.call_remote_function("get_config", default_value={})
        opt_program = opt_program.get("plcprogram", "none.py")

        progress_counter = 0
        for file_name in self.file_list:
            progress_counter += 1

            # Remove base dir of file to set relative for PyLoad
            send_name = file_name.replace(helper.cm.develop_watch_path, "")[1:]
            self.status_message.emit(send_name)

            # Check whether this is the auto start program
            if send_name == opt_program:
                self.plc_program_included = True


            # Transfer file
            try:
                with open(file_name, "rb") as fh:
                    upload_status = helper.cm.call_remote_function(
                        "plcupload", Binary(gzip.compress(fh.read())), send_name,
                        default_value=False
                    )
            except Exception as e:
                pi.logger.error(e)
                self.ec = -2
                return

            if not upload_status:
                self.ec = -1
                return

            self.steps_done.emit(progress_counter)
            if self.check_cancel():
                return

        self.ec = 0


class RevPiFiles(QtWidgets.QMainWindow, Ui_win_files):

    def __init__(self, parent=None):
        super(RevPiFiles, self).__init__(parent)
        self.setupUi(self)

        self.dc_settings = {}
        self.tree_files_counter = 0
        self.tree_files_counter_max = 10000
        self.lbl_path_local.setText(helper.cm.develop_watch_path or self.tr("Please select..."))
        self.lbl_path_local.setToolTip(self.lbl_path_local.text())

        self.btn_all.setEnabled(False)
        self.btn_to_left.setEnabled(False)
        self.btn_to_right.setEnabled(False)
        self.btn_delete_revpi.setEnabled(False)

        if helper.cm.develop_watch_path:
            self._load_files_local(True)
        if helper.cm.connected:
            self._load_files_revpi(True)

        self.restoreGeometry(helper.settings.value("files/geo", b''))
        self.splitter.setSizes(list(map(int, helper.settings.value("files/splitter", [0, 0]))))

    def __del__(self):
        pi.logger.debug("RevPiFiles.__del__")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pi.logger.debug("RevPiFiles.closeEvent")
        helper.settings.setValue("files/geo", self.saveGeometry())
        helper.settings.setValue("files/splitter", self.splitter.sizes())

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

        uploader = UploadFiles(self.file_list_local(), self)
        if uploader.exec_dialog() == QtWidgets.QDialog.Rejected:
            return

        if uploader.ec == 0:
            # Tell user, we did not find the auto start program in files
            if not uploader.plc_program_included:
                QtWidgets.QMessageBox.information(
                    self, self.tr("Information"), self.tr(
                        "A PLC program has been uploaded. Please check the "
                        "PLC program settings to see if the correct program "
                        "is specified as the start program."
                    )
                )

        elif uploader.ec == -1:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The Revolution Pi could not process some parts of the "
                    "transmission."
                )
            )

        elif uploader.ec == -2:
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
        state_local = len(self.tree_files_local.selectedItems()) > 0
        state_revpi = len(self.tree_files_revpi.selectedItems()) > 0

        self.btn_all.setEnabled(state_local)
        self.btn_to_right.setEnabled(state_local)

        if "plcdeletefile" not in helper.cm.xml_funcs:
            self.btn_delete_revpi.setEnabled(False)
            self.btn_delete_revpi.setToolTip(self.tr("The RevPiPyLoad version on the Revolution Pi is to old."))
        else:
            self.btn_delete_revpi.setEnabled(state_revpi)
        if "plcdownload_file" not in helper.cm.xml_funcs:
            self.btn_to_left.setEnabled(False)
            self.btn_to_left.setToolTip(self.tr("The RevPiPyLoad version on the Revolution Pi is to old."))
        elif not helper.cm.develop_watch_path:
            self.btn_to_left.setEnabled(False)
            self.btn_to_left.setToolTip(self.tr("Choose a local directory first."))
        else:
            self.btn_to_left.setEnabled(state_revpi)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Tree management

    @staticmethod
    def _parent_selection_state(item: QtWidgets.QTreeWidgetItem):
        """Set selected, if all children are selected."""
        if item.parent():
            all_selected = True
            for i in range(item.parent().childCount()):
                if not item.parent().child(i).isSelected():
                    all_selected = False
                    break
            item.parent().setSelected(all_selected)

    def _select_children(self, top_item: QtWidgets.QTreeWidgetItem, value: bool):
        """Recursive select children from parent."""
        pi.logger.debug("RevPiFiles._select_children")

        for i in range(top_item.childCount()):
            item = top_item.child(i)
            if item.type() == NodeType.DIR:
                item.setSelected(value)
                self._select_children(item, value)
            elif item.type() == NodeType.FILE:
                item.setSelected(value)

    def __item_selection_changed(self, tree_view: QtWidgets.QTreeView):
        """Manager vor item selection of three views."""
        item = tree_view.currentItem()
        if item is None:
            return

        pi.logger.debug("RevPiFiles.__itemSelectionChanged")

        # Block while preselect other entries
        tree_view.blockSignals(True)

        if item.type() == NodeType.DIR:
            self._select_children(item, item.isSelected())
        elif item.type() == NodeType.FILE:
            self._parent_selection_state(item)

        tree_view.blockSignals(False)

        self._set_gui_control_states()

    @QtCore.pyqtSlot()
    def on_tree_files_local_itemSelectionChanged(self):
        self.__item_selection_changed(self.tree_files_local)
        helper.cm.develop_watch_files = self.file_list_local()

    @QtCore.pyqtSlot()
    def on_tree_files_revpi_itemSelectionChanged(self):
        self.__item_selection_changed(self.tree_files_revpi)

    # endregion # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Local file lists

    def __insert_files_local(self, base_dir: str, child=None):
        """
        Recursively add files to tree view.

        :param base_dir: Directory to scan for files
        :param child: Child widget to add new widgets
        """
        if not os.path.exists(base_dir):
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not open last directory '{0}'."
                ).format(base_dir)
            )
            return

        for de in os.scandir(base_dir):  # type: os.DirEntry

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

                self.__insert_files_local(de.path, item)

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
                self._parent_selection_state(item)

    def _load_files_local(self, silent=False):
        """
        Refresh the file list.

        :param silent: Do not show message boxes
        """
        pi.logger.debug("RevPiFiles._load_files_local")

        self.tree_files_counter = 0
        self.tree_files_local.blockSignals(True)
        self.tree_files_local.clear()
        self.__insert_files_local(helper.cm.develop_watch_path)
        self.tree_files_local.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tree_files_local.blockSignals(False)

        if not silent and self.tree_files_counter > self.tree_files_counter_max:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Stop scanning for files, because we found more than {0} files."
                ).format(self.tree_files_counter_max)
            )

        self._set_gui_control_states()

    def file_list_local(self):
        """Generate a file list with full path of selected entries."""
        pi.logger.debug("RevPiFiles.file_list_local")
        lst = []
        for item in self.tree_files_local.selectedItems():
            if item.type() == NodeType.DIR:
                # We just want files
                continue
            lst.append(item.data(0, WidgetData.file_name))

        return lst

    # endregion # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: RevPi file lists

    def _load_files_revpi(self, silent=False):
        """
        Refresh the file list of revolution pi.

        :param silent: Do not show message boxes
        """
        pi.logger.debug("RevPiFiles._load_files_revpi")

        self.tree_files_revpi.blockSignals(True)
        self.tree_files_revpi.clear()
        self.tree_files_revpi.blockSignals(False)

        if not helper.cm.connected:
            lst_revpi = None
        else:
            lst_revpi = helper.cm.call_remote_function("get_filelist")
            # Just load settings once
            if not self.dc_settings:
                self.dc_settings = helper.cm.call_remote_function("get_config", default_value={})
                self.lbl_path_revpi.setText(
                    self.dc_settings.get("plcworkdir", self.tr("Could not load path of working dir"))
                )
                self.lbl_path_revpi.setToolTip(self.lbl_path_revpi.text())

        if lst_revpi is not None:
            lst_revpi.sort()

            for path_file in lst_revpi:
                lst_path_file = path_file.split("/")
                dir_node = None  # type: QtWidgets.QTreeWidgetItem

                for folder in lst_path_file[:-1]:
                    new_dir_node = QtWidgets.QTreeWidgetItem(NodeType.DIR)
                    new_dir_node.setText(0, folder)
                    new_dir_node.setIcon(0, QtGui.QIcon(":/main/ico/folder.ico"))

                    if dir_node:
                        # Subfolder of top level
                        for i in range(dir_node.childCount()):
                            item = dir_node.child(i)
                            if item.type() != NodeType.DIR:
                                continue
                            if item.text(0) == new_dir_node.text(0):
                                dir_node = item
                                new_dir_node = None
                                break
                        if new_dir_node:
                            dir_node.addChild(new_dir_node)
                            dir_node = new_dir_node
                    else:
                        # Search in top level
                        for i in range(self.tree_files_revpi.topLevelItemCount()):
                            item = self.tree_files_revpi.topLevelItem(i)
                            if item.type() != NodeType.DIR:
                                continue
                            if item.text(0) == new_dir_node.text(0):
                                dir_node = item
                                new_dir_node = None
                                break
                        if new_dir_node:
                            self.tree_files_revpi.addTopLevelItem(new_dir_node)
                            dir_node = new_dir_node

                # This is the file name
                object_name = lst_path_file[-1]
                item = QtWidgets.QTreeWidgetItem(NodeType.FILE)
                item.setText(0, object_name)
                item.setData(0, WidgetData.file_name, path_file)
                item.setIcon(0, QtGui.QIcon(
                    ":/file/ico/file-else.ico" if object_name.find(".py") == -1 else
                    ":/file/ico/file-python.ico"
                ))
                if dir_node:
                    dir_node.addChild(item)
                else:
                    self.tree_files_revpi.addTopLevelItem(item)

            self.tree_files_revpi.sortItems(0, QtCore.Qt.AscendingOrder)

        elif not silent:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not load file list from Revolution Pi."
                )
            )

        self._set_gui_control_states()

    def file_list_revpi(self):
        """Generate a file list with full path of selected entries."""
        pi.logger.debug("RevPiFiles.file_list_revpi")
        lst = []
        for item in self.tree_files_revpi.selectedItems():
            if item.type() == NodeType.DIR:
                # We just want files
                continue
            lst.append(item.data(0, WidgetData.file_name))

        return lst

    # endregion # # # # #

    @QtCore.pyqtSlot()
    def on_btn_all_pressed(self):
        pi.logger.debug("RevPiFiles.on_btn_all_pressed")
        self._do_my_job(True)
        self.file_list_revpi()

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
        self.lbl_path_local.setToolTip(self.lbl_path_local.text())
        helper.cm.develop_watch_path = selected_dir
        helper.cm.develop_watch_files = []

        self._load_files_local(False)

    @QtCore.pyqtSlot()
    def on_btn_refresh_local_pressed(self):
        pi.logger.debug("RevPiFiles.on_btn_refresh_pressed")
        self._load_files_local(False)

    @QtCore.pyqtSlot()
    def on_btn_refresh_revpi_pressed(self):
        pi.logger.debug("RevPiFiles.on_btn_refresh_revpi_pressed")
        self._load_files_revpi(False)

    @QtCore.pyqtSlot()
    def on_btn_to_right_pressed(self):
        """Upload selected files to revolution pi."""
        pi.logger.debug("RevPiFiles.on_btn_to_right_pressed")
        self._do_my_job(False)
        self._load_files_revpi(True)

    @QtCore.pyqtSlot()
    def on_btn_to_left_pressed(self):
        """Download selected file."""
        pi.logger.debug("RevPiFiles.on_btn_to_left_pressed")

        override = None
        for item in self.tree_files_revpi.selectedItems():
            if item.type() != NodeType.FILE:
                continue

            file_name = item.data(0, WidgetData.file_name)
            rc = helper.cm.call_remote_function(
                "plcdownload_file", file_name,
                default_value=Binary()
            )
            rc = rc.data
            if not rc:
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error..."), self.tr(
                        "Error while download file '{0}'."
                    ).format(file_name)
                )
            else:
                file_name = os.path.join(helper.cm.develop_watch_path, file_name)
                if override is None and os.path.exists(file_name):
                    rc_diag = QtWidgets.QMessageBox.question(
                        self, self.tr("Override files..."), self.tr(
                            "One or more files does exist on your computer! Do you want to override the existing"
                            "files?\n\nSelect 'Yes' to override, 'No' to download only missing files."
                        ),
                        buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
                    )
                    if rc_diag == QtWidgets.QMessageBox.Cancel:
                        return
                    override = rc_diag == QtWidgets.QMessageBox.Yes

                if os.path.exists(file_name) and not override:
                    pi.logger.debug("Skip existing file '{0}'".format(file_name))
                    continue

                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                file_data = gzip.decompress(rc)
                with open(os.path.join(helper.cm.develop_watch_path, file_name), "wb") as fh:
                    fh.write(file_data)

        self._load_files_local()

    @QtCore.pyqtSlot()
    def on_btn_delete_revpi_pressed(self):
        """Remove selected files from working directory on revolution pi."""
        pi.logger.debug("RevPiFiles.btn_delete_revpi_pressed")

        lst_delete = []
        for item in self.tree_files_revpi.selectedItems():
            if item.type() == NodeType.FILE:
                lst_delete.append(item.data(0, WidgetData.file_name))

        rc = QtWidgets.QMessageBox.question(
            self, self.tr("Delete files from Revolution Pi..."), self.tr(
                "Do you want to delete {0} files from revolution pi?"
            ).format(len(lst_delete))
        )
        if rc != QtWidgets.QMessageBox.Yes:
            return

        for file_name in lst_delete:
            rc = helper.cm.call_remote_function("plcdeletefile", file_name, default_value=False)
            if not rc:
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error..."), self.tr(
                        "Error while delete file '{0}'."
                    ).format(file_name)
                )

        self._load_files_revpi()
