# -*- coding: utf-8 -*-
"""Options for MQTT system."""

__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

from PyQt5 import QtGui, QtWidgets

from . import proginit as pi
from .ui.mqttmanager_ui import Ui_diag_mqtt


class MqttManager(QtWidgets.QDialog, Ui_diag_mqtt):
    """MQTT settings for option window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.dc = {}

    def _changesdone(self):
        """
        Check for unsaved changes in dialog.

        :return: True, if unsaved changes was found
        """
        return (
            not self.dc or
            self.dc["mqttbasetopic"] != self.txt_basetopic.text() or
            self.dc["mqttsendinterval"] != self.sbx_sendinterval.value() or
            self.dc["mqttsend_on_event"] != int(self.cbx_send_on_event.isChecked()) or
            self.dc["mqttwrite_outputs"] != int(self.cbx_write_outputs.isChecked()) or
            self.dc["mqttbroker_address"] != self.txt_broker_address.text() or
            self.dc["mqtttls_set"] != int(self.cbx_tls_set.isChecked()) or
            self.dc["mqttport"] != self.sbx_port.value() or
            self.dc["mqttusername"] != self.txt_username.text() or
            self.dc["mqttpassword"] != self.txt_password.text() or
            self.dc["mqttclient_id"] != self.txt_client_id.text()
        )

    def _load_settings(self):
        """Load values to GUI widgets."""
        try:
            self.txt_basetopic.setText(self.dc["mqttbasetopic"])
            self.sbx_sendinterval.setValue(self.dc["mqttsendinterval"])
            self.dc["mqttsend_on_event"] = int(self.cbx_send_on_event.isChecked())
            self.dc["mqttwrite_outputs"] = int(self.cbx_write_outputs.isChecked())
            self.txt_broker_address.setText(self.dc["mqttbroker_address"])
            self.cbx_tls_set.setChecked(bool(self.dc["mqtttls_set"]))
            self.sbx_port.setValue(self.dc["mqttport"])
            self.txt_username.setText(self.dc["mqttusername"])
            self.txt_password.setText(self.dc["mqttpassword"])
            self.txt_client_id.setText(self.dc["mqttclient_id"])
        except Exception as e:
            pi.logger.exception(e)
            self.dc = {}
            return False
        return True

    def accept(self) -> None:
        """Save values to value dict."""
        self.dc["mqttbasetopic"] = self.txt_basetopic.text()
        self.dc["mqttsendinterval"] = self.sbx_sendinterval.value()
        self.dc["mqttsend_on_event"] = int(self.cbx_send_on_event.isChecked())
        self.dc["mqttwrite_outputs"] = int(self.cbx_write_outputs.isChecked())
        self.dc["mqttbroker_address"] = self.txt_broker_address.text()
        self.dc["mqtttls_set"] = int(self.cbx_tls_set.isChecked())
        self.dc["mqttport"] = self.sbx_port.value()
        self.dc["mqttusername"] = self.txt_username.text()
        self.dc["mqttpassword"] = self.txt_password.text()
        self.dc["mqttclient_id"] = self.txt_client_id.text()
        super().accept()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self._changesdone():
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
        """Load settings from dc and show dialog."""
        if not self._load_settings():
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not load the MQTT settings dialog. Missing values!"
                )
            )
            return QtWidgets.QDialog.Rejected
        return super().exec()

    def reject(self) -> None:
        """Reject settings."""
        self._load_settings()
        super().reject()

    @property
    def read_only(self):
        """Getter for read_only value."""
        return not self.txt_basetopic.isEnabled()

    @read_only.setter
    def read_only(self, value: bool):
        """Setter for read_only window."""
        self.txt_basetopic.setEnabled(not value)
        self.sbx_sendinterval.setEnabled(not value)
        self.cbx_send_on_event.setEnabled(not value)
        self.cbx_write_outputs.setEnabled(not value)
        self.txt_broker_address.setEnabled(not value)
        self.sbx_port.setEnabled(not value)
        self.cbx_tls_set.setEnabled(not value)
        self.txt_username.setEnabled(not value)
        self.txt_password.setEnabled(not value)
        self.txt_client_id.setEnabled(not value)
        if value:
            self.btn_box.setStandardButtons(
                QtWidgets.QDialogButtonBox.Cancel
            )
        else:
            self.btn_box.setStandardButtons(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
