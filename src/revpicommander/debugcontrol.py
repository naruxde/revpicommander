# -*- coding: utf-8 -*-
"""Debug control widget to append to main window."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

import pickle
from xmlrpc.client import Binary, Fault, MultiCall, MultiCallIterator

from PyQt5 import QtCore, QtGui, QtWidgets

from . import helper
from . import proginit as pi
from .debugios import DebugIos
from .ui.debugcontrol_ui import Ui_wid_debugcontrol


class PsValues(QtCore.QThread):
    """
    Get process image from Revolution Pi.

    If this thread detects a driver reset, it will finish the work.
    """

    driver_reset_detected = QtCore.pyqtSignal()
    process_image_received = QtCore.pyqtSignal(Binary)

    def __init__(self):
        super().__init__()
        self._cycle_time = 200

    def run(self):
        """Read IO values of Revolution Pi."""
        pi.logger.debug("PsValues.run enter")

        while not self.isInterruptionRequested():
            try:
                self.process_image_received.emit(
                    helper.cm.call_remote_function("ps_values", raise_exception=True)
                )
            except Fault:
                pi.logger.warning("Detected piCtory reset.")
                self.requestInterruption()
                self.driver_reset_detected.emit()
            except Exception as e:
                pi.logger.error(e)
                self.process_image_received.emit(Binary())

            self.msleep(self._cycle_time)

        pi.logger.debug("PsValues.run exit")


class DebugControl(QtWidgets.QWidget, Ui_wid_debugcontrol):
    """Debug controller for main window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.dict_devices = {}
        """Key=position, value=device name."""
        self.dict_ios = {"inp": {}, "out": {}}
        """IO types "inp" "out" which include key=device position, value=list with ios."""
        self.dict_windows = {}
        """Debug IO windows with key=device position, value=DebugIos."""

        self.driver_reset_detected = False
        self.err_workvalues = 0
        self.max_errors = 10
        self.th_worker = PsValues()

        self.vl_devices.addItem(
            QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        )
        self.cbx_write.setEnabled(False)
        self.cbx_stay_on_top.setChecked(helper.settings.value("debugcontrol/stay_on_top", False, bool))

        self.shc_read_io = QtWidgets.QShortcut(QtGui.QKeySequence("F4"), self)
        self.shc_read_io.setContext(QtCore.Qt.ApplicationShortcut)
        self.shc_read_io.activated.connect(self.on_btn_read_io_pressed)
        self.shc_refresh_io = QtWidgets.QShortcut(QtGui.QKeySequence("F5"), self)
        self.shc_refresh_io.setContext(QtCore.Qt.ApplicationShortcut)
        self.shc_refresh_io.activated.connect(self.on_btn_refresh_io_pressed)
        self.shc_write_o = QtWidgets.QShortcut(QtGui.QKeySequence("F6"), self)
        self.shc_write_o.setContext(QtCore.Qt.ApplicationShortcut)
        self.shc_write_o.activated.connect(self.on_btn_write_o_clicked)

    def __del__(self):
        pi.logger.debug("DebugControl.__del__")

    def _set_gui_control_states(self):
        """Set states depending on acl level."""
        pi.logger.debug("DebugControl._set_gui_control_states")
        # xml_mode view >= 1
        # xml_mode write >= 3
        self.btn_read_io.setEnabled(not self.cbx_write.isChecked())
        self.btn_refresh_io.setEnabled(not self.cbx_refresh.isChecked())
        self.btn_write_o.setEnabled(
            not self.cbx_write.isChecked() and (helper.cm.xml_mode >= 3 or helper.cm.simulating)
        )
        self.cbx_write.setEnabled(
            self.cbx_refresh.isChecked() and (helper.cm.xml_mode >= 3 or helper.cm.simulating)
        )

    def _destroy_io_view(self, device_position=-1):
        """
        Destroy IO view including the button and dict entry.

        :param device_position: Only device position or -1 for all
        """
        pi.logger.debug("DebugControl._destroy_io_view")
        for position in sorted(self.dict_devices) if device_position == -1 else [device_position]:
            if position in self.dict_windows:
                # Remove singe window and button
                win = self.dict_windows[position]  # type: DebugIos
                win.close()
                win.deleteLater()
                win.disconnect()
                del self.dict_windows[position]

            btn = self.gb_devices.findChild((QtWidgets.QPushButton,), str(position))  # type: QtWidgets.QPushButton
            if btn:
                self.vl_devices.removeWidget(btn)
                btn.deleteLater()
                btn.disconnect()

    def _driver_reset_detected(self):
        """Things to do after driver reset."""
        self.driver_reset_detected = True
        self.cbx_write.setChecked(False)
        self.cbx_refresh.setChecked(False)
        for win in self.dict_windows.values():  # type: DebugIos
            win.stat_bar.showMessage(
                self.tr("Driver reset for piControl detected."),
                10000
            )
        self.reload_devices()

    def _work_values(self, refresh=False, write_out=False, process_image=None):
        """
        Read input and output values.

        :param refresh: Refresh unchanged ios from process image
        :param write_out: Write changed outputs to process image
        :param process_image: Use this <class 'Binary'> for work and do not fetch
        """
        if process_image is not None:
            ba_values = process_image
        else:
            try:
                ba_values = helper.cm.call_remote_function("ps_values", raise_exception=True)
            except Fault:
                pi.logger.warning("Detected piCtory reset.")
                self._driver_reset_detected()
                return
            except Exception as e:
                pi.logger.error(e)
                ba_values = Binary()

        # From now on use bytes instead of Binary
        ba_values = bytearray(ba_values.data)

        if not ba_values:
            if self.cbx_refresh.isChecked():
                self.err_workvalues += 1
            else:
                # Raise error on button press
                self.err_workvalues = self.max_errors

            if self.err_workvalues >= self.max_errors:
                for win in self.dict_windows.values():  # type: DebugIos
                    win.stat_bar.setStyleSheet("background-color: red;")
                    win.stat_bar.showMessage(self.tr(
                        "Error while getting values from Revolution Pi."
                    ), 5000)

            return

        if self.err_workvalues > 0:
            self.err_workvalues = 0
            for win in self.dict_windows.values():  # type: DebugIos
                win.stat_bar.setStyleSheet("")

        # Use multicall to set all changed values
        if write_out and helper.cm.connected:
            cli = helper.cm.get_cli()
            xmlmc = MultiCall(cli)
        else:
            xmlmc = []

        for io_type in self.dict_ios:
            for position in self.dict_ios[io_type]:
                if position not in self.dict_windows:
                    continue

                win = self.dict_windows[position]
                for io in self.dict_ios[io_type][position]:  # type: list
                    # ['name', bytelen, byte_address, 'bmk', bitaddress, 'byteorder', signed]
                    # + wordorder since revpipyload 0.9.9
                    value_procimg = bytes(ba_values[io[2]:io[2] + io[1]])
                    if io[4] >= 0:
                        # Bit-IO
                        value_procimg = bool(
                            int.from_bytes(value_procimg, byteorder=io[5], signed=io[6]) & 1 << io[4]
                        )

                    if (refresh or write_out) and io_type == "out":
                        widget_value, last_value = win.get_value(io[0])
                        if widget_value != last_value:
                            # User changed value

                            if not write_out:
                                # Do not write output after change to save this state
                                continue

                            value_procimg = widget_value
                            if type(xmlmc) == MultiCall:
                                xmlmc.ps_setvalue(position, io[0], widget_value)
                            else:
                                # Simulate multicall an collect result to list
                                xmlmc.append(
                                    helper.cm.call_remote_function("ps_setvalue", position, io[0], widget_value)
                                )

                    win.set_value(io[0], value_procimg)

                if self.cbx_refresh.isChecked():
                    win.stat_bar.showMessage(self.tr("Auto update values..."), 1000)
                else:
                    win.stat_bar.showMessage(self.tr("Values updated..."), 2000)

                if self.driver_reset_detected:
                    # Show values, which we can recover to empty process image
                    win.reset_change_value_colors()

        self.driver_reset_detected = False

        # Set values by multi call
        if write_out:
            if isinstance(xmlmc, list):
                self._validate_multicall(xmlmc)
            else:
                self._validate_multicall(xmlmc())

    def _validate_multicall(self, return_list):
        """
        Check xml rpc multi call return values.

        :param return_list: Return values of multi call
        """
        if isinstance(return_list, MultiCallIterator):
            return_list = return_list.results
            if len(return_list) == 0:
                return
        elif not isinstance(return_list, list):
            return
        pi.logger.debug("DebugControl._validate_multicall")

        str_errmsg = ""
        for lst_result in return_list:  # type: list
            # [[device, io, status, msg]] - Yes, double list list :D
            if type(lst_result[0]) == list:
                lst_result = lst_result.pop()
            if not lst_result[2]:
                # Create error message
                device_name = self.dict_devices[lst_result[0]]
                str_errmsg += self.tr(
                    "Error set value of device '{0}' Output '{1}': {2}\n"
                ).format(device_name, lst_result[1], lst_result[3])
            else:
                self.dict_windows[lst_result[0]].reset_change_value_colors(lst_result[1])

        if str_errmsg != "":
            pi.logger.error(str_errmsg)
            if not self.cbx_refresh.isChecked():
                QtWidgets.QMessageBox.critical(self, self.tr("Error"), str_errmsg)

    def deleteLater(self):
        """Clean up all sub windows."""
        pi.logger.debug("DebugControl.deleteLater")

        self.cbx_write.setChecked(False)
        self.cbx_refresh.setChecked(False)
        self._destroy_io_view()

        super().deleteLater()

    def reload_devices(self):
        """Rebuild GUI depending on devices and ios of Revolution Pi."""
        pi.logger.debug("DebugControl.reload_devices")

        if not helper.cm.call_remote_function("psstart", default_value=False):
            # RevPiPyLoad does not support psstart (too old)
            return False

        # ps_devices format: [[0, 'picore01'], [32, 'di01'], ...
        dict_devices = {v[0]: v[1] for v in helper.cm.call_remote_function("ps_devices", default_value=[])}
        if len(dict_devices) == 0:
            # There is no piCtory configuration on the Revolution Pi
            return False

        # Remove not existing or renamed devices
        for position in self.dict_devices:
            if position not in dict_devices or self.dict_devices[position] != dict_devices[position]:
                self._destroy_io_view(position)

        self.dict_devices = dict_devices

        # Format: {position: [['name', bitlength, byte_address, 'bmk', bitaddress, 'byteorder', signed], ...
        inps_data = helper.cm.call_remote_function("ps_inps", default_value=Binary()).data
        outs_data = helper.cm.call_remote_function("ps_outs", default_value=Binary()).data
        if inps_data == b'' or outs_data == b'':
            return False

        dict_inps = pickle.loads(inps_data)
        dict_outs = pickle.loads(outs_data)

        # Take spacer at last position and reinsert it after buttons
        spacer = self.vl_devices.takeAt(self.vl_devices.count() - 1)

        for position in sorted(self.dict_devices):
            if position in self.dict_windows:
                # DebugIos already exists
                if self.dict_windows[position].update_ios(dict_inps[position], dict_outs[position]):
                    # All IOs match the old ones
                    continue
                else:
                    # Destroy old window to build a new one
                    self._destroy_io_view(position)

            win = DebugIos(
                position, self.dict_devices[position],
                dict_inps[position], dict_outs[position]
            )
            win.device_closed.connect(self.on_device_closed)
            self.dict_windows[position] = win

            btn = QtWidgets.QPushButton(self.gb_devices)
            btn.setCheckable(True)
            btn.setObjectName(str(position))
            btn.setText("{0} | {1}".format(position, self.dict_devices[position]))
            btn.clicked.connect(self.on_btn_device_clicked)
            self.vl_devices.addWidget(btn)

        self.vl_devices.addItem(spacer)

        self.dict_ios["inp"] = dict_inps
        self.dict_ios["out"] = dict_outs

        self._work_values(refresh=True)
        self._set_gui_control_states()

        self.cbx_refresh.setChecked(helper.settings.value("debugcontrol/auto_refresh", False, bool))

        return True

    @QtCore.pyqtSlot(bool)
    def on_btn_device_clicked(self, checked: bool):
        """Open or close IO window."""
        pi.logger.debug("DebugControl.on_btn_device_clicked")

        position = int(self.sender().objectName())
        if position in self.dict_windows:
            win = self.dict_windows[position]  # type: QtWidgets.QMainWindow
            win.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, self.cbx_stay_on_top.isChecked())
            win.setVisible(checked)

    @QtCore.pyqtSlot(int)
    def on_device_closed(self, position: int):
        """Change the check state of button, if window was closed."""
        pi.logger.debug("DebugControl.on_device_closed")
        btn = self.gb_devices.findChild(QtWidgets.QPushButton, str(position))  # type: QtWidgets.QPushButton
        btn.setChecked(False)

    @QtCore.pyqtSlot()
    def on_btn_read_io_pressed(self):
        """Read all IO values and replace changed ones."""
        pi.logger.debug("DebugControl.on_btn_read_io_pressed")
        for win in self.dict_windows.values():  # type: DebugIos
            win.reset_label_colors()
        self._work_values()

    @QtCore.pyqtSlot()
    def on_btn_refresh_io_pressed(self):
        """Read all IO values but do not touch changed ones."""
        pi.logger.debug("DebugControl.on_btn_refresh_io_pressed")
        if not self.cbx_refresh.isChecked():
            self._work_values(refresh=True)

    @QtCore.pyqtSlot()
    def on_btn_write_o_clicked(self):
        """Write outputs."""
        pi.logger.debug("DebugControl.on_btn_write_o_clicked")
        if not self.cbx_write.isChecked() and (helper.cm.xml_mode >= 3 or helper.cm.simulating):
            for win in self.dict_windows.values():  # type: DebugIos
                win.reset_label_colors()
            self._work_values(write_out=True)

    @QtCore.pyqtSlot(int)
    def on_cbx_refresh_stateChanged(self, state: int):
        """Start or stop the auto refresh thread."""
        pi.logger.debug("DebugControl.cbx_refresh_stateChanged")

        # Start / stop worker thread
        if state == QtCore.Qt.Checked and (helper.cm.connected or helper.cm.simulating):
            self.th_worker = PsValues()
            self.th_worker.driver_reset_detected.connect(self._driver_reset_detected)
            self.th_worker.process_image_received.connect(lambda process_image: self._work_values(
                refresh=True,
                write_out=self.cbx_write.isChecked(),
                process_image=process_image
            ))
            self.th_worker.start()

        else:
            self.th_worker.requestInterruption()
            self.th_worker.wait()
            self.th_worker.deleteLater()
            self.cbx_write.setChecked(False)

        self._set_gui_control_states()

    @QtCore.pyqtSlot(bool)
    def on_cbx_refresh_clicked(self, state: bool):
        """Save the state on user action."""
        helper.settings.setValue("debugcontrol/auto_refresh", state)

    @QtCore.pyqtSlot(bool)
    def on_cbx_stay_on_top_clicked(self, state: bool):
        """Save the state on user action."""
        helper.settings.setValue("debugcontrol/stay_on_top", state)

    @QtCore.pyqtSlot(int)
    def on_cbx_write_stateChanged(self, state: int):
        pi.logger.debug("DebugControl.cbx_write_stateChanged")
        checked = state == QtCore.Qt.Checked
        for win in self.dict_windows.values():  # type: DebugIos
            win.write_values = checked

        self._set_gui_control_states()
