# -*- coding: utf-8 -*-
"""Saved connections of Revolution Pi devices."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

from enum import IntEnum

import keyring
from PyQt5 import QtCore, QtGui, QtWidgets
from keyring.errors import KeyringError

from . import helper
from . import proginit as pi
from .helper import RevPiSettings, WidgetData
from .ui.revpiplclist_ui import Ui_diag_connections


class NodeType(IntEnum):
    CON = 1000
    DIR = 1001


class RevPiPlcList(QtWidgets.QDialog, Ui_diag_connections):
    """Manage your saved connections."""

    def __init__(self, parent=None):
        super(RevPiPlcList, self).__init__(parent)
        self.setupUi(self)
        self.__default_port = 55123

        self.__current_item = QtWidgets.QTreeWidgetItem()  # type: QtWidgets.QTreeWidgetItem
        self.changes = True
        self._keyring_cleanup_id_user = []

        self.tre_connections.setColumnWidth(0, 250)
        self.lbl_port.setText(self.lbl_port.text().format(self.__default_port))
        self.sbx_port.setValue(self.__default_port)

    def _load_settings(self):
        """Load values to GUI widgets."""
        pi.logger.debug("RevPiPlcList._load_settings")

        self.tre_connections.clear()
        self.cbb_folder.clear()
        self.cbb_folder.addItem("")

        # Get length of array and close it, the RevPiSettings-class need it
        count_settings = helper.settings.beginReadArray("connections")
        helper.settings.endArray()

        for i in range(count_settings):
            settings = RevPiSettings(i)

            con_item = QtWidgets.QTreeWidgetItem(NodeType.CON)
            con_item.setIcon(0, QtGui.QIcon(":/main/ico/cpu.ico"))
            con_item.setText(0, settings.name)
            con_item.setText(1, settings.address)

            con_item.setData(0, WidgetData.revpi_settings, settings)

            folder = settings.folder
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

        self.tre_connections.expandAll()
        self.changes = False

        if self.tre_connections.topLevelItemCount() == 0:
            self._edit_state()

    def accept(self) -> None:
        pi.logger.debug("RevPiPlcList.accept")

        for internal_id, ssh_user in self._keyring_cleanup_id_user:
            service_name = "{0}.{1}_{2}".format(
                helper.settings.applicationName(),
                helper.settings.organizationName(),
                internal_id
            )
            try:
                # Remove information from os keyring, which we collected on_btn_delete_clicked
                keyring.delete_password(service_name, ssh_user)
            except KeyringError as e:
                pi.logger.error(e)

        helper.settings.remove("connections")

        for i in range(self.tre_connections.topLevelItemCount()):
            root_item = self.tre_connections.topLevelItem(i)
            if root_item.type() == NodeType.DIR:
                for k in range(root_item.childCount()):
                    revpi_settings = root_item.child(k).data(0, WidgetData.revpi_settings)  # type: RevPiSettings
                    revpi_settings.folder = root_item.text(0)
                    revpi_settings.save_settings()
            elif root_item.type() == NodeType.CON:
                revpi_settings = root_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
                revpi_settings.folder = ""
                revpi_settings.save_settings()

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

    def exec_with_presets(self, presets: RevPiSettings) -> int:
        """
        Start dialog with new created settings object and presets.

        :param presets: Use these settings as preset
        :return: Dialog status
        """
        self._load_settings()
        self.on_btn_add_clicked(presets)
        return super(RevPiPlcList, self).exec()

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_btn_box_clicked(self, button: QtWidgets.QAbstractButton):
        if self.btn_box.buttonRole(button) == QtWidgets.QDialogButtonBox.DestructiveRole:
            self.reject()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Connection management

    def _edit_state(self):
        """Set enabled status of all controls, depending on selected item."""
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

        self.cbx_ssh_use_tunnel.setEnabled(con_item)
        self.sbx_ssh_port.setEnabled(con_item)
        self.txt_ssh_user.setEnabled(con_item)

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
            self.tre_connections.expandItem(dir_item)
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

            settings = current.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
            self.txt_name.setText(settings.name)
            self.txt_address.setText(settings.address)
            self.sbx_port.setValue(settings.port)
            self.sbx_timeout.setValue(settings.timeout)
            if current.parent() is None:
                self.cbb_folder.setCurrentIndex(0)
            else:
                self.cbb_folder.setCurrentText(current.parent().text(0))

            self.cbx_ssh_use_tunnel.setChecked(settings.ssh_use_tunnel)
            self.sbx_ssh_port.setValue(settings.ssh_port)
            self.txt_ssh_user.setText(settings.ssh_user)

        elif current and current.type() == NodeType.DIR:
            self.__current_item = current
            self.cbb_folder.setCurrentText(current.text(0))

        else:
            self.__current_item = QtWidgets.QTreeWidgetItem()
            self.cbb_folder.setCurrentText(current.text(0) if current else "")

    @QtCore.pyqtSlot()
    def on_btn_up_clicked(self):
        self._move_item(-1)

    @QtCore.pyqtSlot()
    def on_btn_down_clicked(self):
        self._move_item(1)

    @QtCore.pyqtSlot()
    def on_btn_delete_clicked(self):
        """Remove selected entry."""
        item = self.tre_connections.currentItem()
        if item and item.type() == NodeType.CON:

            revpi_settings = item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
            if revpi_settings.ssh_saved_password:
                # Cleans up keyring in save function
                self._keyring_cleanup_id_user.append((revpi_settings.internal_id, revpi_settings.ssh_user))

            dir_node = item.parent()
            if dir_node:
                dir_node.removeChild(item)
            else:
                index = self.tre_connections.indexOfTopLevelItem(item)
                self.tre_connections.takeTopLevelItem(index)

        self._edit_state()

    @QtCore.pyqtSlot()
    def on_btn_add_clicked(self, settings_preset: RevPiSettings = None):
        """Create new element."""
        settings = settings_preset or RevPiSettings()
        new_item = QtWidgets.QTreeWidgetItem(NodeType.CON)
        new_item.setIcon(0, QtGui.QIcon(":/main/ico/cpu.ico"))
        new_item.setText(0, settings.name)
        new_item.setData(0, WidgetData.revpi_settings, settings)
        sub_folder = self._get_folder_item(self.cbb_folder.currentText())
        if sub_folder:
            sub_folder.addChild(new_item)
        else:
            self.tre_connections.addTopLevelItem(new_item)

        # This will load all settings and prepare widgets
        self.tre_connections.setCurrentItem(new_item)
        self.txt_name.setFocus()
        self.txt_name.selectAll()

    @QtCore.pyqtSlot(str)
    def on_txt_name_textEdited(self, text):
        if self.__current_item.type() != NodeType.CON:
            return
        self.__current_item.setText(0, text)
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.name = text
        self.changes = True

    @QtCore.pyqtSlot(str)
    def on_txt_address_textEdited(self, text):
        if self.__current_item.type() != NodeType.CON:
            return
        self.__current_item.setText(1, text)
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.address = text
        self.changes = True

    @QtCore.pyqtSlot(int)
    def on_sbx_port_valueChanged(self, value: int):
        if self.__current_item.type() != NodeType.CON:
            return
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.port = value
        self.changes = True

    @QtCore.pyqtSlot(int)
    def on_sbx_timeout_valueChanged(self, value: int):
        if self.__current_item.type() != NodeType.CON:
            return
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.timeout = value
        self.changes = True

    @QtCore.pyqtSlot(int)
    def on_cbx_ssh_use_tunnel_stateChanged(self, check_state: int):
        if self.__current_item.type() != NodeType.CON:
            return
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.ssh_use_tunnel = check_state == QtCore.Qt.CheckState.Checked
        self.changes = True

    @QtCore.pyqtSlot(int)
    def on_sbx_ssh_port_valueChanged(self, value: int):
        if self.__current_item.type() != NodeType.CON:
            return
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.ssh_port = value
        self.changes = True

    @QtCore.pyqtSlot(str)
    def on_txt_ssh_user_textEdited(self, text):
        if self.__current_item.type() != NodeType.CON:
            return
        settings = self.__current_item.data(0, WidgetData.revpi_settings)  # type: RevPiSettings
        settings.ssh_user = text
        self.changes = True

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
