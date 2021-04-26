# -*- coding: utf-8 -*-
"""File transfer system to handle QThreads."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2021 Sven Sager"
__license__ = "GPLv3"

from logging import getLogger

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.backgroundworker_ui import Ui_diag_backgroundworker

log = getLogger()


class BackgroundWorker(QtCore.QThread):
    steps_todo = QtCore.pyqtSignal(int)
    steps_done = QtCore.pyqtSignal(int)
    status_message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(BackgroundWorker, self).__init__(parent)

    def check_cancel(self) -> bool:
        """
        Check for interruption of thread and show message

        :return: True, if interruption was requested
        """
        if self.isInterruptionRequested():
            self.status_message.emit(self.tr("User requested cancellation..."))
            self.msleep(750)
            return True
        return False

    def exec_dialog(self) -> int:
        diag = WorkerDialog(self, self.parent())
        rc = diag.exec()
        diag.deleteLater()
        return rc

    def wait_interruptable(self, seconds=-1) -> None:
        """Save function to wait and get the cancel buttons."""
        counter = seconds * 4
        while counter != 0:
            counter -= 1
            self.msleep(250)
            if self._check_cancel():
                break

    def run(self) -> None:
        """Worker thread to import pictures from camera."""
        log.debug("BackgroundWorker.run")
        self.status_message.emit("Started dummy thread...")
        self.wait_interruptable(5)
        self.status_message.emit("Completed dummy thread.")
        self._save_wait(3)


class WorkerDialog(QtWidgets.QDialog, Ui_diag_backgroundworker):

    def __init__(self, worker_thread: BackgroundWorker, parent=None):
        """
        Base of dialog to show progress from a background thread.

        :param worker_thread: Thread with the logic work to do
        :param parent: QtWidget
        """
        super(WorkerDialog, self).__init__(parent)
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
        return super(WorkerDialog, self).exec()

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
