# -*- coding: utf-8 -*-
"""Saved connections of Revolution Pi devices."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

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
        super().__init__(parent)
        self.setupUi(self)
        self.__default_port = 55123

        self.__current_item = QtWidgets.QTreeWidgetItem()  # type: QtWidgets.QTreeWidgetItem
        self.changes = True
        self._keyring_cleanup_id_user = []

        self.tre_connections.setColumnWidth(0, 250)
        self.lbl_port.setText(self.lbl_port.text().format(self.__default_port))
        self.sbx_port.setValue(self.__default_port)

        # Dirty workaround to remove default button to prevent action on ENTER key, while user edit texts
        self.__btn_dummy = QtWidgets.QPushButton(self)
        self.__btn_dummy.setVisible(False)
        self.__btn_dummy.setDefault(True)

    def _load_cbb_folder(self):
        """Clean up all entries and reload existing ones from treeview."""
        self.cbb_folder.blockSignals(True)

        self.cbb_folder.clear()
        self.cbb_folder.addItem("")
        for i in range(self.tre_connections.topLevelItemCount()):
            item = self.tre_connections.topLevelItem(i)
            if item.type() != NodeType.DIR:
                continue
            self.cbb_folder.addItem(item.text(0))

        self.cbb_folder.blockSignals(False)

    def _load_settings(self):
        """Load values to GUI widgets."""
        pi.logger.debug("RevPiPlcList._load_settings")

        self.tre_connections.clear()

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

                sub_folder.addChild(con_item)
            else:
                self.tre_connections.addTopLevelItem(con_item)

        self.tre_connections.expandAll()
        self.changes = False

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
        super().accept()

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
        return super().exec()

    def exec_with_presets(self, presets: RevPiSettings) -> int:
        """
        Start dialog with new created settings object and presets.

        :param presets: Use these settings as preset
        :return: Dialog status
        """
        self._load_settings()
        self.on_btn_add_clicked(presets)
        return super().exec()

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_btn_box_clicked(self, button: QtWidgets.QAbstractButton):
        if self.btn_box.buttonRole(button) == QtWidgets.QDialogButtonBox.DestructiveRole:
            self.reject()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Connection management

    def _edit_state(self):
        """Set enabled status of all controls, depending on selected item."""
        pi.logger.debug("RevPiPlcList._edit_state")

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
        self.btn_delete.setEnabled(con_item or dir_item)
        self.txt_name.setEnabled(con_item)
        self.txt_address.setEnabled(con_item)
        self.sbx_port.setEnabled(con_item)
        self.sbx_timeout.setEnabled(con_item)
        self.cbb_folder.setEnabled(con_item or dir_item)
        self.cbb_folder.setEditable(dir_item)
        if self.cbb_folder.isEditable():
            # Disable auto complete, this would override a new typed name with existing one
            self.cbb_folder.setCompleter(None)

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
        else:
            index = self.tre_connections.indexOfTopLevelItem(item)
            new_index = index + count
            if 0 <= index < self.tre_connections.topLevelItemCount():
                item = self.tre_connections.takeTopLevelItem(index)
                self.tre_connections.insertTopLevelItem(new_index, item)
                if item.type() == NodeType.DIR:
                    # Expand a moved dir node, it would be collapsed after move
                    self.tre_connections.expandItem(item)

        self.tre_connections.setCurrentItem(item)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidgetItem)
    def on_tre_connections_currentItemChanged(
            self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):

        self._edit_state()
        self._load_cbb_folder()

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

        def remove_item(item: QtWidgets.QTreeWidgetItem):
            """Remove CON item and save keyring actions for save action."""
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

        item_to_remove = self.tre_connections.currentItem()

        if item_to_remove and item_to_remove.type() == NodeType.DIR:
            if item_to_remove.childCount():
                rc = QtWidgets.QMessageBox.question(
                    self, self.tr("Question"), self.tr(
                        "If you remote this folder, all containing elements will be removed, too. \n\n"
                        "Do you want to delete folder and all elements?"
                    ),
                )
                if rc != QtWidgets.QMessageBox.Yes:
                    return

                while item_to_remove.childCount() > 0:
                    remove_item(item_to_remove.child(0))

            item_index = self.tre_connections.indexOfTopLevelItem(item_to_remove)
            self.tre_connections.takeTopLevelItem(item_index)

        elif item_to_remove and item_to_remove.type() == NodeType.CON:
            remove_item(item_to_remove)

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

    @QtCore.pyqtSlot()
    def on_btn_add_dir_clicked(self):
        """Add a new folder."""
        folder_text = self.tr("New folder")
        sub_folder = QtWidgets.QTreeWidgetItem(NodeType.DIR)
        sub_folder.setIcon(0, QtGui.QIcon(":/main/ico/folder.ico"))
        sub_folder.setText(0, folder_text)

        self.tre_connections.addTopLevelItem(sub_folder)
        self.tre_connections.setCurrentItem(sub_folder)
        self.cbb_folder.setFocus()

        self.changes = True

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
    def on_cbb_folder_currentIndexChanged(self, text: str):
        pi.logger.debug("RevPiPlcList.on_cbb_folder_currentIndexChanged({0})".format(text))

        if self.__current_item.type() == NodeType.CON:
            new_dir_node = self._get_folder_item(text)
            current_dir_node = self.__current_item.parent()
            if current_dir_node == new_dir_node:
                # No change required, both nodes are the same
                return

            change_item = self.__current_item
            self.tre_connections.blockSignals(True)
            self.changes = True

            if current_dir_node:
                # Move an element to other folder or root
                index = current_dir_node.indexOfChild(change_item)
                change_item = current_dir_node.takeChild(index)

            else:
                # Move a root element to a folder
                index = self.tre_connections.indexOfTopLevelItem(change_item)
                change_item = self.tre_connections.takeTopLevelItem(index)

            if text == "":
                self.tre_connections.addTopLevelItem(change_item)

            else:
                new_dir_node.addChild(change_item)

            self.tre_connections.blockSignals(False)
            self.tre_connections.setCurrentItem(change_item)

    @QtCore.pyqtSlot(str)
    def on_cbb_folder_editTextChanged(self, text: str):
        pi.logger.debug("RevPiPlcList.on_cbb_folder_editTextChanged({0})".format(text))

        if self.__current_item.type() == NodeType.DIR and self.__current_item.text(0) != text:
            # We just have to rename the dir node
            self.__current_item.setText(0, text)
            self.changes = True

    # endregion # # # # #
