# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debugcontrol.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wid_debugcontrol(object):
    def setupUi(self, wid_debugcontrol):
        wid_debugcontrol.setObjectName("wid_debugcontrol")
        wid_debugcontrol.resize(402, 214)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wid_debugcontrol.sizePolicy().hasHeightForWidth())
        wid_debugcontrol.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(wid_debugcontrol)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gb_devices = QtWidgets.QGroupBox(wid_debugcontrol)
        self.gb_devices.setObjectName("gb_devices")
        self.vl_devices = QtWidgets.QVBoxLayout(self.gb_devices)
        self.vl_devices.setObjectName("vl_devices")
        self.gridLayout.addWidget(self.gb_devices, 0, 0, 1, 1)
        self.cbx_stay_on_top = QtWidgets.QCheckBox(wid_debugcontrol)
        self.cbx_stay_on_top.setObjectName("cbx_stay_on_top")
        self.gridLayout.addWidget(self.cbx_stay_on_top, 1, 0, 1, 1)
        self.gb_control = QtWidgets.QGroupBox(wid_debugcontrol)
        self.gb_control.setObjectName("gb_control")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gb_control)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_read_io = QtWidgets.QPushButton(self.gb_control)
        self.btn_read_io.setObjectName("btn_read_io")
        self.verticalLayout.addWidget(self.btn_read_io)
        self.btn_refresh_io = QtWidgets.QPushButton(self.gb_control)
        self.btn_refresh_io.setObjectName("btn_refresh_io")
        self.verticalLayout.addWidget(self.btn_refresh_io)
        self.btn_write_o = QtWidgets.QPushButton(self.gb_control)
        self.btn_write_o.setObjectName("btn_write_o")
        self.verticalLayout.addWidget(self.btn_write_o)
        self.cbx_refresh = QtWidgets.QCheckBox(self.gb_control)
        self.cbx_refresh.setObjectName("cbx_refresh")
        self.verticalLayout.addWidget(self.cbx_refresh)
        self.cbx_write = QtWidgets.QCheckBox(self.gb_control)
        self.cbx_write.setObjectName("cbx_write")
        self.verticalLayout.addWidget(self.cbx_write)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.gb_control, 0, 1, 2, 1)

        self.retranslateUi(wid_debugcontrol)
        QtCore.QMetaObject.connectSlotsByName(wid_debugcontrol)

    def retranslateUi(self, wid_debugcontrol):
        _translate = QtCore.QCoreApplication.translate
        self.gb_devices.setTitle(_translate("wid_debugcontrol", "Revolution Pi devices"))
        self.cbx_stay_on_top.setText(_translate("wid_debugcontrol", "Open to stay on top"))
        self.gb_control.setTitle(_translate("wid_debugcontrol", "IO Control"))
        self.btn_read_io.setToolTip(_translate("wid_debugcontrol", "Read all IO values and discard local changes (F4)"))
        self.btn_read_io.setText(_translate("wid_debugcontrol", "Read &all IO values"))
        self.btn_read_io.setShortcut(_translate("wid_debugcontrol", "F4"))
        self.btn_refresh_io.setToolTip(_translate("wid_debugcontrol", "Refresh all IO values which are locally not changed (F5)"))
        self.btn_refresh_io.setText(_translate("wid_debugcontrol", "&Refresh unchanged IOs"))
        self.btn_refresh_io.setShortcut(_translate("wid_debugcontrol", "F5"))
        self.btn_write_o.setToolTip(_translate("wid_debugcontrol", "Write locally changed output values to process image (F6)"))
        self.btn_write_o.setText(_translate("wid_debugcontrol", "&Write changed outputs"))
        self.btn_write_o.setShortcut(_translate("wid_debugcontrol", "F6"))
        self.cbx_refresh.setText(_translate("wid_debugcontrol", "&Auto refresh values"))
        self.cbx_write.setText(_translate("wid_debugcontrol", "and write outputs"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wid_debugcontrol = QtWidgets.QWidget()
    ui = Ui_wid_debugcontrol()
    ui.setupUi(wid_debugcontrol)
    wid_debugcontrol.show()
    sys.exit(app.exec_())
