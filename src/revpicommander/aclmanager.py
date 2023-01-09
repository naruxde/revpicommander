# -*- coding: utf-8 -*-
"""Manager for ACL lists."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

from re import compile

from PyQt5 import QtCore, QtGui, QtWidgets

from .helper import WidgetData
from .ui.aclmanager_ui import Ui_diag_aclmanager


class AclManager(QtWidgets.QDialog, Ui_diag_aclmanager):
    """ACL manager."""

    def __init__(self, parent=None):
        super(AclManager, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.__re_ipacl = compile(r"(25[0-5]|(2[0-4]|[01]?\d|)\d)(\.(25[0-5]|(2[0-4]|[01]?\d|)\d)){3},-1")
        self.__dict_acltext = {}
        self.__cbb_level_loaded_index = 0
        self.__mrk_message_shown = 0
        self.__oldacl = ""
        self.__read_only = False

        # Prepare GUI
        self.tb_acls.setColumnWidth(0, 300)
        self.tb_acls.setColumnWidth(1, 50)
        self.btn_edit.setEnabled(False)
        self.btn_remove.setEnabled(False)
        self.btn_add.setEnabled(False)

        # Move to next focus when enter a "."
        self.mrk_txt_ip_a_keyPressEvent = self.txt_ip_a.keyPressEvent
        self.mrk_txt_ip_b_keyPressEvent = self.txt_ip_b.keyPressEvent
        self.mrk_txt_ip_c_keyPressEvent = self.txt_ip_c.keyPressEvent
        self.mrk_txt_ip_d_keyPressEvent = self.txt_ip_d.keyPressEvent
        self.txt_ip_a.keyPressEvent = self.txt_ip_a_keyPressEvent
        self.txt_ip_b.keyPressEvent = self.txt_ip_b_keyPressEvent
        self.txt_ip_c.keyPressEvent = self.txt_ip_c_keyPressEvent
        self.txt_ip_d.keyPressEvent = self.txt_ip_d_keyPressEvent

    def __check_load_error(self):
        """
        Check load errors and shows a message one time.
        :return: True, if message was shown
        """
        if bool(self.__mrk_message_shown & 1):
            return False

        for row in range(self.tb_acls.rowCount()):
            if self.tb_acls.item(row, 0).data(WidgetData.has_error):
                self.__mrk_message_shown += 1
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error"), self.tr(
                        "There are errors in the ACL list!\nCheck the ALC levels of the "
                        "red lines in the table. The ACL levels or ip addresses are "
                        "invalid. If you save this dialog again, we will remove the "
                        "wrong entries automatically."
                    )
                )
                return True
        return False

    def _changes_done(self):
        """
        Check for unsaved changes in dialog.

        :return: True, if unsaved changes was found
        """
        return self.__table_to_acl() != self.__oldacl

    def accept(self) -> None:
        """Save settings."""
        if self.btn_add.isEnabled():
            # Entry is ready to save, did the user forgot to click the button?
            ask = QtWidgets.QMessageBox.question(
                self, self.tr("Unsaved entry"), self.tr(
                    "You worked on a new ACL entry. Do you want to save "
                    "that entry, too?"
                )
            ) == QtWidgets.QMessageBox.Yes
            if ask:
                self.on_btn_add_clicked()

        if self.__check_load_error():
            return

        self.__oldacl = self.__table_to_acl()
        super(AclManager, self).accept()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self._changes_done():
            ask = QtWidgets.QMessageBox.question(
                self, self.tr("Question"), self.tr(
                    "Do you really want to quit? \nUnsaved changes will be lost"
                )
            ) == QtWidgets.QMessageBox.Yes

            if ask:
                self.reject()
            else:
                a0.ignore()

    def exec(self) -> int:
        return super(AclManager, self).exec()

    def reject(self) -> None:
        """Restore old settings."""
        self.setup_acl_manager(self.__oldacl, self.__dict_acltext)
        super(AclManager, self).reject()

    def setup_acl_manager(self, acl_string: str, acl_texts: dict):
        if type(acl_string) != str:
            raise TypeError("acl_string must be <class 'str'>")
        if type(acl_texts) != dict:
            raise TypeError("acl_texts must be <class 'dict'>")

        self.__dict_acltext = acl_texts.copy()

        # Clean up widgets
        while self.tb_acls.rowCount() > 0:
            self.tb_acls.removeRow(0)
        self.cbb_level.clear()
        self.cbb_level.addItem(self.tr("Select..."), -1)
        self.lbl_level_info.clear()

        self.__re_ipacl = compile(
            r"([\d*]{1,3}\.){3}[\d*]{1,3},[" +
            str(min(self.__dict_acltext.keys(), default=0)) + r"-" +
            str(max(self.__dict_acltext.keys(), default=0)) + r"]"
        )

        for ip_level in acl_string.split(" "):
            self.__table_add_acl(ip_level)

        lst_level_text = []
        for level in sorted(self.__dict_acltext.keys()):
            level_text = self.tr("Level") + " {0}: {1}".format(level, self.__dict_acltext[level])
            lst_level_text.append(level_text)
            self.cbb_level.addItem(level_text, level)

        self.lbl_level_info.setText("\n".join(lst_level_text))
        self.__oldacl = self.__table_to_acl()

    def get_acl(self):
        """Get current ACL string."""
        return self.__oldacl

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: ACL list

    def __load_selected_entry(self):
        row = self.tb_acls.currentRow()
        if row < 0:
            return

        item = self.tb_acls.item(row, 0)
        ip_blocks = item.text().split(".")
        self.txt_ip_a.setText(ip_blocks[0])
        self.txt_ip_b.setText(ip_blocks[1])
        self.txt_ip_c.setText(ip_blocks[2])
        self.txt_ip_d.setText(ip_blocks[3])

        for index in range(self.cbb_level.count()):
            if self.cbb_level.itemData(index, QtCore.Qt.UserRole) == item.data(WidgetData.acl_level):
                self.__cbb_level_loaded_index = index
                self.cbb_level.setCurrentIndex(index)
                break

        self._check_all_filled()

    def __table_add_acl(self, ip_level: str):
        """Add ACL entry to table."""
        # Empty acl_string create empty ip_level
        if not ip_level:
            return

        ip, level = ip_level.split(",")
        if self.__re_ipacl.match(ip_level):
            brush = QtGui.QBrush()
            has_error = False
            tool_tip = ""
        else:
            brush = QtGui.QBrush(QtGui.QColor("red"))
            has_error = True
            tool_tip = self.tr("This entry has an invalid ACL level or wrong IP format!")

        for row in range(self.tb_acls.rowCount()):
            item_0 = self.tb_acls.item(row, 0)
            if item_0.text() == ip:
                item_1 = self.tb_acls.item(row, 1)

                # Update existing entry
                item_0.setData(WidgetData.acl_level, int(level))
                item_0.setData(WidgetData.has_error, has_error)
                item_0.setBackground(brush)
                item_0.setToolTip(tool_tip)
                item_1.setText(level)
                item_1.setBackground(brush)
                item_1.setToolTip(tool_tip)
                return

        row_count = self.tb_acls.rowCount()
        self.tb_acls.insertRow(row_count)

        item = QtWidgets.QTableWidgetItem(ip)
        item.setData(WidgetData.acl_level, int(level))
        item.setData(WidgetData.has_error, has_error)
        item.setBackground(brush)
        item.setToolTip(tool_tip)
        self.tb_acls.setItem(row_count, 0, item)

        item = QtWidgets.QTableWidgetItem(level)
        item.setBackground(brush)
        item.setToolTip(tool_tip)
        self.tb_acls.setItem(row_count, 1, item)

    def __table_to_acl(self, force=False, row_indexes=None):
        """
        Create acl string with valid entries only.

        :param force: If True, return all entries
        :param row_indexes: Only from indexes ist <class 'list'>
        :return: ACL string
        """
        if row_indexes is None:
            row_indexes = range(self.tb_acls.rowCount())

        buff_acl = ""
        for i in row_indexes:
            item = self.tb_acls.item(i, 0)
            ip_level = "{0},{1} ".format(item.text(), item.data(WidgetData.acl_level))
            if not (force or self.__re_ipacl.match(ip_level)):
                continue
            buff_acl += ip_level
        return buff_acl.strip()

    @QtCore.pyqtSlot(QtWidgets.QTableWidgetItem)
    def on_tb_acls_itemDoubleClicked(self, item: QtWidgets.QTableWidgetItem):
        if not self.__read_only:
            self.__load_selected_entry()

    @QtCore.pyqtSlot()
    def on_tb_acls_itemSelectionChanged(self):
        selected_rows = int(len(self.tb_acls.selectedItems()) / self.tb_acls.columnCount())
        self.btn_edit.setEnabled(not self.__read_only and selected_rows == 1)
        self.btn_remove.setEnabled(not self.__read_only and selected_rows > 0)

    @QtCore.pyqtSlot()
    def on_btn_edit_clicked(self):
        self.__load_selected_entry()

    @QtCore.pyqtSlot()
    def on_btn_remove_clicked(self):
        lst_selected_row_indexes = [mi.row() for mi in self.tb_acls.selectionModel().selectedRows(0)]
        if len(lst_selected_row_indexes) == 0:
            return

        str_remove = ""
        for ip_level in self.__table_to_acl(True, lst_selected_row_indexes).split(" "):
            if not ip_level:
                # Empty string will return empty field
                continue
            ip, level = ip_level.split(",")
            str_remove += "\nIP: {0:>15}\tLevel: {1}".format(ip, level)

        ask = QtWidgets.QMessageBox.question(
            self, self.tr("Question"), self.tr(
                "Do you really want to delete the following items?\n{0}"
            ).format(str_remove)
        ) == QtWidgets.QMessageBox.Yes

        if ask:
            # Turn order to start deleting from the button to preserve right indexes
            lst_selected_row_indexes.sort(reverse=True)
            for row in lst_selected_row_indexes:
                self.tb_acls.removeRow(row)

    # endregion # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Group box IP

    def _check_all_filled(self):
        all_filled = \
            len(self.txt_ip_a.text()) > 0 and \
            len(self.txt_ip_b.text()) > 0 and \
            len(self.txt_ip_c.text()) > 0 and \
            len(self.txt_ip_d.text()) > 0 and \
            self.cbb_level.currentIndex() != 0 and (
                self.txt_ip_a.isModified() or self.txt_ip_b.isModified() or
                self.txt_ip_c.isModified() or self.txt_ip_d.isModified() or
                self.cbb_level.currentIndex() != self.__cbb_level_loaded_index
            )

        self.btn_add.setEnabled(not self.__read_only and all_filled)

    def _move_ip_cursor(self, key: int, sender_widget: QtWidgets.QLineEdit,
                        last_widget: QtWidgets.QLineEdit, next_widget: QtWidgets.QLineEdit):
        """
        Move cursor between ip enter widgets.

        :param key: Pressed key to check
        :param sender_widget: Sender widget of this key
        :param last_widget: Set focus to this widget on backspace key
        :param next_widget: Set focus to this widget on period key
        :return: True, if the key should not be processed further
        """
        if last_widget and key == QtCore.Qt.Key_Backspace and len(sender_widget.text()) == 0:
            last_widget.setFocus()
        elif next_widget and key == QtCore.Qt.Key_Period:
            next_widget.setFocus()
            return True
        return False

    def txt_ip_a_keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self._move_ip_cursor(a0.key(), self.txt_ip_a, self.txt_ip_a, self.txt_ip_b):
            self.mrk_txt_ip_a_keyPressEvent(a0)

    def txt_ip_b_keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self._move_ip_cursor(a0.key(), self.txt_ip_b, self.txt_ip_a, self.txt_ip_c):
            self.mrk_txt_ip_b_keyPressEvent(a0)

    def txt_ip_c_keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self._move_ip_cursor(a0.key(), self.txt_ip_c, self.txt_ip_b, self.txt_ip_d):
            self.mrk_txt_ip_c_keyPressEvent(a0)

    def txt_ip_d_keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self._move_ip_cursor(a0.key(), self.txt_ip_d, self.txt_ip_c, self.txt_ip_d):
            self.mrk_txt_ip_d_keyPressEvent(a0)

    @QtCore.pyqtSlot(str)
    def on_txt_ip_a_textChanged(self, text: str):
        self._check_all_filled()

    @QtCore.pyqtSlot(str)
    def on_txt_ip_b_textChanged(self, text: str):
        self._check_all_filled()

    @QtCore.pyqtSlot(str)
    def on_txt_ip_c_textChanged(self, text: str):
        self._check_all_filled()

    @QtCore.pyqtSlot(str)
    def on_txt_ip_d_textChanged(self, text: str):
        self._check_all_filled()

    @QtCore.pyqtSlot(int)
    def on_cbb_level_currentIndexChanged(self, index: int):
        self._check_all_filled()

    @QtCore.pyqtSlot()
    def on_btn_add_clicked(self):
        """Add a new entry to acl table."""
        ip_level = "{0}.{1}.{2}.{3},{4}".format(
            self.txt_ip_a.text(),
            self.txt_ip_b.text(),
            self.txt_ip_c.text(),
            self.txt_ip_d.text(),
            self.cbb_level.currentData(QtCore.Qt.UserRole)
        )
        if self.__re_ipacl.match(ip_level):
            self.__table_add_acl(ip_level)
            self.on_btn_clear_clicked()
        else:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not save new ACL entry! Check format of ip address "
                    "and acl level is in value list."
                )
            )

    @QtCore.pyqtSlot()
    def on_btn_clear_clicked(self):
        """Clear entry widgets."""
        self.txt_ip_a.clear()
        self.txt_ip_b.clear()
        self.txt_ip_c.clear()
        self.txt_ip_d.clear()
        self.cbb_level.setCurrentIndex(0)
        self.__cbb_level_loaded_index = 0

    # endregion # # # # #

    @property
    def read_only(self):
        """Getter for read_only value."""
        return self.__read_only

    @read_only.setter
    def read_only(self, value):
        """Setter for read_only window."""
        self.__read_only = value
        self.txt_ip_a.setEnabled(not value)
        self.txt_ip_b.setEnabled(not value)
        self.txt_ip_c.setEnabled(not value)
        self.txt_ip_d.setEnabled(not value)
        self.cbb_level.setEnabled(not value)
        self.btn_clear.setEnabled(not value)
        if value:
            self.btn_box.setStandardButtons(
                QtWidgets.QDialogButtonBox.Cancel
            )
        else:
            self.btn_box.setStandardButtons(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )


# Debugging
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = AclManager(None)
    win.setup_acl_manager(
        "127.0.1.*,0 127.0.0.1,1 127.0.0.2,2", {
            0: "Just have a look",
            1: "Do more things",
        }
    )
    win.read_only = False
    rc = win.exec()
    print(
        "return code:", rc,
        "acl:", win.get_acl()
    )
