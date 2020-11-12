# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'revpilogfile.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_win_revpilogfile(object):
    def setupUi(self, win_revpilogfile):
        win_revpilogfile.setObjectName("win_revpilogfile")
        win_revpilogfile.resize(796, 347)
        self.centralwidget = QtWidgets.QWidget(win_revpilogfile)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cbx_stay_on_top = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_stay_on_top.setObjectName("cbx_stay_on_top")
        self.gridLayout_3.addWidget(self.cbx_stay_on_top, 1, 0, 1, 1)
        self.cbx_wrap = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_wrap.setObjectName("cbx_wrap")
        self.gridLayout_3.addWidget(self.cbx_wrap, 1, 1, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.gridLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid_daemon = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid_daemon.setContentsMargins(0, 0, 0, 0)
        self.grid_daemon.setObjectName("grid_daemon")
        self.lbl_daemon = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_daemon.setObjectName("lbl_daemon")
        self.grid_daemon.addWidget(self.lbl_daemon, 0, 0, 1, 1)
        self.btn_daemon = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_daemon.setObjectName("btn_daemon")
        self.grid_daemon.addWidget(self.btn_daemon, 0, 1, 1, 1)
        self.txt_daemon = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.txt_daemon.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt_daemon.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt_daemon.setTabChangesFocus(True)
        self.txt_daemon.setUndoRedoEnabled(False)
        self.txt_daemon.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.txt_daemon.setReadOnly(True)
        self.txt_daemon.setObjectName("txt_daemon")
        self.grid_daemon.addWidget(self.txt_daemon, 1, 0, 1, 2)
        self.grid_daemon.setColumnStretch(0, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.grid_app = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.grid_app.setContentsMargins(0, 0, 0, 0)
        self.grid_app.setObjectName("grid_app")
        self.btn_app = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_app.setObjectName("btn_app")
        self.grid_app.addWidget(self.btn_app, 0, 1, 1, 1)
        self.lbl_app = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.lbl_app.setObjectName("lbl_app")
        self.grid_app.addWidget(self.lbl_app, 0, 0, 1, 1)
        self.txt_app = QtWidgets.QPlainTextEdit(self.gridLayoutWidget_2)
        self.txt_app.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt_app.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txt_app.setTabChangesFocus(True)
        self.txt_app.setUndoRedoEnabled(False)
        self.txt_app.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.txt_app.setReadOnly(True)
        self.txt_app.setObjectName("txt_app")
        self.grid_app.addWidget(self.txt_app, 1, 0, 1, 2)
        self.grid_app.setColumnStretch(0, 1)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 2)
        win_revpilogfile.setCentralWidget(self.centralwidget)

        self.retranslateUi(win_revpilogfile)
        QtCore.QMetaObject.connectSlotsByName(win_revpilogfile)

    def retranslateUi(self, win_revpilogfile):
        _translate = QtCore.QCoreApplication.translate
        win_revpilogfile.setWindowTitle(_translate("win_revpilogfile", "RevPi Python PLC Logfiles"))
        self.cbx_stay_on_top.setText(_translate("win_revpilogfile", "Stay on top of all windows"))
        self.cbx_wrap.setText(_translate("win_revpilogfile", "Linewrap"))
        self.lbl_daemon.setText(_translate("win_revpilogfile", "RevPiPyLoad - Logfile"))
        self.btn_daemon.setText(_translate("win_revpilogfile", "Clear view"))
        self.btn_app.setText(_translate("win_revpilogfile", "Clear view"))
        self.lbl_app.setText(_translate("win_revpilogfile", "Python PLC program - Logfile"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win_revpilogfile = QtWidgets.QMainWindow()
    ui = Ui_win_revpilogfile()
    ui.setupUi(win_revpilogfile)
    win_revpilogfile.show()
    sys.exit(app.exec_())
