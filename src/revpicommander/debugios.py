# -*- coding: utf-8 -*-
"""One device of the Revolution Pi."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

import struct

from PyQt5 import QtCore, QtGui, QtWidgets

from . import helper
from . import proginit as pi
from .ui.debugios_ui import Ui_win_debugios


class DebugIos(QtWidgets.QMainWindow, Ui_win_debugios):
    """IO window of one device."""

    device_closed = QtCore.pyqtSignal(int)
    """This window was closed."""

    search_class = (QtWidgets.QLineEdit, QtWidgets.QDoubleSpinBox, QtWidgets.QCheckBox)

    def __init__(self, position: int, name: str, inputs: list, outputs: list, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.restoreGeometry(helper.cm.settings.debug_geos.get(position, b''))
        self.setWindowTitle("{0} - {1}".format(position, name))
        self.gb_io.setTitle(self.gb_io.title().format(name))

        self.__qwa = {}
        """Quick widget access."""

        self.position = position
        self.name = name
        self.inputs = inputs.copy()
        self.outputs = outputs.copy()
        self.write_values = False

        self.length = self._calc_device_length(self.inputs, self.outputs)

        self.style_sheet = ""
        self._create_io(self.inputs, self.saw_inp, True)
        self._create_io(self.outputs, self.saw_out, False)
        self.style_sheet = "background-color: red;"

    def __del__(self):
        pi.logger.debug("DebugIos.__del__")

    def closeEvent(self, a0: QtGui.QCloseEvent):
        pi.logger.debug("DebugIos.closeEvent")
        helper.cm.settings.debug_geos[self.position] = self.saveGeometry()
        self.device_closed.emit(self.position)

    @staticmethod
    def _calc_min_max(byte_length: int, signed: bool):
        """Calculate min an max value which fits to bytes."""
        max_int_value = 256 ** byte_length
        return max_int_value / 2 * -1 if signed else 0.0, \
            max_int_value / 2 - 1 if signed else max_int_value - 1

    @staticmethod
    def _calc_device_length(inputs: list, outputs: list) -> int:
        """Calculate the device length with IO data."""
        if inputs and outputs:
            min_input = min(inputs, key=lambda k: k[2])
            max_output = max(outputs, key=lambda k: k[2])
        elif inputs:
            min_input = min(inputs, key=lambda k: k[2])
            max_output = max(inputs, key=lambda k: k[2])
        elif outputs:
            min_input = min(outputs, key=lambda k: k[2])
            max_output = max(outputs, key=lambda k: k[2])
        else:
            return 0

        return max_output[2] + max_output[1] - min_input[2]

    def _create_io(self, lst_ios: list, container: QtWidgets.QWidget, read_only: bool):
        lst_names = list(lst[0] for lst in lst_ios)
        layout = container.layout()  # type: QtWidgets.QFormLayout

        for val in container.findChildren(self.search_class, options=QtCore.Qt.FindDirectChildrenOnly):
            name = val.objectName()
            if name not in lst_names:
                # Remove old io from layout
                del self.__qwa[name]
                layout.removeRow(layout.getWidgetPosition(val)[0])

        counter = -1
        for io in lst_ios:
            counter += 1

            name = io[0]
            byte_length = io[1]
            bit_address = io[4]
            byteorder = io[5]
            signed = io[6]
            word_order = io[7] if len(io) > 7 else "ignored"

            val = container.findChild(self.search_class, name)
            if val is not None:
                # Destroy IO if the properties was changed
                if byte_length != val.property("byte_length") or \
                        bit_address != val.property("bit_address") or \
                        byteorder != ("big" if val.property("big_endian") else "little") or \
                        signed != val.property("signed"):
                    del self.__qwa[name]
                    layout.removeRow(layout.getWidgetPosition(val)[0])
                    pi.logger.debug("Destroy property changed IO '{0}'".format(name))
                else:
                    continue

            lbl = QtWidgets.QLabel(name, container)
            lbl.setObjectName("lbl_".format(name))
            lbl.setStyleSheet(self.style_sheet)

            val = self._create_widget(name, byte_length, bit_address, byteorder, signed, read_only, word_order)
            val.setParent(container)
            layout.insertRow(counter, val, lbl)

        self.splitter.setSizes([1, 1])

    def _create_widget(
            self, name: str, byte_length: int, bit_address: int, byteorder: str, signed: bool, read_only: bool,
            word_order: str):
        """Create widget in functions address space to use lambda functions."""
        if bit_address >= 0:
            val = QtWidgets.QCheckBox()
            val.setEnabled(not read_only)

            # Set alias to use the same function name on all widget types
            val.setValue = val.setChecked
            if not read_only:
                val.stateChanged.connect(self._change_cbx_value)
                val.value = val.isChecked

        elif byte_length > 4:
            # Bytes or string
            val = QtWidgets.QLineEdit()
            val.setReadOnly(read_only)
            val.setProperty("struct_type", "text")

            val.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            val.customContextMenuRequested.connect(self.on_context_menu)

            # Set alias to use the same function name on all widget types
            val.setValue = val.setText
            if not read_only:
                val.textChanged.connect(self._change_txt_value)
                val.value = val.text

        else:
            struct_type = "B" if byte_length == 1 else "H" if byte_length == 2 else "I"

            val = QtWidgets.QDoubleSpinBox()
            val.setReadOnly(read_only)
            val.setProperty("struct_type", struct_type)
            val.setProperty("frm", "{0}{1}".format(
                ">" if byteorder == "big" else "<",
                struct_type.lower() if signed else struct_type
            ))

            val.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            val.customContextMenuRequested.connect(self.on_context_menu)

            val.setDecimals(0)
            min_value, max_value = self._calc_min_max(byte_length, signed)
            val.setMinimum(min_value)
            val.setMaximum(max_value)
            if not read_only:
                val.valueChanged.connect(self._change_sbx_dvalue)

        val.setObjectName(name)
        val.setProperty("big_endian", byteorder == "big")
        val.setProperty("bit_address", bit_address)
        val.setProperty("byte_length", byte_length)
        val.setProperty("signed", signed)
        val.setProperty("word_order", word_order)

        self.__qwa[name] = val
        return val

    @QtCore.pyqtSlot(int)
    def _change_cbx_value(self, value: int):
        """Change value of a check box."""
        if self.sender().property("last_value") == (value == 2):
            self.sender().setStyleSheet("")
        else:
            self.sender().setStyleSheet("background-color: yellow;")

    @QtCore.pyqtSlot(float)
    def _change_sbx_dvalue(self, value: float):
        """Change value of a spin box."""
        if self.sender().property("last_value") == int(value):
            self.sender().setStyleSheet("")
        else:
            self.sender().setStyleSheet("background-color: yellow;")

    @QtCore.pyqtSlot(str)
    def _change_txt_value(self, value: str):
        """Change value of a text box."""
        if self.sender().property("last_value") == value:
            self.sender().setStyleSheet("")
        else:
            self.sender().setStyleSheet("background-color: yellow;")

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_context_menu(self, point: QtCore.QPoint):
        """Generate menu for data format changes."""
        pi.logger.debug("DebugIos.on_context_menu")

        sender = self.sender()
        men = QtWidgets.QMenu(sender)

        if sender.property("byte_length") > 4:
            # Textbox needs format buttons
            act_as_text = QtWidgets.QAction(self.tr("as text"))
            men.addAction(act_as_text)
            act_as_number = QtWidgets.QAction(self.tr("as number"))
            men.addAction(act_as_number)
            men.addSeparator()
        else:
            act_as_text = None
            act_as_number = None

        act_signed = QtWidgets.QAction(self.tr("signed"), men)
        act_signed.setCheckable(True)
        act_signed.setChecked(sender.property("signed") or False)
        men.addAction(act_signed)

        act_byteorder = QtWidgets.QAction(self.tr("big_endian"), men)
        act_byteorder.setCheckable(True)
        act_byteorder.setChecked(sender.property("big_endian") or False)
        men.addAction(act_byteorder)

        if sender.property("byte_length") > 2:
            act_wordorder = QtWidgets.QAction(self.tr("switch wordorder"))
            act_wordorder.setCheckable(True)
            act_wordorder.setChecked(sender.property("word_order") == "big")
            men.addAction(act_wordorder)
        else:
            act_wordorder = None

        rc = men.exec(sender.mapToGlobal(point))
        if not rc:
            men.deleteLater()
            return

        # Get actual value to reformat it
        actual_value, last_value = self.get_value(sender.objectName())
        if rc == act_signed:
            sender.setProperty("signed", act_signed.isChecked())
            if type(sender) == QtWidgets.QDoubleSpinBox:
                # Recalculate min / max for spinbox
                min_value, max_value = self._calc_min_max(
                    sender.property("byte_length"), sender.property("signed")
                )
                sender.setMinimum(min_value)
                sender.setMaximum(max_value)
        elif rc == act_byteorder:
            sender.setProperty("big_endian", act_byteorder.isChecked())
        elif rc == act_wordorder:
            sender.setProperty("word_order", "big" if act_wordorder.isChecked() else "little")

        if sender.property("frm"):
            sender.setProperty("frm", "{0}{1}".format(
                ">" if act_byteorder.isChecked() else "<",
                sender.property("struct_type").lower() if act_signed.isChecked()
                else sender.property("struct_type").upper()
            ))
        elif rc == act_as_text:
            sender.setProperty("struct_type", "text")
        elif rc == act_as_number:
            sender.setProperty("struct_type", "number")

        self.set_value(sender.objectName(), actual_value)
        men.deleteLater()

    def reset_label_colors(self):
        """Clean up color from labels."""
        for wid in self.findChildren(QtWidgets.QLabel):  # type: QtWidgets.QLabel
            wid.setStyleSheet("")

    def reset_change_value_colors(self, io_name=None):
        """
        Clean up color from changed outputs.

        :param io_name: Clean up only this IO
        """
        pi.logger.debug("DebugIos.reset_change_value_colors")
        if io_name is None:
            lst_wid = self.saw_out.findChildren(
                self.search_class, options=QtCore.Qt.FindDirectChildrenOnly)
        else:
            lst_wid = self.saw_out.findChildren(
                self.search_class, name=io_name, options=QtCore.Qt.FindDirectChildrenOnly)

        for wid in lst_wid:
            value, last_value = self.get_value(wid.objectName())
            if value == last_value:
                wid.setStyleSheet("")
            else:
                wid.setStyleSheet("background-color: yellow;")

    def update_ios(self, inputs: list, outputs: list):
        """Update IOs after driver reset of piCtory."""

        # Check device length, this has to match to reuse this device
        if self.length != self._calc_device_length(inputs, outputs):
            return False

        # Remove IOs, which was remove or renamed
        self._create_io(inputs, self.saw_inp, True)
        self._create_io(outputs, self.saw_out, False)

        return True

    def get_value(self, io_name: str):
        """
        Standard get function for a value of different widgets and last value.

        :param io_name: Name of IO
        :return: (actual value, last value) <class 'tuple'>
        """
        # child = self.findChild(self.search_class, io_name)
        child = self.__qwa[io_name]
        actual_value = child.value()
        last_value = child.value() if child.property("last_value") is None else child.property("last_value")
        if child.property("frm"):
            return struct.pack(child.property("frm"), int(actual_value)), \
                struct.pack(child.property("frm"), int(last_value))
        elif type(actual_value) == str:
            if child.property("struct_type") == "number":
                try:
                    actual_value = int(actual_value).to_bytes(
                        child.property("byte_length"),
                        byteorder="big" if child.property("big_endian") else "little",
                        signed=child.property("signed") or False
                    )
                    last_value = int(last_value).to_bytes(
                        child.property("byte_length"),
                        byteorder="big" if child.property("big_endian") else "little",
                        signed=child.property("signed") or False
                    )
                    return actual_value, last_value
                except Exception:
                    pi.logger.error("Could not convert '{0}' to bytes".format(actual_value))
                    pass

            return actual_value.encode(), last_value.encode()
        else:
            return actual_value, last_value

    def set_value(self, io_name: str, value, just_last_value=False):
        """
        Standard set function for a value of different widgets.

        :param io_name: Name of IO
        :param value: New value as bytes or bool for widget
        :param just_last_value: Just set last value property
        """
        child = self.__qwa[io_name]

        if child.property("word_order") == "big" and type(value) == bytes:
            value = helper.swap_word_order(value)

        if child.property("frm"):
            value = struct.unpack(child.property("frm"), value)[0]
        elif type(value) == bytes:
            if child.property("struct_type") == "text":
                try:
                    value = value.decode("utf-8")
                except UnicodeDecodeError:
                    child.setProperty("struct_type", "number")
                    QtWidgets.QMessageBox.warning(
                        self, self.tr("Can not use format text"), self.tr(
                            "Can not convert bytes {0} to a text for IO '{1}'. Switch to number format instead!"
                        ).format(value, io_name)
                    )
            if child.property("struct_type") == "number":
                # fixme: Crashs with too much bytes
                value = str(int.from_bytes(
                    value,
                    byteorder="big" if child.property("big_endian") else "little",
                    signed=child.property("signed") or False
                ))

        child.setProperty("last_value", value)
        if not just_last_value:
            child.setValue(value)
