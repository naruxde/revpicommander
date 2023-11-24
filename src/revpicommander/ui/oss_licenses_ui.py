# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oss_licenses.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_diag_oss_licenses(object):
    def setupUi(self, diag_oss_licenses):
        diag_oss_licenses.setObjectName("diag_oss_licenses")
        diag_oss_licenses.resize(640, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(diag_oss_licenses)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(diag_oss_licenses)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tb_oss_licenses = QtWidgets.QTableWidget(self.splitter)
        self.tb_oss_licenses.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tb_oss_licenses.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tb_oss_licenses.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tb_oss_licenses.setCornerButtonEnabled(False)
        self.tb_oss_licenses.setObjectName("tb_oss_licenses")
        self.tb_oss_licenses.setColumnCount(2)
        self.tb_oss_licenses.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_oss_licenses.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_oss_licenses.setHorizontalHeaderItem(1, item)
        self.tb_oss_licenses.horizontalHeader().setSortIndicatorShown(True)
        self.tb_oss_licenses.horizontalHeader().setStretchLastSection(True)
        self.tb_oss_licenses.verticalHeader().setVisible(False)
        self.txt_license = QtWidgets.QTextEdit(self.splitter)
        self.txt_license.setTabChangesFocus(True)
        self.txt_license.setUndoRedoEnabled(False)
        self.txt_license.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.txt_license.setReadOnly(True)
        self.txt_license.setObjectName("txt_license")
        self.verticalLayout.addWidget(self.splitter)
        self.btn_box = QtWidgets.QDialogButtonBox(diag_oss_licenses)
        self.btn_box.setOrientation(QtCore.Qt.Horizontal)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.btn_box.setObjectName("btn_box")
        self.verticalLayout.addWidget(self.btn_box)
        self.action_start = QtWidgets.QAction(diag_oss_licenses)
        self.action_start.setObjectName("action_start")

        self.retranslateUi(diag_oss_licenses)
        self.btn_box.accepted.connect(diag_oss_licenses.accept) # type: ignore
        self.btn_box.rejected.connect(diag_oss_licenses.reject) # type: ignore
        self.action_start.triggered.connect(diag_oss_licenses.exec) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(diag_oss_licenses)

    def retranslateUi(self, diag_oss_licenses):
        _translate = QtCore.QCoreApplication.translate
        diag_oss_licenses.setWindowTitle(_translate("diag_oss_licenses", "Open-Source licenses"))
        self.tb_oss_licenses.setSortingEnabled(True)
        item = self.tb_oss_licenses.horizontalHeaderItem(0)
        item.setText(_translate("diag_oss_licenses", "Software"))
        item = self.tb_oss_licenses.horizontalHeaderItem(1)
        item.setText(_translate("diag_oss_licenses", "License"))
        self.action_start.setText(_translate("diag_oss_licenses", "More licenses..."))
        self.action_start.setToolTip(_translate("diag_oss_licenses", "Show more open-source software licenses"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    diag_oss_licenses = QtWidgets.QDialog()
    ui = Ui_diag_oss_licenses()
    ui.setupUi(diag_oss_licenses)
    diag_oss_licenses.show()
    sys.exit(app.exec_())
