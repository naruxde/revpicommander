# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debugios.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_win_debugios(object):
    def setupUi(self, win_debugios):
        win_debugios.setObjectName("win_debugios")
        win_debugios.resize(434, 343)
        self.centralwidget = QtWidgets.QWidget(win_debugios)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gb_io = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_io.setObjectName("gb_io")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gb_io)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.gb_io)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.sca_inp = QtWidgets.QScrollArea(self.splitter)
        self.sca_inp.setLineWidth(0)
        self.sca_inp.setWidgetResizable(True)
        self.sca_inp.setObjectName("sca_inp")
        self.saw_inp = QtWidgets.QWidget()
        self.saw_inp.setGeometry(QtCore.QRect(0, 0, 201, 275))
        self.saw_inp.setObjectName("saw_inp")
        self.form_inp = QtWidgets.QFormLayout(self.saw_inp)
        self.form_inp.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.form_inp.setContentsMargins(-1, 6, -1, 6)
        self.form_inp.setObjectName("form_inp")
        self.sca_inp.setWidget(self.saw_inp)
        self.sca_out = QtWidgets.QScrollArea(self.splitter)
        self.sca_out.setLineWidth(0)
        self.sca_out.setWidgetResizable(True)
        self.sca_out.setObjectName("sca_out")
        self.saw_out = QtWidgets.QWidget()
        self.saw_out.setGeometry(QtCore.QRect(0, 0, 201, 275))
        self.saw_out.setObjectName("saw_out")
        self.form_out = QtWidgets.QFormLayout(self.saw_out)
        self.form_out.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.form_out.setContentsMargins(-1, 6, -1, 6)
        self.form_out.setObjectName("form_out")
        self.sca_out.setWidget(self.saw_out)
        self.verticalLayout_2.addWidget(self.splitter)
        self.verticalLayout.addWidget(self.gb_io)
        win_debugios.setCentralWidget(self.centralwidget)
        self.stat_bar = QtWidgets.QStatusBar(win_debugios)
        self.stat_bar.setObjectName("stat_bar")
        win_debugios.setStatusBar(self.stat_bar)

        self.retranslateUi(win_debugios)
        QtCore.QMetaObject.connectSlotsByName(win_debugios)

    def retranslateUi(self, win_debugios):
        _translate = QtCore.QCoreApplication.translate
        self.gb_io.setTitle(_translate("win_debugios", "{0}: Inputs | Outputs"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win_debugios = QtWidgets.QMainWindow()
    ui = Ui_win_debugios()
    ui.setupUi(win_debugios)
    win_debugios.show()
    sys.exit(app.exec_())
