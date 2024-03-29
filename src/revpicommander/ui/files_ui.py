# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'files.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_win_files(object):
    def setupUi(self, win_files):
        win_files.setObjectName("win_files")
        win_files.resize(725, 519)
        self.centralwidget = QtWidgets.QWidget(win_files)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vl_local = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vl_local.setContentsMargins(0, 0, 0, 0)
        self.vl_local.setObjectName("vl_local")
        self.gb_select_local = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.gb_select_local.setObjectName("gb_select_local")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_select_local)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_select_local = QtWidgets.QLabel(self.gb_select_local)
        self.lbl_select_local.setObjectName("lbl_select_local")
        self.gridLayout_2.addWidget(self.lbl_select_local, 0, 0, 1, 1)
        self.btn_select_local = QtWidgets.QPushButton(self.gb_select_local)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/action/ico/folder-open.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_select_local.setIcon(icon)
        self.btn_select_local.setIconSize(QtCore.QSize(24, 24))
        self.btn_select_local.setAutoDefault(False)
        self.btn_select_local.setObjectName("btn_select_local")
        self.gridLayout_2.addWidget(self.btn_select_local, 0, 1, 1, 1)
        self.btn_refresh_local = QtWidgets.QPushButton(self.gb_select_local)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/action/ico/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_refresh_local.setIcon(icon1)
        self.btn_refresh_local.setIconSize(QtCore.QSize(24, 24))
        self.btn_refresh_local.setObjectName("btn_refresh_local")
        self.gridLayout_2.addWidget(self.btn_refresh_local, 0, 2, 1, 1)
        self.lbl_path_local = QtWidgets.QLabel(self.gb_select_local)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_path_local.sizePolicy().hasHeightForWidth())
        self.lbl_path_local.setSizePolicy(sizePolicy)
        self.lbl_path_local.setToolTip("/")
        self.lbl_path_local.setText("/")
        self.lbl_path_local.setObjectName("lbl_path_local")
        self.gridLayout_2.addWidget(self.lbl_path_local, 1, 0, 1, 3)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.vl_local.addWidget(self.gb_select_local)
        self.hl_revpi_2 = QtWidgets.QHBoxLayout()
        self.hl_revpi_2.setObjectName("hl_revpi_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hl_revpi_2.addItem(spacerItem)
        self.btn_to_right = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_to_right.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/action/ico/arrow-right.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_to_right.setIcon(icon2)
        self.btn_to_right.setIconSize(QtCore.QSize(24, 24))
        self.btn_to_right.setAutoDefault(False)
        self.btn_to_right.setObjectName("btn_to_right")
        self.hl_revpi_2.addWidget(self.btn_to_right)
        self.vl_local.addLayout(self.hl_revpi_2)
        self.tree_files_local = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        self.tree_files_local.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tree_files_local.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_files_local.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tree_files_local.setIconSize(QtCore.QSize(24, 24))
        self.tree_files_local.setObjectName("tree_files_local")
        self.tree_files_local.headerItem().setText(0, "1")
        self.tree_files_local.header().setVisible(False)
        self.vl_local.addWidget(self.tree_files_local)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.vl_revpi = QtWidgets.QVBoxLayout(self.gridLayoutWidget_2)
        self.vl_revpi.setContentsMargins(0, 0, 0, 0)
        self.vl_revpi.setObjectName("vl_revpi")
        self.gb_select_revpi = QtWidgets.QGroupBox(self.gridLayoutWidget_2)
        self.gb_select_revpi.setObjectName("gb_select_revpi")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gb_select_revpi)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lbl_path_revpi = QtWidgets.QLabel(self.gb_select_revpi)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_path_revpi.sizePolicy().hasHeightForWidth())
        self.lbl_path_revpi.setSizePolicy(sizePolicy)
        self.lbl_path_revpi.setToolTip("/")
        self.lbl_path_revpi.setText("/")
        self.lbl_path_revpi.setObjectName("lbl_path_revpi")
        self.gridLayout_3.addWidget(self.lbl_path_revpi, 1, 0, 1, 2)
        self.lbl_select_revpi = QtWidgets.QLabel(self.gb_select_revpi)
        self.lbl_select_revpi.setObjectName("lbl_select_revpi")
        self.gridLayout_3.addWidget(self.lbl_select_revpi, 0, 0, 1, 1)
        self.btn_refresh_revpi = QtWidgets.QPushButton(self.gb_select_revpi)
        self.btn_refresh_revpi.setIcon(icon1)
        self.btn_refresh_revpi.setIconSize(QtCore.QSize(24, 24))
        self.btn_refresh_revpi.setObjectName("btn_refresh_revpi")
        self.gridLayout_3.addWidget(self.btn_refresh_revpi, 0, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.vl_revpi.addWidget(self.gb_select_revpi)
        self.hl_revpi = QtWidgets.QHBoxLayout()
        self.hl_revpi.setObjectName("hl_revpi")
        self.btn_to_left = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_to_left.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/action/ico/arrow-left.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_to_left.setIcon(icon3)
        self.btn_to_left.setIconSize(QtCore.QSize(24, 24))
        self.btn_to_left.setAutoDefault(False)
        self.btn_to_left.setObjectName("btn_to_left")
        self.hl_revpi.addWidget(self.btn_to_left)
        self.btn_delete_revpi = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_delete_revpi.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/action/ico/edit-delete.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete_revpi.setIcon(icon4)
        self.btn_delete_revpi.setIconSize(QtCore.QSize(24, 24))
        self.btn_delete_revpi.setAutoDefault(False)
        self.btn_delete_revpi.setObjectName("btn_delete_revpi")
        self.hl_revpi.addWidget(self.btn_delete_revpi)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hl_revpi.addItem(spacerItem1)
        self.btn_mark_plcprogram = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_mark_plcprogram.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/file/ico/autostart.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_mark_plcprogram.setIcon(icon5)
        self.btn_mark_plcprogram.setIconSize(QtCore.QSize(24, 24))
        self.btn_mark_plcprogram.setAutoDefault(False)
        self.btn_mark_plcprogram.setObjectName("btn_mark_plcprogram")
        self.hl_revpi.addWidget(self.btn_mark_plcprogram)
        self.vl_revpi.addLayout(self.hl_revpi)
        self.tree_files_revpi = QtWidgets.QTreeWidget(self.gridLayoutWidget_2)
        self.tree_files_revpi.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tree_files_revpi.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_files_revpi.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tree_files_revpi.setIconSize(QtCore.QSize(24, 24))
        self.tree_files_revpi.setObjectName("tree_files_revpi")
        self.tree_files_revpi.headerItem().setText(0, "1")
        self.tree_files_revpi.header().setVisible(False)
        self.vl_revpi.addWidget(self.tree_files_revpi)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.btn_all = QtWidgets.QPushButton(self.centralwidget)
        self.btn_all.setObjectName("btn_all")
        self.gridLayout.addWidget(self.btn_all, 1, 0, 1, 1)
        win_files.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(win_files)
        self.statusbar.setObjectName("statusbar")
        win_files.setStatusBar(self.statusbar)

        self.retranslateUi(win_files)
        QtCore.QMetaObject.connectSlotsByName(win_files)

    def retranslateUi(self, win_files):
        _translate = QtCore.QCoreApplication.translate
        win_files.setWindowTitle(_translate("win_files", "File manager"))
        self.gb_select_local.setTitle(_translate("win_files", "Local computer"))
        self.lbl_select_local.setText(_translate("win_files", "Path to development root:"))
        self.btn_select_local.setToolTip(_translate("win_files", "Open developer root directory"))
        self.btn_refresh_local.setToolTip(_translate("win_files", "Reload file list"))
        self.tree_files_local.setSortingEnabled(True)
        self.gb_select_revpi.setTitle(_translate("win_files", "Revolution Pi"))
        self.lbl_select_revpi.setText(_translate("win_files", "RevPiPyLoad working directory:"))
        self.btn_refresh_revpi.setToolTip(_translate("win_files", "Reload file list"))
        self.tree_files_revpi.setSortingEnabled(True)
        self.btn_all.setText(_translate("win_files", "Stop - Upload - Start"))
from . import ressources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win_files = QtWidgets.QMainWindow()
    ui = Ui_win_files()
    ui.setupUi(win_files)
    win_files.show()
    sys.exit(app.exec_())
