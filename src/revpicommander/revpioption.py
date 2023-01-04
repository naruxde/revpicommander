# -*- coding: utf-8 -*-
"""RevPiPyLoad options window."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

from PyQt5 import QtCore, QtGui, QtWidgets

from . import helper
from . import proginit as pi
from .aclmanager import AclManager
from .mqttmanager import MqttManager
from .ui.revpioption_ui import Ui_diag_options


class RevPiOption(QtWidgets.QDialog, Ui_diag_options):
    """Set options of RevPiPyLoad."""

    def __init__(self, parent=None):
        super(RevPiOption, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.dc = {}
        self.acl_plcslave = ""
        self.acl_xmlrpc = ""
        self.mrk_xml_ask = True

        self._dict_mqttsettings = {
            "mqttbasetopic": "revpi01",
            "mqttclient_id": "",
            "mqttbroker_address": "127.0.0.1",
            "mqttpassword": "",
            "mqttport": 1883,
            "mqttsend_on_event": 0,
            "mqttsendinterval": 30,
            "mqtttls_set": 0,
            "mqttusername": "",
            "mqttwrite_outputs": 0,
        }

        self.diag_aclmanager = AclManager(self)
        self.rejected.connect(self.diag_aclmanager.reject)
        self.diag_mqttmanager = MqttManager(self)
        self.rejected.connect(self.diag_mqttmanager.reject)
        self.diag_mqttmanager.dc = self._dict_mqttsettings

    def _apply_acl(self):
        """Set availability of controls depending on ACL level."""
        allow = helper.cm.xml_mode >= 4

        self.cbx_autostart.setEnabled(allow)
        self.cbx_autoreload.setEnabled(allow)
        self.sbx_autoreloaddelay.setEnabled(allow)
        self.cbx_zeroonexit.setEnabled(allow)
        self.cbx_zeroonerror.setEnabled(allow)
        self.cbb_replace_io.setEnabled(allow)
        self.txt_replace_io.setEnabled(allow and self.cbb_replace_io.currentIndex() == 3)
        self.cbx_plcslave.setEnabled(allow)
        self.cbx_mqtt.setEnabled(allow)
        self.cbx_xmlrpc.setEnabled(allow)

        if allow:
            self.btn_box.setStandardButtons(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
        else:
            self.btn_box.setStandardButtons(
                QtWidgets.QDialogButtonBox.Cancel
            )

    def _changesdone(self):
        """
        Check for unsaved changes in dialog.

        :return: True, if unsaved changes was found
        """
        return (
            int(self.cbx_autostart.isChecked()) != self.dc.get("autostart", 0) or
            int(self.cbx_autoreload.isChecked()) != self.dc.get("autoreload", 1) or
            self.sbx_autoreloaddelay.value() != self.dc.get("autoreloaddelay", 5) or
            int(self.cbx_zeroonexit.isChecked()) != self.dc.get("zeroonexit", 0) or
            int(self.cbx_zeroonerror.isChecked()) != self.dc.get("zeroonerror", 0) or
            self.txt_replace_io.text() != self.dc.get("replace_ios", "") or
            self.cbb_reset_driver_action.currentIndex() != self.dc.get("reset_driver_action", 2) or
            # todo: self.dc.get("rtlevel", 2)

            int(self.cbx_plcslave.isChecked()) != self.dc.get("plcslave", 0) or
            self.acl_plcslave != self.dc.get("plcslaveacl", "") or

            int(self.cbx_mqtt.isChecked()) != self.dc.get("mqtt", 0) or
            self._changesdone_mqtt() or

            int(self.cbx_xmlrpc.isChecked()) != self.dc.get("xmlrpc", 0) or
            self.acl_xmlrpc != self.dc.get("xmlrpcacl", "")
        )

    def _changesdone_mqtt(self):
        """
        Check for unsaved changes in mqtt settings.

        :return: True, if unsaved changes was found
        """
        for key in self._dict_mqttsettings:
            if key in self.dc:
                if self._dict_mqttsettings[key] != self.dc[key]:
                    return True
        return False

    def _load_settings(self):
        """Load values to GUI widgets."""
        pi.logger.debug("RevPiOption._load_settings")

        self.mrk_xml_ask = True

        self.cbx_autostart.setChecked(bool(self.dc.get("autostart", 0)))
        self.cbx_autoreload.setChecked(bool(self.dc.get("autoreload", 1)))
        self.sbx_autoreloaddelay.setValue(self.dc.get("autoreloaddelay", 5))
        self.cbx_zeroonexit.setChecked(bool(self.dc.get("zeroonexit", 0)))
        self.cbx_zeroonerror.setChecked(bool(self.dc.get("zeroonerror", 0)))
        self.txt_replace_io.setText(self.dc.get("replace_ios", ""))
        self.cbb_reset_driver_action.setCurrentIndex(self.dc.get("reset_driver_action", 2))
        self.cbx_plcslave.setChecked(bool(self.dc.get("plcslave", 0)))
        self.acl_plcslave = self.dc.get("plcslaveacl", "")
        self.cbx_mqtt.setChecked(bool(self.dc.get("mqtt", 0)))
        self.cbx_xmlrpc.setChecked(bool(self.dc.get("xmlrpc", 0)))
        self.acl_xmlrpc = self.dc.get("xmlrpcacl", "")

        # Find the right index of combo box
        if self.txt_replace_io.text() == "":
            self.cbb_replace_io.setCurrentIndex(0)
        elif self.txt_replace_io.text() == "/etc/revpipyload/replace_ios.conf":
            self.cbb_replace_io.setCurrentIndex(1)
        elif self.txt_replace_io.text() == "replace_ios.conf":
            self.cbb_replace_io.setCurrentIndex(2)
        else:
            self.cbb_replace_io.setCurrentIndex(3)

        # Update directory with mqtt values to compare with dc values
        for key in self._dict_mqttsettings:
            if key in self.dc:
                self._dict_mqttsettings[key] = self.dc[key]

    def accept(self) -> None:
        if not self._changesdone():
            super(RevPiOption, self).accept()
            return

        ask = QtWidgets.QMessageBox.question(
            self, self.tr("Question"), self.tr(
                "The settings will be set on the Revolution Pi now.\n\n"
                "ACL changes and service settings are applied immediately."
            )
        ) == QtWidgets.QMessageBox.Yes

        if not ask:
            return

        self.dc["autostart"] = int(self.cbx_autostart.isChecked())
        self.dc["autoreload"] = int(self.cbx_autoreload.isChecked())
        self.dc["autoreloaddelay"] = self.sbx_autoreloaddelay.value()
        self.dc["reset_driver_action"] = self.cbb_reset_driver_action.currentIndex()
        self.dc["zeroonexit"] = int(self.cbx_zeroonexit.isChecked())
        self.dc["zeroonerror"] = int(self.cbx_zeroonerror.isChecked())
        self.dc["replace_ios"] = self.txt_replace_io.text()

        # PLCSlave Settings
        self.dc["plcslave"] = int(self.cbx_plcslave.isChecked())
        self.dc["plcslaveacl"] = self.acl_plcslave

        # MQTT Settings
        self.dc["mqtt"] = int(self.cbx_mqtt.isChecked())
        self.dc["mqttbasetopic"] = self._dict_mqttsettings["mqttbasetopic"]
        self.dc["mqttsendinterval"] = int(self._dict_mqttsettings["mqttsendinterval"])
        self.dc["mqttsend_on_event"] = int(self._dict_mqttsettings["mqttsend_on_event"])
        self.dc["mqttwrite_outputs"] = int(self._dict_mqttsettings["mqttwrite_outputs"])
        self.dc["mqttbroker_address"] = self._dict_mqttsettings["mqttbroker_address"]
        self.dc["mqttport"] = int(self._dict_mqttsettings["mqttport"])
        self.dc["mqtttls_set"] = int(self._dict_mqttsettings["mqtttls_set"])
        self.dc["mqttusername"] = self._dict_mqttsettings["mqttusername"]
        self.dc["mqttpassword"] = self._dict_mqttsettings["mqttpassword"]
        self.dc["mqttclient_id"] = self._dict_mqttsettings["mqttclient_id"]

        # XML Settings
        self.dc["xmlrpc"] = int(self.cbx_xmlrpc.isChecked())
        self.dc["xmlrpcacl"] = self.acl_xmlrpc

        saved = helper.cm.call_remote_function(
            "set_config", self.dc, ask,
            default_value=False
        )

        if saved:
            super(RevPiOption, self).accept()
        else:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The settings could not be saved on the Revolution Pi!\n"
                    "Try to save the values one mor time and check the log "
                    "files of RevPiPyLoad if the error rises again."
                )
            )

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
        # Reset class values
        if not helper.cm.connected:
            return QtWidgets.QDialog.Rejected

        self.dc = helper.cm.call_remote_function("get_config", default_value={})
        if len(self.dc) == 0:
            return QtWidgets.QDialog.Rejected

        self._load_settings()
        self._apply_acl()

        running = helper.cm.call_remote_function("plcslaverunning", default_value=False)
        self.lbl_slave_status.setText(
            self.tr("running") if running else self.tr("stopped")
        )
        self.lbl_slave_status.setStyleSheet(
            "color: green" if running else "color: red"
        )

        running = helper.cm.call_remote_function("mqttrunning")
        if running is None:
            # On older versions of RevPiPyLoad MQTT is not implemented
            self.cbx_mqtt.setToolTip(self.tr(
                "The MQTT service is not available on your RevPiPyLoad version."
            ))
            self.btn_mqtt.setVisible(False)
            self.lbl_mqtt_status.setText("N/A")
            self.lbl_mqtt_status.setStyleSheet("")
        else:
            self.cbx_mqtt.setToolTip("")
            self.btn_mqtt.setVisible(True)
            self.lbl_mqtt_status.setText(
                self.tr("running") if running else self.tr("stopped")
            )
            self.lbl_mqtt_status.setStyleSheet(
                "color: green" if running else "color: red"
            )

        return super(RevPiOption, self).exec()

    def reject(self) -> None:
        """Reject all sub windows and reload settings."""
        self._load_settings()
        super(RevPiOption, self).reject()

    @QtCore.pyqtSlot(int)
    def on_cbb_replace_io_currentIndexChanged(self, index: int):
        """Update replace_io path in text field to compare values."""
        if index == 0:
            self.txt_replace_io.setText("")
        elif index == 1:
            self.txt_replace_io.setText("/etc/revpipyload/replace_ios.conf")
        elif index == 2:
            self.txt_replace_io.setText("replace_ios.conf")
        else:
            self.txt_replace_io.setText(self.dc.get("replace_ios", ""))

        self.txt_replace_io.setEnabled(index == 3)

    @QtCore.pyqtSlot()
    def on_btn_aclplcslave_clicked(self):
        """Start ACL manager to edit ACL entries."""
        self.diag_aclmanager.setup_acl_manager(self.acl_plcslave, {
            0: self.tr("read only"),
            1: self.tr("read and write"),
        })
        self.diag_aclmanager.read_only = helper.cm.xml_mode < 4
        if self.diag_aclmanager.exec() == QtWidgets.QDialog.Accepted:
            self.acl_plcslave = self.diag_aclmanager.get_acl()

    @QtCore.pyqtSlot()
    def on_btn_mqtt_clicked(self):
        """Open MQTT settings."""
        if not helper.cm.connected:
            return

        self.diag_mqttmanager.read_only = helper.cm.xml_mode < 4
        self.diag_mqttmanager.exec()

    @QtCore.pyqtSlot(int)
    def on_cbx_xmlrpc_stateChanged(self, state: int):
        if state == QtCore.Qt.Unchecked and self.mrk_xml_ask:
            self.mrk_xml_ask = QtWidgets.QMessageBox.question(
                self, self.tr("Question"), self.tr(
                    "Are you sure you want to deactivate the XML-RPC server? "
                    "You will NOT be able to access the Revolution Pi with "
                    "this program after saving the options!"
                )
            ) == QtWidgets.QMessageBox.No
            if self.mrk_xml_ask:
                self.cbx_xmlrpc.setCheckState(QtCore.Qt.Checked)

    @QtCore.pyqtSlot()
    def on_btn_aclxmlrpc_clicked(self):
        self.diag_aclmanager.setup_acl_manager(self.acl_xmlrpc, {
            0: self.tr("Start/Stop PLC program and read logs"),
            1: self.tr("+ read IOs in watch mode"),
            2: self.tr("+ read properties and download PLC program"),
            3: self.tr("+ upload PLC program"),
            4: self.tr("+ set properties")
        })
        self.diag_aclmanager.read_only = helper.cm.xml_mode < 4
        if self.diag_aclmanager.exec() == QtWidgets.QDialog.Accepted:
            self.acl_xmlrpc = self.diag_aclmanager.get_acl()
