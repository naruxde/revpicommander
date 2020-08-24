# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'revpidevelop.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wid_develop(object):
    def setupUi(self, wid_develop):
        wid_develop.setObjectName("wid_develop")
        wid_develop.resize(374, 444)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wid_develop.sizePolicy().hasHeightForWidth())
        wid_develop.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(wid_develop)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_all = QtWidgets.QPushButton(wid_develop)
        self.btn_all.setObjectName("btn_all")
        self.gridLayout.addWidget(self.btn_all, 2, 0, 1, 1)
        self.btn_upload = QtWidgets.QPushButton(wid_develop)
        self.btn_upload.setObjectName("btn_upload")
        self.gridLayout.addWidget(self.btn_upload, 2, 1, 1, 1)
        self.tree_files = QtWidgets.QTreeWidget(wid_develop)
        self.tree_files.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tree_files.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tree_files.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tree_files.setIconSize(QtCore.QSize(24, 24))
        self.tree_files.setObjectName("tree_files")
        self.tree_files.headerItem().setText(0, "1")
        self.tree_files.header().setVisible(False)
        self.gridLayout.addWidget(self.tree_files, 1, 0, 1, 2)
        self.gb_select = QtWidgets.QGroupBox(wid_develop)
        self.gb_select.setObjectName("gb_select")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_select)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_select = QtWidgets.QLabel(self.gb_select)
        self.lbl_select.setObjectName("lbl_select")
        self.gridLayout_2.addWidget(self.lbl_select, 0, 0, 1, 1)
        self.btn_select = QtWidgets.QPushButton(self.gb_select)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/ico/folder-open.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_select.setIcon(icon)
        self.btn_select.setIconSize(QtCore.QSize(24, 24))
        self.btn_select.setObjectName("btn_select")
        self.gridLayout_2.addWidget(self.btn_select, 0, 1, 1, 1)
        self.lbl_path = QtWidgets.QLabel(self.gb_select)
        self.lbl_path.setObjectName("lbl_path")
        self.gridLayout_2.addWidget(self.lbl_path, 1, 0, 1, 2)
        self.btn_refresh = QtWidgets.QPushButton(self.gb_select)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/ico/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_refresh.setIcon(icon1)
        self.btn_refresh.setIconSize(QtCore.QSize(24, 24))
        self.btn_refresh.setObjectName("btn_refresh")
        self.gridLayout_2.addWidget(self.btn_refresh, 0, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout.addWidget(self.gb_select, 0, 0, 1, 2)

        self.retranslateUi(wid_develop)
        QtCore.QMetaObject.connectSlotsByName(wid_develop)

    def retranslateUi(self, wid_develop):
        _translate = QtCore.QCoreApplication.translate
        self.btn_all.setText(_translate("wid_develop", "Stop / Upload / Start"))
        self.btn_upload.setText(_translate("wid_develop", "Just upload"))
        self.gb_select.setTitle(_translate("wid_develop", "File watcher for PLC development"))
        self.lbl_select.setText(_translate("wid_develop", "Path to development root:"))
        self.btn_select.setToolTip(_translate("wid_develop", "Open developer root directory"))
        self.lbl_path.setText(_translate("wid_develop", "/"))
        self.btn_refresh.setToolTip(_translate("wid_develop", "Reload file list"))

from . import ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wid_develop = QtWidgets.QWidget()
    ui = Ui_wid_develop()
    ui.setupUi(wid_develop)
    wid_develop.show()
    sys.exit(app.exec_())

