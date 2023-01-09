#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""RevPiCommander main program."""

__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "GPLv3"
__version__ = "0.9.10rc2"

import webbrowser
from os.path import dirname, join

from PyQt5 import QtCore, QtGui, QtWidgets

from . import helper
from . import proginit as pi
from . import revpilogfile
from .avahisearch import AvahiSearch
from .debugcontrol import DebugControl
from .helper import RevPiSettings
from .revpifiles import RevPiFiles
from .revpiinfo import RevPiInfo
from .revpioption import RevPiOption
from .revpiplclist import RevPiPlcList
from .revpiprogram import RevPiProgram
from .simulator import Simulator
from .ui.revpicommander_ui import Ui_win_revpicommander


class RevPiCommander(QtWidgets.QMainWindow, Ui_win_revpicommander):
    """Main application of RevPiCommander."""

    def __init__(self, parent=None):
        """Init main program."""
        super(RevPiCommander, self).__init__(parent)
        self.setupUi(self)

        self.wid_debugcontrol = None  # type: DebugControl
        """Holds the widget of DebugControl."""
        self.simulating = False
        """True, if simulation is running."""
        self.dict_men_connections_subfolder = {}
        """Submenus for folder entries."""

        self._set_gui_control_states()
        self._load_men_connections()

        # Load sub windows
        self.diag_connections = RevPiPlcList(self)
        self.diag_search = AvahiSearch(self)
        self.diag_info = RevPiInfo(__version__, self)
        self.diag_options = RevPiOption(self)
        self.diag_program = RevPiProgram(self)
        self.win_files = RevPiFiles(self)
        self.win_log = revpilogfile.RevPiLogfile(self)

        self.btn_plc_logs.clicked.connect(self.on_act_logs_triggered)

        helper.cm.connection_disconnected.connect(self.on_cm_connection_disconnected)
        helper.cm.connection_disconnecting.connect(self.on_cm_connection_disconnecting)
        helper.cm.connection_established.connect(self.on_cm_connection_established)
        helper.cm.connection_error_observed.connect(self.on_cm_connection_error_observed)
        helper.cm.status_changed.connect(self.on_cm_status_changed)

        self.restoreGeometry(helper.settings.value("revpicommander/geo", b''))

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pi.logger.debug("RevPiCommander.closeEvent")
        helper.cm.pyload_disconnect()
        helper.settings.setValue("revpicommander/geo", self.saveGeometry())

    def _set_gui_control_states(self):
        """Setup states of actions and buttons."""
        if helper.cm.simulating:
            self.btn_plc_stop.setEnabled(True)  # Stop simulator
            self.btn_plc_restart.setEnabled(True)  # Reset simulator values
            self.btn_plc_debug.setEnabled(True)

        else:
            connected = helper.cm.connected
            self.men_plc.setEnabled(connected)
            self.act_logs.setEnabled(connected)
            self.act_options.setEnabled(connected and helper.cm.xml_mode >= 2)
            self.act_program.setEnabled(connected and helper.cm.xml_mode >= 2)
            self.act_developer.setEnabled(connected and helper.cm.xml_mode >= 3)
            self.act_pictory.setEnabled(connected)
            self.act_reset.setEnabled(connected and helper.cm.xml_mode >= 3)
            self.act_disconnect.setEnabled(connected)
            self.btn_plc_start.setEnabled(connected)
            self.btn_plc_stop.setEnabled(connected)
            self.btn_plc_restart.setEnabled(connected)
            self.btn_plc_logs.setEnabled(connected)
            self.btn_plc_debug.setEnabled(connected and helper.cm.xml_mode >= 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Connection management

    @QtCore.pyqtSlot(str)
    def on_cm_connection_error_observed(self, message: str):
        """
        Connection error occurred in connection manager.

        :param message: Error message
        """
        self.statusbar.showMessage(message, 15000)

    @QtCore.pyqtSlot()
    def on_cm_connection_disconnected(self):
        """Connection of connection manager was disconnected."""
        pi.logger.debug("RevPiCommander.on_cm_connection_disconnected")

        self._set_gui_control_states()
        self.txt_host.setVisible(True)
        self.txt_host.clear()
        self.txt_connection.clear()

    @QtCore.pyqtSlot()
    def on_cm_connection_disconnecting(self):
        """Connection of connection manager will now disconnect."""
        pi.logger.debug("RevPiCommander.on_cm_connection_disconnecting")

        # This will remove the widgets in the button functions
        self.btn_plc_debug.setChecked(False)

        self.diag_info.reject()
        self.diag_options.reject()
        self.diag_program.reject()
        self.win_files.close()
        self.win_files.deleteLater()

        self.centralwidget.adjustSize()
        self.adjustSize()

    @QtCore.pyqtSlot()
    def on_cm_connection_established(self):
        """Connection manager established a new connection and loaded values."""
        pi.logger.debug("RevPiCommander.on_cm_connection_established")

        self._set_gui_control_states()
        if helper.cm.simulating:
            self.txt_host.setVisible(False)
            self.txt_connection.setText("configrsc=\"{0}\", procimg=\"{1}\"".format(
                helper.cm.simulating_configrsc,
                helper.cm.simulating_procimg,
            ))
        else:
            self.txt_host.setText(helper.cm.settings.name)
            self.txt_connection.setText(helper.cm.settings.address)
        self.win_files = RevPiFiles(self)

    @QtCore.pyqtSlot(str, str)
    def on_cm_status_changed(self, text: str, color: str):
        """PLC program status from Revolution Pi."""
        self.txt_status.setText(text)
        self.txt_status.setStyleSheet("background: {0}".format(color))

    # endregion # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Menu entries

    def _load_men_connections(self):
        """Build up connections menu."""

        self.men_connections.clear()
        self.dict_men_connections_subfolder.clear()

        for settings in helper.all_revpi_settings():  # type: RevPiSettings
            if settings.folder:
                if settings.folder not in self.dict_men_connections_subfolder:
                    men_sub = QtWidgets.QMenu(self.men_connections)
                    men_sub.setTitle(settings.folder)
                    self.dict_men_connections_subfolder[settings.folder] = men_sub
                    self.men_connections.addMenu(men_sub)
                parent_menu = self.dict_men_connections_subfolder[settings.folder]
            else:
                parent_menu = self.men_connections

            display_name = settings.name
            if settings.ssh_use_tunnel:
                display_name += " (SSH)"

            act = QtWidgets.QAction(parent_menu)
            act.setText(display_name)
            act.setData(settings)
            act.setToolTip("{0}:{1}".format(settings.address, settings.port))
            parent_menu.addAction(act)

    @QtCore.pyqtSlot()
    def on_act_connections_triggered(self):
        """Edit saved connections to Revolution Pi devices."""
        if self.diag_connections.exec() == QtWidgets.QDialog.Accepted:
            self._load_men_connections()

    @QtCore.pyqtSlot()
    def on_act_search_triggered(self):
        """Search for Revolution Pi with zero conf."""
        if self.diag_search.exec() == QtWidgets.QDialog.Accepted:
            if self.diag_search.connect_settings:
                if self.diag_search.just_save:
                    self.diag_connections.exec_with_presets(self.diag_search.connect_settings)
                else:
                    helper.cm.pyload_connect(self.diag_search.connect_settings, self)

        self._load_men_connections()

    @QtCore.pyqtSlot()
    def on_act_simulator_triggered(self):
        """Start the simulator function."""
        diag = Simulator(self)
        if diag.exec() != QtWidgets.QDialog.Accepted:
            diag.deleteLater()
            return

        helper.cm.pyload_disconnect()
        configrsc_file = helper.settings.value("simulator/configrsc", "", str)
        procimg_file = helper.settings.value("simulator/procimg", "", str)

        if helper.cm.pyload_simulate(configrsc_file, procimg_file, diag.cbx_stop_remove.isChecked()):
            QtWidgets.QMessageBox.information(
                self, self.tr("Simulator started..."), self.tr(
                    "The simulator is running!\n\nYou can work with this simulator if your call "
                    "RevPiModIO with this additional parameters:\nprocimg={0}\nconfigrsc={1}\n\n"
                    "You can copy that from header textbox."
                ).format(procimg_file, configrsc_file)
            )
        else:
            pi.logger.error("Can not start simulator")
            QtWidgets.QMessageBox.critical(
                self, self.tr("Can not start..."), self.tr(
                    "Can not start the simulator! Maybe the piCtory file is corrupt "
                    "or you have no write permissions for '{0}'."
                ).format(procimg_file)
            )

        diag.deleteLater()

    @QtCore.pyqtSlot()
    def on_act_logs_triggered(self):
        """Show log window."""
        if not helper.cm.connected:
            return

        if "load_plclog" not in helper.cm.xml_funcs:
            QtWidgets.QMessageBox.warning(
                self, self.tr("Warning"), self.tr(
                    "This version of Logviewer ist not supported in version {0} "
                    "of RevPiPyLoad on your RevPi! You need at least version 0.4.1."
                ).format(helper.cm.call_remote_function("version", default_value="-"))
            )
            return None

        if self.win_log.isHidden():
            self.win_log.show()
        else:
            self.win_log.activateWindow()

    @QtCore.pyqtSlot()
    def on_act_options_triggered(self):
        """Show option dialog."""
        if not helper.cm.connected:
            return

        if helper.cm.xml_mode < 2:
            QtWidgets.QMessageBox.warning(
                self, self.tr("Warning"), self.tr(
                    "XML-RPC access mode in the RevPiPyLoad "
                    "configuration is too small to access this dialog!"
                )
            )
            return

        # Check version of RevPiPyLoad, must be greater than 0.5!
        if helper.cm.pyload_version < (0, 6, 0):
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The Version of RevPiPyLoad on your Revolution Pi ({0}) is to old. "
                    "This Version of RevPiCommander require at least version 0.6.0 "
                    "of RevPiPyLoad. Please update your Revolution Pi!"
                )
            )
            return

        rc = self.diag_options.exec()
        if rc == QtWidgets.QDialog.Accepted:
            helper.cm.refresh_xml_mode()

    @QtCore.pyqtSlot()
    def on_act_program_triggered(self):
        """Show program dialog."""
        if not helper.cm.connected:
            return

        if helper.cm.xml_mode < 2:
            QtWidgets.QMessageBox.warning(
                self, self.tr("Warning"), self.tr(
                    "XML-RPC access mode in the RevPiPyLoad "
                    "configuration is too small to access this dialog!"
                )
            )
            return

        self.diag_program.exec()

    @QtCore.pyqtSlot()
    def on_act_developer_triggered(self):
        """Extent developer mode to main window."""
        if not helper.cm.connected:
            return

        if self.win_files.isHidden():
            self.win_files.show()
        else:
            self.win_files.activateWindow()

    @QtCore.pyqtSlot()
    def on_act_pictory_triggered(self):
        """Open piCtory in default browser of operating system."""
        if helper.cm.address:
            webbrowser.open("http://{0}/".format(helper.cm.address))

    @QtCore.pyqtSlot()
    def on_act_reset_triggered(self):
        """Reset piControl driver on revolution pi."""
        if not (helper.cm.connected and helper.cm.xml_mode >= 3):
            return

        ask = QtWidgets.QMessageBox.question(
            self, self.tr("Question"), self.tr(
                "Are you sure to reset piControl?\n"
                "The pictory configuration will be reloaded. During that time "
                "the process image will be interrupted and could rise errors "
                "on running control programs!"
            )
        )
        if ask != QtWidgets.QMessageBox.Yes:
            return

        ec = helper.cm.call_remote_function("resetpicontrol", default_value=-1)
        if ec == 0:
            QtWidgets.QMessageBox.information(
                self, self.tr("Success"), self.tr(
                    "piControl reset executed successfully"
                )
            )

        else:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "piControl reset could not be executed successfully"
                )
            )

    @QtCore.pyqtSlot()
    def on_act_disconnect_triggered(self):
        """Close actual connection."""
        helper.cm.pyload_disconnect()

    @QtCore.pyqtSlot(QtWidgets.QAction)
    def on_men_connections_triggered(self, action: QtWidgets.QAction):
        """A connection is selected in the men_connections menu."""
        helper.cm.pyload_connect(action.data(), self)

    @QtCore.pyqtSlot()
    def on_act_webpage_triggered(self):
        """Open project page in default browser of operating system."""
        webbrowser.open("https://revpimodio.org")

    @QtCore.pyqtSlot()
    def on_act_info_triggered(self):
        """Open info window of application."""
        self.diag_info.exec()

    # endregion # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Button events

    @QtCore.pyqtSlot()
    def on_btn_plc_start_clicked(self):
        """Start plc program on revolution pi."""
        helper.cm.call_remote_function("plcstart")

    @QtCore.pyqtSlot()
    def on_btn_plc_stop_clicked(self):
        """Start plc program on revolution pi."""
        if helper.cm.simulating:
            helper.cm.pyload_disconnect()
        else:
            helper.cm.call_remote_function("plcstop")

    @QtCore.pyqtSlot()
    def on_btn_plc_restart_clicked(self):
        """Restart plc program on revolution pi."""
        if helper.cm.simulating:
            rc = QtWidgets.QMessageBox.question(
                self, self.tr("Reset to piCtory defaults..."), self.tr(
                    "Do you want to reset your process image to {0} values?\n"
                    "You have to stop other RevPiModIO programs before doing that, "
                    "because they could reset the outputs."
                ).format(
                    self.tr("zero") if helper.settings.value("simulator/restart_zero", False, bool)
                    else self.tr("piCtory default"))
            ) == QtWidgets.QMessageBox.Yes
            if rc:
                # Set piCtory default values in process image
                helper.cm.reset_simulator()
        else:
            helper.cm.call_remote_function("plcstop")
            helper.cm.call_remote_function("plcstart")

    @QtCore.pyqtSlot(bool)
    def on_btn_plc_debug_toggled(self, state: bool):
        """Start plc watch mode."""
        if not (state or self.wid_debugcontrol is None):
            # Remove widget
            self.gl.removeWidget(self.wid_debugcontrol)
            self.wid_debugcontrol.deleteLater()
            self.wid_debugcontrol = None

        elif "psstart" not in helper.cm.xml_funcs:
            QtWidgets.QMessageBox.warning(
                self, self.tr("Warning"), self.tr(
                    "The watch mode ist not supported in version {0} "
                    "of RevPiPyLoad on your RevPi! You need at least version "
                    "0.5.3! Maybe the python3-revpimodio2 module is not "
                    "installed on your RevPi at least version 2.0.0."
                ).format(helper.cm.call_remote_function("version", "-"))
            )
            self.btn_plc_debug.setChecked(False)
            self.btn_plc_debug.setEnabled(False)

        elif helper.cm.xml_mode < 1 and not helper.cm.simulating:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not load this function, because your ACL level is to low!\n"
                    "You need at least level 1 to read or level 3 to write."
                )
            )
            self.btn_plc_debug.setChecked(False)

        elif helper.cm.connected or helper.cm.simulating:
            debugcontrol = DebugControl(self.centralwidget)
            if debugcontrol.reload_devices():
                self.wid_debugcontrol = debugcontrol
                self.gl.addWidget(self.wid_debugcontrol)
            else:
                debugcontrol.deleteLater()
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error"), self.tr(
                        "Can not load piCtory configuration. \n"
                        "Did you create a hardware configuration? "
                        "Please check this in piCtory!"
                    )
                )
                self.btn_plc_debug.setChecked(False)

        self.centralwidget.adjustSize()
        self.adjustSize()

    # endregion # # # # #


def main() -> int:
    from sys import argv

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(argv)

    try:
        # Setup translation from file with system language
        translator = QtCore.QTranslator()
        translator.load(
            QtCore.QLocale.system(),
            "revpicommander", "_", join(dirname(__file__), "locale"), ".qm"
        )
        app.installTranslator(translator)
    except Exception:
        pass

    # Prepare workers
    helper.cm.start()

    win = RevPiCommander()
    win.show()
    exit_code = app.exec()

    # Clean up workers
    helper.cm.requestInterruption()
    helper.cm.wait()

    return exit_code


if __name__ == "__main__":
    import sys

    sys.exit(main())
