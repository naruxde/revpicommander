# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'avahisearch.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_diag_search(object):
    def setupUi(self, diag_search):
        diag_search.setObjectName("diag_search")
        diag_search.resize(480, 360)
        self.gridLayout = QtWidgets.QGridLayout(diag_search)
        self.gridLayout.setObjectName("gridLayout")
        self.hl_header = QtWidgets.QHBoxLayout()
        self.hl_header.setObjectName("hl_header")
        self.lbl_search = QtWidgets.QLabel(diag_search)
        self.lbl_search.setObjectName("lbl_search")
        self.hl_header.addWidget(self.lbl_search)
        self.btn_restart = QtWidgets.QPushButton(diag_search)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_restart.sizePolicy().hasHeightForWidth())
        self.btn_restart.setSizePolicy(sizePolicy)
        self.btn_restart.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/ico/reload.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_restart.setIcon(icon)
        self.btn_restart.setIconSize(QtCore.QSize(24, 24))
        self.btn_restart.setObjectName("btn_restart")
        self.hl_header.addWidget(self.btn_restart)
        self.gridLayout.addLayout(self.hl_header, 0, 0, 1, 2)
        self.tb_revpi = QtWidgets.QTableWidget(diag_search)
        self.tb_revpi.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tb_revpi.setTabKeyNavigation(False)
        self.tb_revpi.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tb_revpi.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tb_revpi.setWordWrap(False)
        self.tb_revpi.setCornerButtonEnabled(False)
        self.tb_revpi.setObjectName("tb_revpi")
        self.tb_revpi.setColumnCount(2)
        self.tb_revpi.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_revpi.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_revpi.setHorizontalHeaderItem(1, item)
        self.tb_revpi.horizontalHeader().setHighlightSections(False)
        self.tb_revpi.horizontalHeader().setStretchLastSection(True)
        self.tb_revpi.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tb_revpi, 1, 0, 1, 2)
        self.btn_connect = QtWidgets.QPushButton(diag_search)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout.addWidget(self.btn_connect, 2, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(diag_search)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 2, 1, 1, 1)
        self.btn_box = QtWidgets.QDialogButtonBox(diag_search)
        self.btn_box.setOrientation(QtCore.Qt.Horizontal)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.btn_box.setObjectName("btn_box")
        self.gridLayout.addWidget(self.btn_box, 3, 0, 1, 2)

        self.retranslateUi(diag_search)
        self.btn_box.rejected.connect(diag_search.reject)
        QtCore.QMetaObject.connectSlotsByName(diag_search)

    def retranslateUi(self, diag_search):
        _translate = QtCore.QCoreApplication.translate
        diag_search.setWindowTitle(_translate("diag_search", "Search Revolution Pi devices"))
        self.lbl_search.setText(_translate("diag_search", "Searching for Revolution Pi devices in your network..."))
        self.btn_restart.setToolTip(_translate("diag_search", "Restart search"))
        self.tb_revpi.setSortingEnabled(True)
        item = self.tb_revpi.horizontalHeaderItem(0)
        item.setText(_translate("diag_search", "Zero-conf name"))
        item = self.tb_revpi.horizontalHeaderItem(1)
        item.setText(_translate("diag_search", "IP address"))
        self.btn_connect.setText(_translate("diag_search", "&Connect to Revolution Pi"))
        self.btn_save.setText(_translate("diag_search", "&Save connection"))
from . import ressources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    diag_search = QtWidgets.QDialog()
    ui = Ui_diag_search()
    ui.setupUi(diag_search)
    diag_search.show()
    sys.exit(app.exec_())
