# -*- coding: utf-8 -*-
"""View log files from Revolution Pi."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

from enum import IntEnum

from PyQt5 import QtCore, QtGui, QtWidgets

from . import helper
from . import proginit as pi
from .ui.revpilogfile_ui import Ui_win_revpilogfile


class LogType(IntEnum):
    NONE = 0
    APP = 1
    DAEMON = 2


class DataThread(QtCore.QThread):
    error_detected = QtCore.pyqtSignal(str)
    line_logged = QtCore.pyqtSignal(LogType, bool, str)
    """log_type, success, text"""

    def __init__(self, parent=None, cycle_time=1000):
        super(DataThread, self).__init__(parent)

        self._cycle_time = cycle_time
        self._paused = True
        self.error_count = 0
        self.max_block = 16384  # 16 kByte
        self.mrk_app = 0
        self.mrk_daemon = 0

    def _load_log(self, log_type: LogType, xmlcall, start_position: int):
        """
        Get log text and put it to log viewer.

        :param log_type: Type of log file <class 'LogType'>
        :param xmlcall: XML-RPC call to get log text
        :param start_position: Start position in log file to read from
        :return: tuple(position: int, EOF: bool)
        """
        # Load max data from start position
        buff_log = helper.cm.call_remote_function(
            xmlcall,
            start_position,
            self.max_block,
            raise_exception=True
        ).data  # type: bytes

        eof = True
        if buff_log == b'\x16':  # 'ESC'
            # RevPiPyLoad could not access log file on Revolution Pi
            self.line_logged.emit(log_type, False, "")

        elif buff_log == b'\x19':  # 'EndOfMedia'
            # The log file was rotated by log rotate on the Revolution Pi
            start_position = 0
            eof = False
            pi.logger.info("RevPi started a new log file.")

        elif buff_log:
            start_position += len(buff_log)
            eof = len(buff_log) < self.max_block
            self.line_logged.emit(log_type, True, buff_log.decode("utf-8", errors="replace"))

        return start_position, eof

    def pause(self):
        """Stop checking new log lines, but leave thread alive."""
        pi.logger.debug("DataThread.pause")
        self._paused = True

    def resume(self):
        """Start checking for new log lines."""
        pi.logger.debug("DataThread.resume")
        self._paused = False

    def run(self) -> None:
        pi.logger.debug("DataThread.run")

        while not self.isInterruptionRequested():
            eof_app = False
            eof_daemon = False
            if not self._paused:
                try:
                    while not (eof_app or self.isInterruptionRequested()):
                        self.mrk_app, eof_app = self._load_log(
                            LogType.APP,
                            "load_applog",
                            self.mrk_app,
                        )
                    while not (eof_daemon or self.isInterruptionRequested()):
                        self.mrk_daemon, eof_daemon = self._load_log(
                            LogType.DAEMON,
                            "load_plclog",
                            self.mrk_daemon,
                        )
                    self.error_count = 0
                except Exception as e:
                    if self.error_count == 0:
                        self.error_detected.emit(str(e))
                    self.error_count += 1

            self.msleep(self._cycle_time)


class RevPiLogfile(QtWidgets.QMainWindow, Ui_win_revpilogfile):
    """Log file viewer for daemon and plc program log."""

    def __init__(self, parent=None):
        u"""Init RevPiLogfile-Class."""
        super(RevPiLogfile, self).__init__(parent)
        self.setupUi(self)

        self.th_data = DataThread(self)
        self.err_daemon = 0

        helper.cm.connection_established.connect(self.on_cm_connection_established)
        helper.cm.connection_disconnecting.connect(self.on_cm_connection_disconnecting)

        self._load_gui_settings()

    def _create_data_thread(self):
        self.th_data.deleteLater()

        self.th_data = DataThread(self)
        self.th_data.error_detected.connect(self.txt_daemon.setPlainText)
        self.th_data.line_logged.connect(self.on_line_logged)
        self.th_data.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        helper.settings.setValue("logfile/geo", self.saveGeometry())
        helper.settings.setValue("logfile/stay_on_top", self.cbx_stay_on_top.isChecked())

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.th_data.pause()
        super(RevPiLogfile, self).hideEvent(a0)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.th_data.resume()
        super(RevPiLogfile, self).showEvent(a0)

    def _load_gui_settings(self):
        self.restoreGeometry(helper.settings.value("logfile/geo", b''))
        self.cbx_stay_on_top.setChecked(helper.settings.value("logfile/stay_on_top", False, bool))
        self.cbx_wrap.setChecked(helper.settings.value("logfile/wrap", False, bool))

    @QtCore.pyqtSlot()
    def on_cm_connection_disconnecting(self):
        """Disconnecting form Revolution Pi."""
        self.th_data.requestInterruption()
        self.th_data.wait()

    @QtCore.pyqtSlot()
    def on_cm_connection_established(self):
        """New connection established."""
        self.txt_app.clear()
        self.txt_daemon.clear()

        self._create_data_thread()
        if self.isVisible():
            self.th_data.resume()

    @QtCore.pyqtSlot()
    def on_btn_daemon_clicked(self):
        """Clear the daemon log view."""
        self.txt_daemon.clear()

    @QtCore.pyqtSlot()
    def on_btn_app_clicked(self):
        """Clear the app log view."""
        self.txt_app.clear()

    @QtCore.pyqtSlot(int)
    def on_cbx_stay_on_top_stateChanged(self, state: int):
        """Set flag to stay on top of all windows."""
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, state == QtCore.Qt.Checked)

    @QtCore.pyqtSlot(int)
    def on_cbx_wrap_stateChanged(self, state: int):
        """Line wrap mode."""
        wrap_mode = QtWidgets.QPlainTextEdit.WidgetWidth if state == QtCore.Qt.Checked else \
            QtWidgets.QPlainTextEdit.NoWrap
        self.txt_daemon.setLineWrapMode(wrap_mode)
        self.txt_app.setLineWrapMode(wrap_mode)
        helper.settings.setValue("logfile/wrap", self.cbx_wrap.isChecked())

    @QtCore.pyqtSlot(LogType, bool, str)
    def on_line_logged(self, log_type: LogType, success: bool, text: str):
        pi.logger.debug("RevPiLogfile.on_line_logged")

        if log_type == LogType.APP:
            textwidget = self.txt_app
        elif log_type == LogType.DAEMON:
            textwidget = self.txt_daemon
        else:
            return

        bar = textwidget.verticalScrollBar()
        auto_scroll = bar.value() == bar.maximum()

        if not success:
            textwidget.clear()
            textwidget.setPlainText(self.tr("Can not access log file on the RevPi"))
        elif text != "":
            # Function will add \n automatically
            textwidget.appendPlainText(text.strip("\n"))
            if auto_scroll:
                bar.setValue(bar.maximum())
