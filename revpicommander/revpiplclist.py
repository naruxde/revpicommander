# -*- coding: utf-8 -*-
"""Saved connections of Revolution Pi devices."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "GPLv3"

from enum import IntEnum

from PyQt5 import QtCore, QtGui, QtWidgets

import helper
import proginit as pi
from helper import WidgetData
from ui.revpiplclist_ui import Ui_diag_connections


class NodeType(IntEnum):
    CON = 1000
    DIR = 1001


class RevPiPlcList(QtWidgets.QDialog, Ui_diag_connections):
    """Manage your saved connections."""

    def __init__(self, parent=None):
        super(RevPiPlcList, self).__init__(parent)
        self.setupUi(self)
        self.__default_name = self.tr("New connection")
        self.__default_port = 55123

        self.__current_item = QtWidgets.QTreeWidgetItem()  # type: QtWidgets.QTreeWidgetItem
        self.changes = True

        self.tre_connections.setColumnWidth(0, 250)
        self.lbl_port.setText(self.lbl_port.text().format(self.__default_port))
        self.sbx_port.setValue(self.__default_port)

    def _load_settings(self):
        """Load values to GUI widgets."""
        pi.logger.debug("RevPiPlcList._load_settings")

        self.tre_connections.clear()
        self.cbb_folder.clear()
        self.cbb_folder.addItem("")
        for i in range(helper.settings.beginReadArray("connections")):
            helper.settings.setArrayIndex(i)

            con_item = QtWidgets.QTreeWidgetItem(NodeType.CON)
            con_item.setIcon(0, QtGui.QIcon(":/main/ico/cpu.ico"))
            con_item.setText(0, helper.settings.value("name", "Revolution Pi", str))
            con_item.setText(1, helper.settings.value("address", "127.0.0.1", str))
            con_item.setData(0, WidgetData.port, helper.settings.value("port", self.__default_port, int))
            con_item.setData(0, WidgetData.timeout, helper.settings.value("timeout", 5, int))

            con_item.setData(0, WidgetData.last_dir_upload, helper.settings.value("last_dir_upload"))
            con_item.setData(0, WidgetData.last_file_upload, helper.settings.value("last_file_upload"))
            con_item.setData(0, WidgetData.last_dir_pictory, helper.settings.value("last_dir_pictory"))
            con_item.setData(0, WidgetData.last_dir_picontrol, helper.settings.value("last_dir_picontrol"))
            con_item.setData(0, WidgetData.last_dir_selected, helper.settings.value("last_dir_selected"))
            con_item.setData(0, WidgetData.last_pictory_file, helper.settings.value("last_pictory_file"))
            con_item.setData(0, WidgetData.last_tar_file, helper.settings.value("last_tar_file"))
            con_item.setData(0, WidgetData.last_zip_file, helper.settings.value("last_zip_file"))
            con_item.setData(0, WidgetData.watch_files, helper.settings.value("watch_files"))
            con_item.setData(0, WidgetData.watch_path, helper.settings.value("watch_path"))
            con_item.setData(0, WidgetData.debug_geos, helper.settings.value("debug_geos"))

            folder = helper.settings.value("folder", "", str)
            if folder:
                sub_folder = self._get_folder_item(folder)
                if sub_folder is None:
                    sub_folder = QtWidgets.QTreeWidgetItem(NodeType.DIR)
                    sub_folder.setIcon(0, QtGui.QIcon(":/main/ico/folder.ico"))
                    sub_folder.setText(0, folder)
                    self.tre_connections.addTopLevelItem(sub_folder)
                    self.cbb_folder.addItem(folder)

                sub_folder.addChild(con_item)
            else:
                self.tre_connections.addTopLevelItem(con_item)

        helper.settings.endArray()

        self.tre_connections.expandAll()
        self.changes = True

        if self.tre_connections.topLevelItemCount() == 0:
            self._edit_state()

    def accept(self) -> None:
        pi.logger.debug("RevPiPlcList.accept")

        def set_settings(node: QtWidgets.QTreeWidgetItem):
            parent = node.parent()
            helper.settings.setValue("address", node.text(1))
            helper.settings.setValue("folder", parent.text(0) if parent else "")
            helper.settings.setValue("name", node.text(0))
            helper.settings.setValue("port", node.data(0, WidgetData.port))
            helper.settings.setValue("timeout", node.data(0, WidgetData.timeout))

            if node.data(0, WidgetData.last_dir_upload):
                helper.settings.setValue("last_dir_upload", node.data(0, WidgetData.last_dir_upload))
            if node.data(0, WidgetData.last_file_upload):
                helper.settings.setValue("last_file_upload", node.data(0, WidgetData.last_file_upload))
            if node.data(0, WidgetData.last_dir_pictory):
                helper.settings.setValue("last_dir_pictory", node.data(0, WidgetData.last_dir_pictory))
            if node.data(0, WidgetData.last_dir_picontrol):
                helper.settings.setValue("last_dir_picontrol", node.data(0, WidgetData.last_dir_picontrol))
            if node.data(0, WidgetData.last_dir_selected):
                helper.settings.setValue("last_dir_selected", node.data(0, WidgetData.last_dir_selected))
            if node.data(0, WidgetData.last_pictory_file):
                helper.settings.setValue("last_pictory_file", node.data(0, WidgetData.last_pictory_file))
            if node.data(0, WidgetData.last_tar_file):
                helper.settings.setValue("last_tar_file", node.data(0, WidgetData.last_tar_file))
            if node.data(0, WidgetData.last_zip_file):
                helper.settings.setValue("last_zip_file", node.data(0, WidgetData.last_zip_file))
            if node.data(0, WidgetData.watch_files):
                helper.settings.setValue("watch_files", node.data(0, WidgetData.watch_files))
            if node.data(0, WidgetData.watch_path):
                helper.settings.setValue("watch_path", node.data(0, WidgetData.watch_path))
            if node.data(0, WidgetData.debug_geos):
                helper.settings.setValue("debug_geos", node.data(0, WidgetData.debug_geos))

        helper.settings.remove("connections")
        helper.settings.beginWriteArray("connections")

        counter_index = 0
        for i in range(self.tre_connections.topLevelItemCount()):
            root_item = self.tre_connections.topLevelItem(i)
            if root_item.type() == NodeType.DIR:
                for k in range(root_item.childCount()):
                    helper.settings.setArrayIndex(counter_index)
                    set_settings(root_item.child(k))
                    counter_index += 1
            elif root_item.type() == NodeType.CON:
                helper.settings.setArrayIndex(counter_index)
                set_settings(root_item)
                counter_index += 1

        helper.settings.endArray()

        self.changes = False
        super(RevPiPlcList, self).accept()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pi.logger.debug("RevPiPlcList.closeEvent")
        if self.changes:
            ask = QtWidgets.QMessageBox.question(
                self, self.tr("Question"), self.tr(
                    "Do you really want to quit? \nUnsaved changes will be lost."
                )
            ) == QtWidgets.QMessageBox.Yes

            if ask:
                self.reject()
            else:
                a0.ignore()

    def exec(self) -> int:
        self._load_settings()
        return super(RevPiPlcList, self).exec()

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_btn_box_clicked(self, button: QtWidgets.QAbstractButton):
        if self.btn_box.buttonRole(button) == QtWidgets.QDialogButtonBox.DestructiveRole:
            self.reject()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Connection management

    def _edit_state(self):
        item = self.tre_connections.currentItem()
        if item is None:
            up_ok = False
            down_ok = False
            con_item = False
            dir_item = False
        else:
            con_item = item.type() == NodeType.CON
            dir_item = item.type() == NodeType.DIR

            if item.parent():
                index = item.parent().indexOfChild(item)
                up_ok = index > 0
                down_ok = index < item.parent().childCount() - 1
            else:
                index = self.tre_connections.indexOfTopLevelItem(item)
                up_ok = index > 0
                down_ok = index < self.tre_connections.topLevelItemCount() - 1

        self.btn_up.setEnabled(up_ok)
        self.btn_down.setEnabled(down_ok)
        self.btn_delete.setEnabled(con_item)
        self.txt_name.setEnabled(con_item)
        self.txt_address.setEnabled(con_item)
        self.sbx_port.setEnabled(con_item)
        self.sbx_timeout.setEnabled(con_item)
        self.cbb_folder.setEnabled(con_item or dir_item)

    def _get_folder_item(self, name: str):
        """Find the folder entry by name."""
        for i in range(self.tre_connections.topLevelItemCount()):
            tli = self.tre_connections.topLevelItem(i)
            if tli.type() == NodeType.DIR and tli.text(0) == name:
                return tli
        return None

    def _move_item(self, count: int):
        """Move connection item up or down"""
        item = self.tre_connections.currentItem()
        if not item:
            return

        if item.parent():
            dir_item = item.parent()
            index = dir_item.indexOfChild(item)
            new_index = index + count
            if 0 <= new_index < dir_item.childCount():
                item = dir_item.takeChild(index)
                dir_item.insertChild(new_index, item)
        else:
            index = self.tre_connections.indexOfTopLevelItem(item)
            new_index = index + count
            if 0 <= index < self.tre_connections.topLevelItemCount():
                item = self.tre_connections.takeTopLevelItem(index)
                self.tre_connections.insertTopLevelItem(new_index, item)

        self.tre_connections.setCurrentItem(item)
        self._edit_state()

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidgetItem)
    def on_tre_connections_currentItemChanged(
            self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):

        self._edit_state()
        if current and current.type() == NodeType.CON:
            self.__current_item = current
            self.txt_name.setText(current.text(0))
            self.txt_address.setText(current.text(1))
            self.sbx_port.setValue(current.data(0, WidgetData.port))
            self.sbx_timeout.setValue(current.data(0, WidgetData.timeout))
            if current.parent() is None:
                self.cbb_folder.setCurrentIndex(0)
            else:
                self.cbb_folder.setCurrentText(current.parent().text(0))
        elif current and current.type() == NodeType.DIR:
            self.__current_item = current
            self.cbb_folder.setCurrentText(current.text(0))
        else:
            self.__current_item = QtWidgets.QTreeWidgetItem()
            self.cbb_folder.setCurrentText(current.text(0) if current else "")

    @QtCore.pyqtSlot()
    def on_btn_up_pressed(self):
        self._move_item(-1)

    @QtCore.pyqtSlot()
    def on_btn_down_pressed(self):
        self._move_item(1)

    @QtCore.pyqtSlot()
    def on_btn_delete_pressed(self):
        """Remove selected entry."""
        item = self.tre_connections.currentItem()
        if item and item.type() == NodeType.CON:
            dir_node = item.parent()
            if dir_node:
                dir_node.removeChild(item)
            else:
                index = self.tre_connections.indexOfTopLevelItem(item)
                self.tre_connections.takeTopLevelItem(index)

        self._edit_state()

    @QtCore.pyqtSlot()
    def on_btn_add_pressed(self):
        """Create new element."""
        self.__current_item = QtWidgets.QTreeWidgetItem(NodeType.CON)
        self.__current_item.setIcon(0, QtGui.QIcon(":/main/ico/cpu.ico"))
        self.__current_item.setText(0, self.__default_name)
        self.__current_item.setData(0, WidgetData.port, self.__default_port)
        self.__current_item.setData(0, WidgetData.timeout, 5)
        sub_folder = self._get_folder_item(self.cbb_folder.currentText())
        if sub_folder:
            sub_folder.addChild(self.__current_item)
        else:
            self.tre_connections.addTopLevelItem(self.__current_item)

        self.tre_connections.setCurrentItem(self.__current_item)
        self.txt_name.setFocus()
        self.txt_name.selectAll()

    @QtCore.pyqtSlot(str)
    def on_txt_name_textEdited(self, text):
        if self.__current_item.type() != NodeType.CON:
            return
        self.__current_item.setText(0, text)

    @QtCore.pyqtSlot(str)
    def on_txt_address_textEdited(self, text):
        if self.__current_item.type() != NodeType.CON:
            return
        self.__current_item.setText(1, text)

    @QtCore.pyqtSlot(int)
    def on_sbx_port_valueChanged(self, value: int):
        if self.__current_item.type() != NodeType.CON:
            return
        self.__current_item.setData(0, WidgetData.port, value)

    @QtCore.pyqtSlot(int)
    def on_sbx_timeout_valueChanged(self, value: int):
        if self.__current_item.type() != NodeType.CON:
            return
        self.__current_item.setData(0, WidgetData.timeout, value)

    @QtCore.pyqtSlot(str)
    def on_cbb_folder_editTextChanged(self, text: str):
        pi.logger.debug("RevPiPlcList.on_cbb_folder_editTextChanged({0})".format(text))

        if self.__current_item.type() == NodeType.DIR:
            # We just have to rename the dir node
            self.__current_item.setText(0, text)

        elif self.__current_item.type() == NodeType.CON:
            sub_folder = self._get_folder_item(text)
            dir_node = self.__current_item.parent()
            if dir_node:
                if dir_node.text(0) == text:
                    # It is the same folder
                    return

                if text != "" and dir_node.childCount() == 1 and not sub_folder:
                    # The folder hold just one item, so we can rename that
                    for i in range(self.cbb_folder.count()):
                        if self.cbb_folder.itemText(i) == dir_node.text(0):
                            self.cbb_folder.setItemText(i, text)
                            break
                    dir_node.setText(0, text)
                    return

                index = dir_node.indexOfChild(self.__current_item)
                self.__current_item = dir_node.takeChild(index)

            elif text != "":
                # Move root to folder
                index = self.tre_connections.indexOfTopLevelItem(self.__current_item)
                self.__current_item = self.tre_connections.takeTopLevelItem(index)

            else:
                # Root stays root
                return

            if text == "":
                self.tre_connections.addTopLevelItem(self.__current_item)

            else:
                if sub_folder is None:
                    sub_folder = QtWidgets.QTreeWidgetItem(NodeType.DIR)
                    sub_folder.setIcon(0, QtGui.QIcon(":/main/ico/folder.ico"))
                    sub_folder.setText(0, text)
                    self.tre_connections.addTopLevelItem(sub_folder)
                    self.cbb_folder.addItem(text)
                sub_folder.addChild(self.__current_item)

            if dir_node and dir_node.childCount() == 0:
                # Remove empty folders
                for i in range(self.cbb_folder.count()):
                    if self.cbb_folder.itemText(i) == dir_node.text(0):
                        self.cbb_folder.removeItem(i)
                        break
                index = self.tre_connections.indexOfTopLevelItem(dir_node)
                self.tre_connections.takeTopLevelItem(index)

            self.tre_connections.setCurrentItem(self.__current_item)
            self.cbb_folder.setFocus()

    # endregion # # # # #
