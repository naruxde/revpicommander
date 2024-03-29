# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'revpicommander.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_win_revpicommander(object):
    def setupUi(self, win_revpicommander):
        win_revpicommander.setObjectName("win_revpicommander")
        win_revpicommander.resize(353, 299)
        win_revpicommander.setWindowTitle("RevPi Commander")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main/ico/revpipycontrol.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        win_revpicommander.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(win_revpicommander)
        self.centralwidget.setObjectName("centralwidget")
        self.gl = QtWidgets.QVBoxLayout(self.centralwidget)
        self.gl.setObjectName("gl")
        self.hzl_connection = QtWidgets.QHBoxLayout()
        self.hzl_connection.setObjectName("hzl_connection")
        self.txt_host = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_host.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txt_host.setText("")
        self.txt_host.setReadOnly(True)
        self.txt_host.setObjectName("txt_host")
        self.hzl_connection.addWidget(self.txt_host)
        self.txt_connection = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_connection.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txt_connection.setText("")
        self.txt_connection.setReadOnly(True)
        self.txt_connection.setObjectName("txt_connection")
        self.hzl_connection.addWidget(self.txt_connection)
        self.gl.addLayout(self.hzl_connection)
        self.btn_plc_start = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/ico/system-run.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_plc_start.setIcon(icon1)
        self.btn_plc_start.setObjectName("btn_plc_start")
        self.gl.addWidget(self.btn_plc_start)
        self.btn_plc_stop = QtWidgets.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/action/ico/process-stop.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_plc_stop.setIcon(icon2)
        self.btn_plc_stop.setObjectName("btn_plc_stop")
        self.gl.addWidget(self.btn_plc_stop)
        self.btn_plc_restart = QtWidgets.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/action/ico/view-refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_plc_restart.setIcon(icon3)
        self.btn_plc_restart.setObjectName("btn_plc_restart")
        self.gl.addWidget(self.btn_plc_restart)
        self.btn_plc_logs = QtWidgets.QPushButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/action/ico/applications-utilities.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_plc_logs.setIcon(icon4)
        self.btn_plc_logs.setObjectName("btn_plc_logs")
        self.gl.addWidget(self.btn_plc_logs)
        self.hzl_status = QtWidgets.QHBoxLayout()
        self.hzl_status.setObjectName("hzl_status")
        self.lbl_status = QtWidgets.QLabel(self.centralwidget)
        self.lbl_status.setObjectName("lbl_status")
        self.hzl_status.addWidget(self.lbl_status)
        self.txt_status = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_status.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txt_status.setText("")
        self.txt_status.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_status.setReadOnly(True)
        self.txt_status.setObjectName("txt_status")
        self.hzl_status.addWidget(self.txt_status)
        self.gl.addLayout(self.hzl_status)
        self.btn_plc_debug = QtWidgets.QPushButton(self.centralwidget)
        self.btn_plc_debug.setMinimumSize(QtCore.QSize(300, 0))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/action/ico/edit-find.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_plc_debug.setIcon(icon5)
        self.btn_plc_debug.setCheckable(True)
        self.btn_plc_debug.setObjectName("btn_plc_debug")
        self.gl.addWidget(self.btn_plc_debug)
        win_revpicommander.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(win_revpicommander)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 353, 24))
        self.menubar.setObjectName("menubar")
        self.men_file = QtWidgets.QMenu(self.menubar)
        self.men_file.setObjectName("men_file")
        self.men_help = QtWidgets.QMenu(self.menubar)
        self.men_help.setObjectName("men_help")
        self.men_plc = QtWidgets.QMenu(self.menubar)
        self.men_plc.setObjectName("men_plc")
        self.men_connections = QtWidgets.QMenu(self.menubar)
        self.men_connections.setObjectName("men_connections")
        win_revpicommander.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(win_revpicommander)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        win_revpicommander.setStatusBar(self.statusbar)
        self.act_connections = QtWidgets.QAction(win_revpicommander)
        self.act_connections.setShortcut("Ctrl+N")
        self.act_connections.setObjectName("act_connections")
        self.act_search = QtWidgets.QAction(win_revpicommander)
        self.act_search.setShortcut("Ctrl+F")
        self.act_search.setObjectName("act_search")
        self.act_quit = QtWidgets.QAction(win_revpicommander)
        self.act_quit.setObjectName("act_quit")
        self.act_webpage = QtWidgets.QAction(win_revpicommander)
        self.act_webpage.setObjectName("act_webpage")
        self.act_info = QtWidgets.QAction(win_revpicommander)
        self.act_info.setObjectName("act_info")
        self.act_logs = QtWidgets.QAction(win_revpicommander)
        self.act_logs.setShortcut("Ctrl+L")
        self.act_logs.setObjectName("act_logs")
        self.act_options = QtWidgets.QAction(win_revpicommander)
        self.act_options.setShortcut("Ctrl+O")
        self.act_options.setObjectName("act_options")
        self.act_program = QtWidgets.QAction(win_revpicommander)
        self.act_program.setShortcut("Ctrl+P")
        self.act_program.setObjectName("act_program")
        self.act_developer = QtWidgets.QAction(win_revpicommander)
        self.act_developer.setShortcut("Ctrl+D")
        self.act_developer.setObjectName("act_developer")
        self.act_pictory = QtWidgets.QAction(win_revpicommander)
        self.act_pictory.setObjectName("act_pictory")
        self.act_disconnect = QtWidgets.QAction(win_revpicommander)
        self.act_disconnect.setShortcut("Ctrl+X")
        self.act_disconnect.setObjectName("act_disconnect")
        self.act_reset = QtWidgets.QAction(win_revpicommander)
        self.act_reset.setObjectName("act_reset")
        self.act_simulator = QtWidgets.QAction(win_revpicommander)
        self.act_simulator.setObjectName("act_simulator")
        self.men_file.addAction(self.act_connections)
        self.men_file.addAction(self.act_search)
        self.men_file.addSeparator()
        self.men_file.addAction(self.act_simulator)
        self.men_file.addSeparator()
        self.men_file.addAction(self.act_quit)
        self.men_help.addAction(self.act_webpage)
        self.men_help.addSeparator()
        self.men_help.addAction(self.act_info)
        self.men_plc.addAction(self.act_logs)
        self.men_plc.addAction(self.act_options)
        self.men_plc.addAction(self.act_program)
        self.men_plc.addAction(self.act_developer)
        self.men_plc.addSeparator()
        self.men_plc.addAction(self.act_pictory)
        self.men_plc.addAction(self.act_reset)
        self.men_plc.addSeparator()
        self.men_plc.addAction(self.act_disconnect)
        self.menubar.addAction(self.men_file.menuAction())
        self.menubar.addAction(self.men_plc.menuAction())
        self.menubar.addAction(self.men_connections.menuAction())
        self.menubar.addAction(self.men_help.menuAction())

        self.retranslateUi(win_revpicommander)
        self.act_quit.triggered.connect(win_revpicommander.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(win_revpicommander)
        win_revpicommander.setTabOrder(self.btn_plc_start, self.btn_plc_stop)
        win_revpicommander.setTabOrder(self.btn_plc_stop, self.btn_plc_restart)
        win_revpicommander.setTabOrder(self.btn_plc_restart, self.btn_plc_logs)
        win_revpicommander.setTabOrder(self.btn_plc_logs, self.btn_plc_debug)

    def retranslateUi(self, win_revpicommander):
        _translate = QtCore.QCoreApplication.translate
        self.btn_plc_start.setText(_translate("win_revpicommander", "PLC &start"))
        self.btn_plc_stop.setText(_translate("win_revpicommander", "PLC s&top"))
        self.btn_plc_restart.setText(_translate("win_revpicommander", "PLC restart"))
        self.btn_plc_logs.setText(_translate("win_revpicommander", "PLC &logs"))
        self.lbl_status.setText(_translate("win_revpicommander", "Status:"))
        self.btn_plc_debug.setText(_translate("win_revpicommander", "PLC watch &mode"))
        self.men_file.setTitle(_translate("win_revpicommander", "&File"))
        self.men_help.setTitle(_translate("win_revpicommander", "&Help"))
        self.men_plc.setTitle(_translate("win_revpicommander", "&PLC"))
        self.men_connections.setTitle(_translate("win_revpicommander", "&Connections"))
        self.act_connections.setText(_translate("win_revpicommander", "&Connections..."))
        self.act_search.setText(_translate("win_revpicommander", "&Search Revolution Pi..."))
        self.act_quit.setText(_translate("win_revpicommander", "&Quit"))
        self.act_webpage.setText(_translate("win_revpicommander", "Visit &webpage..."))
        self.act_info.setText(_translate("win_revpicommander", "&Info..."))
        self.act_logs.setText(_translate("win_revpicommander", "PLC &logs..."))
        self.act_options.setText(_translate("win_revpicommander", "PLC &options..."))
        self.act_program.setText(_translate("win_revpicommander", "PLC progra&m..."))
        self.act_developer.setText(_translate("win_revpicommander", "PLC de&veloper..."))
        self.act_pictory.setText(_translate("win_revpicommander", "piCtory configuraiton..."))
        self.act_disconnect.setText(_translate("win_revpicommander", "&Disconnect"))
        self.act_reset.setText(_translate("win_revpicommander", "Reset driver..."))
        self.act_simulator.setText(_translate("win_revpicommander", "RevPi si&mulator..."))
from . import ressources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win_revpicommander = QtWidgets.QMainWindow()
    ui = Ui_win_revpicommander()
    ui.setupUi(win_revpicommander)
    win_revpicommander.show()
    sys.exit(app.exec_())
