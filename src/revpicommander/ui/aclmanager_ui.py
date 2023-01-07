# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aclmanager.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_diag_aclmanager(object):
    def setupUi(self, diag_aclmanager):
        diag_aclmanager.setObjectName("diag_aclmanager")
        diag_aclmanager.resize(454, 572)
        self.verticalLayout = QtWidgets.QVBoxLayout(diag_aclmanager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gb_acls = QtWidgets.QGroupBox(diag_aclmanager)
        self.gb_acls.setObjectName("gb_acls")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gb_acls)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tb_acls = QtWidgets.QTableWidget(self.gb_acls)
        self.tb_acls.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tb_acls.setTabKeyNavigation(False)
        self.tb_acls.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tb_acls.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tb_acls.setWordWrap(False)
        self.tb_acls.setCornerButtonEnabled(False)
        self.tb_acls.setObjectName("tb_acls")
        self.tb_acls.setColumnCount(2)
        self.tb_acls.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_acls.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_acls.setHorizontalHeaderItem(1, item)
        self.tb_acls.horizontalHeader().setHighlightSections(False)
        self.tb_acls.horizontalHeader().setStretchLastSection(True)
        self.tb_acls.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tb_acls)
        self.hl_acls = QtWidgets.QHBoxLayout()
        self.hl_acls.setObjectName("hl_acls")
        self.btn_edit = QtWidgets.QPushButton(self.gb_acls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_edit.sizePolicy().hasHeightForWidth())
        self.btn_edit.setSizePolicy(sizePolicy)
        self.btn_edit.setObjectName("btn_edit")
        self.hl_acls.addWidget(self.btn_edit)
        self.btn_remove = QtWidgets.QPushButton(self.gb_acls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_remove.sizePolicy().hasHeightForWidth())
        self.btn_remove.setSizePolicy(sizePolicy)
        self.btn_remove.setObjectName("btn_remove")
        self.hl_acls.addWidget(self.btn_remove)
        self.verticalLayout_2.addLayout(self.hl_acls)
        self.verticalLayout.addWidget(self.gb_acls)
        self.gb_edit = QtWidgets.QGroupBox(diag_aclmanager)
        self.gb_edit.setObjectName("gb_edit")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_edit)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_clear = QtWidgets.QPushButton(self.gb_edit)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout_2.addWidget(self.btn_clear, 1, 0, 1, 1)
        self.btn_add = QtWidgets.QPushButton(self.gb_edit)
        self.btn_add.setObjectName("btn_add")
        self.gridLayout_2.addWidget(self.btn_add, 1, 1, 1, 1)
        self.fl_edit = QtWidgets.QFormLayout()
        self.fl_edit.setObjectName("fl_edit")
        self.lbl_ip = QtWidgets.QLabel(self.gb_edit)
        self.lbl_ip.setObjectName("lbl_ip")
        self.fl_edit.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_ip)
        self.lbl_level = QtWidgets.QLabel(self.gb_edit)
        self.lbl_level.setObjectName("lbl_level")
        self.fl_edit.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_level)
        self.cbb_level = QtWidgets.QComboBox(self.gb_edit)
        self.cbb_level.setObjectName("cbb_level")
        self.fl_edit.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbb_level)
        self.hl_ip = QtWidgets.QHBoxLayout()
        self.hl_ip.setObjectName("hl_ip")
        self.txt_ip_a = QtWidgets.QLineEdit(self.gb_edit)
        self.txt_ip_a.setMaxLength(3)
        self.txt_ip_a.setObjectName("txt_ip_a")
        self.hl_ip.addWidget(self.txt_ip_a)
        self.lbl_ip_a = QtWidgets.QLabel(self.gb_edit)
        self.lbl_ip_a.setText(".")
        self.lbl_ip_a.setObjectName("lbl_ip_a")
        self.hl_ip.addWidget(self.lbl_ip_a)
        self.txt_ip_b = QtWidgets.QLineEdit(self.gb_edit)
        self.txt_ip_b.setMaxLength(3)
        self.txt_ip_b.setObjectName("txt_ip_b")
        self.hl_ip.addWidget(self.txt_ip_b)
        self.lbl_ip_b = QtWidgets.QLabel(self.gb_edit)
        self.lbl_ip_b.setText(".")
        self.lbl_ip_b.setObjectName("lbl_ip_b")
        self.hl_ip.addWidget(self.lbl_ip_b)
        self.txt_ip_c = QtWidgets.QLineEdit(self.gb_edit)
        self.txt_ip_c.setMaxLength(3)
        self.txt_ip_c.setObjectName("txt_ip_c")
        self.hl_ip.addWidget(self.txt_ip_c)
        self.lbl_ip_c = QtWidgets.QLabel(self.gb_edit)
        self.lbl_ip_c.setText(".")
        self.lbl_ip_c.setObjectName("lbl_ip_c")
        self.hl_ip.addWidget(self.lbl_ip_c)
        self.txt_ip_d = QtWidgets.QLineEdit(self.gb_edit)
        self.txt_ip_d.setMaxLength(3)
        self.txt_ip_d.setObjectName("txt_ip_d")
        self.hl_ip.addWidget(self.txt_ip_d)
        self.fl_edit.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.hl_ip)
        self.gridLayout_2.addLayout(self.fl_edit, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.gb_edit)
        self.lbl_level_info = QtWidgets.QLabel(diag_aclmanager)
        self.lbl_level_info.setText("")
        self.lbl_level_info.setObjectName("lbl_level_info")
        self.verticalLayout.addWidget(self.lbl_level_info)
        self.btn_box = QtWidgets.QDialogButtonBox(diag_aclmanager)
        self.btn_box.setOrientation(QtCore.Qt.Horizontal)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_box.setObjectName("btn_box")
        self.verticalLayout.addWidget(self.btn_box)

        self.retranslateUi(diag_aclmanager)
        self.btn_box.accepted.connect(diag_aclmanager.accept) # type: ignore
        self.btn_box.rejected.connect(diag_aclmanager.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(diag_aclmanager)
        diag_aclmanager.setTabOrder(self.tb_acls, self.btn_edit)
        diag_aclmanager.setTabOrder(self.btn_edit, self.btn_remove)
        diag_aclmanager.setTabOrder(self.btn_remove, self.txt_ip_a)
        diag_aclmanager.setTabOrder(self.txt_ip_a, self.txt_ip_b)
        diag_aclmanager.setTabOrder(self.txt_ip_b, self.txt_ip_c)
        diag_aclmanager.setTabOrder(self.txt_ip_c, self.txt_ip_d)
        diag_aclmanager.setTabOrder(self.txt_ip_d, self.cbb_level)

    def retranslateUi(self, diag_aclmanager):
        _translate = QtCore.QCoreApplication.translate
        diag_aclmanager.setWindowTitle(_translate("diag_aclmanager", "IP access control list"))
        self.gb_acls.setTitle(_translate("diag_aclmanager", "Existing ACLs"))
        item = self.tb_acls.horizontalHeaderItem(0)
        item.setText(_translate("diag_aclmanager", "IP Address"))
        item = self.tb_acls.horizontalHeaderItem(1)
        item.setText(_translate("diag_aclmanager", "Access Level"))
        self.btn_edit.setText(_translate("diag_aclmanager", "&Edit"))
        self.btn_remove.setText(_translate("diag_aclmanager", "&Remove"))
        self.gb_edit.setTitle(_translate("diag_aclmanager", "Add / Edit access entry"))
        self.btn_clear.setText(_translate("diag_aclmanager", "Clear fields"))
        self.btn_add.setText(_translate("diag_aclmanager", "&Save entry"))
        self.lbl_ip.setText(_translate("diag_aclmanager", "IP address:"))
        self.lbl_level.setText(_translate("diag_aclmanager", "Access level:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    diag_aclmanager = QtWidgets.QDialog()
    ui = Ui_diag_aclmanager()
    ui.setupUi(diag_aclmanager)
    diag_aclmanager.show()
    sys.exit(app.exec_())
