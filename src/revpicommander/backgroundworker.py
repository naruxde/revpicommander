# -*- coding: utf-8 -*-
"""File transfer system to handle QThreads."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

from logging import getLogger

from PyQt5 import QtCore, QtGui, QtWidgets

from .ui.backgroundworker_ui import Ui_diag_backgroundworker

log = getLogger(__name__)


class BackgroundWorker(QtCore.QThread):
    steps_todo = QtCore.pyqtSignal(int)
    steps_done = QtCore.pyqtSignal(int)
    status_message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, interruption_text: str = None):
        super().__init__(parent)
        self._interruption_text = interruption_text or self.tr("User requested cancellation...")

    def check_cancel(self) -> bool:
        """
        Check for interruption of thread and show message

        :return: True, if interruption was requested
        """
        if self.isInterruptionRequested():
            self.status_message.emit(self._interruption_text)
            self.msleep(750)
            return True
        return False

    def exec_dialog(self, window_title="", can_cancel=True) -> int:
        """
        Show dialog with progress bar.

        :param window_title: Title of Dialog window
        :param can_cancel: If False, the cancel button is deactivated
        :return: Dialog result
        """
        diag = WorkerDialog(self, self.parent())
        diag.setWindowTitle(window_title)
        diag.btn_box.setEnabled(can_cancel)
        rc = diag.exec()
        diag.deleteLater()
        return rc

    def wait_interruptable(self, seconds=-1) -> bool:
        """
        Save function to wait and get the cancel buttons.

        :param seconds: Wait this amount of seconds
        :return: True, if interruption was requested
        """
        counter = seconds * 4
        while counter != 0:
            counter -= 1
            self.msleep(250)
            if self.check_cancel():
                return True
        return False

    def run(self) -> None:
        """Override this function with your logic."""
        raise NotImplementedError()


class BackgroundWaiter(BackgroundWorker):
    """Just wait an amount of time and show progress bar."""

    def __init__(self, seconds: int, status_message: str, parent=None, interruption_text: str = None):
        super().__init__(parent, interruption_text)
        self._status_message = status_message
        self._wait_steps = seconds * 4

    def run(self) -> None:
        log.debug("BackgroundWaiter.run")
        self.steps_todo.emit(self._wait_steps)
        self.status_message.emit(self._status_message)
        counter = 0
        while counter <= self._wait_steps:
            counter += 1
            self.msleep(250)
            if self.isInterruptionRequested():
                self.steps_done.emit(self._wait_steps)
            if self.check_cancel():
                return
            self.steps_done.emit(counter)


class WorkerDialog(QtWidgets.QDialog, Ui_diag_backgroundworker):

    def __init__(self, worker_thread: BackgroundWorker, parent=None):
        """
        Base of dialog to show progress from a background thread.

        :param worker_thread: Thread with the logic work to do
        :param parent: QtWidget
        """
        super().__init__(parent)
        self.setupUi(self)

        self._canceled = False

        self._th = worker_thread
        self._th.finished.connect(self.on_th_finished)
        self._th.steps_todo.connect(self.pgb_status.setMaximum)
        self._th.steps_done.connect(self.pgb_status.setValue)
        self._th.status_message.connect(self.lbl_status.setText)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        a0.ignore()

    def exec(self) -> int:
        self._th.start()
        return super().exec()

    @QtCore.pyqtSlot()
    def on_th_finished(self) -> None:
        """Check the result of import thread."""
        if self._canceled:
            self.reject()
        else:
            self.accept()

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_btn_box_clicked(self, button: QtWidgets.QAbstractButton) -> None:
        """Control buttons for dialog."""
        role = self.btn_box.buttonRole(button)
        log.debug("WorkerDialog.on_btn_box_clicked({0})".format(role))

        if role == QtWidgets.QDialogButtonBox.RejectRole:
            self._th.requestInterruption()
            self._canceled = True
