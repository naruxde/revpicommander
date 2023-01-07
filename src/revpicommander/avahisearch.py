# -*- coding: utf-8 -*-
"""Revolution Pi search with zeroconf."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

import webbrowser
from os import name as osname
from re import compile
from sys import platform

from PyQt5 import QtCore, QtGui, QtWidgets
from zeroconf import IPVersion, ServiceBrowser, Zeroconf

from . import proginit as pi
from .helper import WidgetData, settings
from .ui.avahisearch_ui import Ui_diag_search


def find_settings_index(address: str, port: int) -> int:
    """
    Search index of saved settings.

    :param address: Host or IP address of Revolution Pi
    :param port: Port to connect
    :return: Index of settings array or -1, if not found
    """
    settings_index = -1
    for i in range(settings.beginReadArray("connections")):
        settings.setArrayIndex(i)

        _address = settings.value("address", type=str)
        _port = settings.value("port", type=int)
        if address.lower() == _address.lower() and port == _port:
            settings_index = i
            break

    settings.endArray()
    return settings_index


class AvahiSearchThread(QtCore.QThread):
    """Search thread for Revolution Pi with installed RevPiPyLoad."""
    added = QtCore.pyqtSignal(str, str, int, str, str)
    removed = QtCore.pyqtSignal(str, str)
    updated = QtCore.pyqtSignal(str, str, int, str, str)

    def __init__(self, parent=None):
        super(AvahiSearchThread, self).__init__(parent)
        self._cycle_wait_ms = 1000

        self.__dict_arp = {}
        self.re_posix = compile(
            r"(?P<ip>(\d{1,3}\.){3}\d{1,3}).*"
            r"(?P<mac>([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})"
        )

    def _update_arp(self) -> None:
        """Find mac address in arp table."""
        if osname == "posix":
            with open("/proc/net/arp") as fh:
                for line in fh.readlines():
                    ip_mac = self.re_posix.search(line)
                    if ip_mac:
                        self.__dict_arp[ip_mac.group("ip")] = ip_mac.group("mac")

    def get_mac(self, ip: str) -> dict:
        """
        Get mac address of ip, if known.

        :param ip: IP address to find mac address
        :return: MAC address as string or empty string, if unknown
        """
        return self.__dict_arp.get(ip, "")

    def remove_service(self, zeroconf: Zeroconf, conf_type: str, name: str) -> None:
        """Revolution Pi disappeared."""
        pi.logger.debug("AvahiSearchThread.remove_service")
        self.removed.emit(name, conf_type)

    def add_service(self, zeroconf: Zeroconf, conf_type: str, name: str) -> None:
        """New Revolution Pi found."""
        pi.logger.debug("AvahiSearchThread.add_service")
        info = zeroconf.get_service_info(conf_type, name)
        if not info:
            return

        for ip in info.parsed_addresses(IPVersion.V4Only):
            self.added.emit(name, info.server, info.port, conf_type, ip)

    def update_service(self, zeroconf: Zeroconf, conf_type: str, name: str) -> None:
        """New data of revolution pi"""
        pi.logger.debug("AvahiSearchThread.add_service")
        info = zeroconf.get_service_info(conf_type, name)
        if not info:
            return

        for ip in info.parsed_addresses(IPVersion.V4Only):
            self.updated.emit(name, info.server, info.port, conf_type, ip)

    def run(self) -> None:
        pi.logger.debug("Started zero conf discovery.")
        zeroconf = Zeroconf()
        revpi_browser = ServiceBrowser(zeroconf, "_revpipyload._tcp.local.", self)
        while not self.isInterruptionRequested():
            # Just hanging around :)
            self.msleep(self._cycle_wait_ms)
        zeroconf.close()
        pi.logger.debug("Stopped zero conf discovery.")


class AvahiSearch(QtWidgets.QDialog, Ui_diag_search):

    def __init__(self, parent=None):
        super(AvahiSearch, self).__init__(parent)
        self.setupUi(self)

        self.clipboard = QtGui.QGuiApplication.clipboard()
        self.connect_index = -1
        self.known_hosts = {}
        self.th_zero_conf = AvahiSearchThread(self)

        self.tb_revpi.setColumnWidth(0, 250)
        self.btn_connect.setEnabled(False)
        self.btn_save.setEnabled(False)

        self.restoreGeometry(settings.value("avahisearch/geo", b''))
        column_sizes = settings.value("avahisearch/column_sizes", [], type=list)
        if len(column_sizes) == self.tb_revpi.columnCount():
            for i in range(self.tb_revpi.columnCount()):
                self.tb_revpi.setColumnWidth(i, int(column_sizes[i]))

        # Global context menus
        self.cm_connect_actions = QtWidgets.QMenu(self)
        self.cm_connect_actions.addAction(self.act_connect_ssh)
        self.cm_connect_actions.addAction(self.act_connect_xmlrpc)

        self.cm_quick_actions = QtWidgets.QMenu(self)
        self.cm_quick_actions.addAction(self.act_open_pictory)
        self.cm_quick_actions.addSeparator()
        self.cm_quick_actions.addAction(self.act_copy_ip)
        self.cm_quick_actions.addAction(self.act_copy_host)
        self.cm_quick_actions.addSeparator()
        self.cm_quick_actions.addAction(self.act_connect_ssh)
        self.cm_quick_actions.addAction(self.act_connect_xmlrpc)

        self.tb_revpi.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tb_revpi.customContextMenuRequested.connect(self._cm_quick_exec)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def _cm_connect_exec(self, position: QtCore.QPoint) -> None:
        row = self.tb_revpi.currentRow()
        if row == -1:
            return

        item = self.tb_revpi.item(row, 0)
        settings_index = find_settings_index(item.data(WidgetData.address), item.data(WidgetData.port))
        if settings_index >= 0:
            self.connect_index = settings_index
            self.accept()
            return

        action = self.cm_connect_actions.exec(position)
        if action:
            action.trigger()

    @QtCore.pyqtSlot(QtCore.QPoint)
    def _cm_quick_exec(self, position: QtCore.QPoint) -> None:
        if self.tb_revpi.currentItem() is None:
            return

        sender = self.sender()
        action = self.cm_quick_actions.exec(sender.mapToGlobal(position))
        if action:
            action.trigger()

    def _load_known_hosts(self) -> None:
        """Load existing connections to show hostname of existing ip addresses"""
        self.known_hosts.clear()

        for i in range(settings.beginReadArray("connections")):
            settings.setArrayIndex(i)

            name = settings.value("name", type=str)
            folder = settings.value("folder", type=str)
            address = settings.value("address", type=str)
            self.known_hosts[address] = "{0}/{1}".format(folder, name) if folder else name

        settings.endArray()

    def _restart_search(self) -> None:
        """Clean up and restart search thread."""
        while self.tb_revpi.rowCount() > 0:
            self.tb_revpi.removeRow(0)
        self.th_zero_conf.requestInterruption()

        self.th_zero_conf = AvahiSearchThread(self)
        self.th_zero_conf.added.connect(self.on_avahi_added)
        self.th_zero_conf.updated.connect(self.on_avahi_added)
        self.th_zero_conf.removed.connect(self.on_avahi_removed)
        self.th_zero_conf.start()

    def _save_connection(self, row: int, ssh_tunnel: bool, no_warn=False) -> int:
        """
        Save the connection from given row to settings.

        :param row: Row with connection data
        :param ssh_tunnel: Save as SSH tunnel connection
        :param no_warn: If True, no message boxes will appear
        :return: Array index of connection (found or saved) or -1
        """
        item = self.tb_revpi.item(row, 0)
        if not item:
            return -1

        folder_name = self.tr("Auto discovered")
        selected_name = item.text()
        selected_address = item.data(WidgetData.address)
        selected_port = item.data(WidgetData.port)
        i = 0
        for i in range(settings.beginReadArray("connections")):
            settings.setArrayIndex(i)

            name = settings.value("name", type=str)
            address = settings.value("address", type=str)
            port = settings.value("port", type=int)
            if address.lower() == selected_address.lower() and port == selected_port:
                if not no_warn:
                    QtWidgets.QMessageBox.information(
                        self, self.tr("Already in list..."), self.tr(
                            "The selected Revolution Pi is already saved in your "
                            "connection list as '{0}'."
                        ).format(name)
                    )
                settings.endArray()
                return i

        settings.endArray()
        settings.beginWriteArray("connections")

        settings.setArrayIndex(i + 1)
        settings.setValue("address", selected_address)
        settings.setValue("folder", folder_name)
        settings.setValue("name", selected_name)
        settings.setValue("port", selected_port)

        settings.setValue("ssh_use_tunnel", ssh_tunnel)
        settings.setValue("ssh_port", 22)
        settings.setValue("ssh_user", "pi")

        settings.endArray()

        if not no_warn:
            QtWidgets.QMessageBox.information(
                self, self.tr("Success"), self.tr(
                    "The connection with the name '{0}' was successfully saved "
                    "to folder '{1}' in your connections."
                ).format(selected_name, folder_name)
            )

        return i + 1

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        settings.setValue("avahisearch/geo", self.saveGeometry())
        settings.setValue("avahisearch/column_sizes", [
            self.tb_revpi.columnWidth(i)
            for i in range(self.tb_revpi.columnCount())
        ])

    def exec(self) -> int:
        self._load_known_hosts()
        self._restart_search()
        rc = super(AvahiSearch, self).exec()
        self.th_zero_conf.requestInterruption()
        return rc

    @QtCore.pyqtSlot()
    def on_act_connect_ssh_triggered(self) -> None:
        """Copy ip address of selected item to clipboard."""
        pi.logger.debug("AvahiSearch.on_act_connect_ssh_triggered")
        if self.tb_revpi.currentRow() == -1:
            return
        self.connect_index = self._save_connection(self.tb_revpi.currentRow(), True, no_warn=True)
        self.accept()

    @QtCore.pyqtSlot()
    def on_act_connect_xmlrpc_triggered(self) -> None:
        """Copy ip address of selected item to clipboard."""
        pi.logger.debug("AvahiSearch.on_act_connect_xmlrpc_triggered")
        if self.tb_revpi.currentRow() == -1:
            return
        self.connect_index = self._save_connection(self.tb_revpi.currentRow(), False, no_warn=True)
        self.accept()

    @QtCore.pyqtSlot()
    def on_act_copy_host_triggered(self) -> None:
        """Copy ip address of selected item to clipboard."""
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
        host_name = item.data(WidgetData.host_name)
        if platform == "win32":
            # Strip hostname on Windows systems, it can not resolve .local addresses
            host_name = host_name[:host_name.find(".")]
        self.clipboard.setText(host_name)

    @QtCore.pyqtSlot()
    def on_act_copy_ip_triggered(self) -> None:
        """Copy ip address of selected item to clipboard."""
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
        self.clipboard.setText(item.data(WidgetData.address))

    @QtCore.pyqtSlot()
    def on_act_open_pictory_triggered(self) -> None:
        """Open piCtory in default browser of operating system."""
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
        if platform == "win32":
            webbrowser.open("http://{0}/".format(item.data(WidgetData.address)))
        else:
            webbrowser.open("http://{0}/".format(item.data(WidgetData.host_name)))

    @QtCore.pyqtSlot(str, str, int, str, str)
    def on_avahi_added(self, name: str, server: str, port: int, conf_type: str, ip: str) -> None:
        """New Revolution Pi found."""
        index = -1
        for i in range(self.tb_revpi.rowCount()):
            if self.tb_revpi.item(i, 0).data(WidgetData.object_name) == name:
                index = i
                break

        if index == -1:
            # New Row
            item_name = QtWidgets.QTableWidgetItem()
            item_ip = QtWidgets.QTableWidgetItem()

            index = self.tb_revpi.rowCount()
            self.tb_revpi.insertRow(index)
            self.tb_revpi.setItem(index, 0, item_name)
            self.tb_revpi.setItem(index, 1, item_ip)
        else:
            # Update row
            item_name = self.tb_revpi.item(index, 0)
            item_ip = self.tb_revpi.item(index, 1)

        host_name = server[:-1]
        item_name.setIcon(QtGui.QIcon(":/main/ico/cpu.ico"))
        if ip in self.known_hosts:
            item_name.setText("{0} ({1})".format(host_name, self.known_hosts[ip]))
        else:
            item_name.setText(host_name)
        item_name.setData(WidgetData.object_name, name)
        item_name.setData(WidgetData.address, ip)
        item_name.setData(WidgetData.port, port)
        item_name.setData(WidgetData.host_name, host_name)
        item_ip.setText(ip)

    @QtCore.pyqtSlot(str, str)
    def on_avahi_removed(self, name: str, conf_type: str) -> None:
        """Revolution Pi disappeared."""
        for i in range(self.tb_revpi.rowCount()):
            if self.tb_revpi.item(i, 0).data(WidgetData.object_name) == name:
                self.tb_revpi.removeRow(i)
                break

    @QtCore.pyqtSlot(int, int)
    def on_tb_revpi_cellDoubleClicked(self, row: int, column: int) -> None:
        """Connect to double-clicked Revolution Pi."""
        pi.logger.debug("AvahiSearch.on_tb_revpi_cellDoubleClicked")
        cur = QtGui.QCursor()
        self._cm_connect_exec(cur.pos())

    @QtCore.pyqtSlot(int, int, int, int)
    def on_tb_revpi_currentCellChanged(self, row: int, column: int, last_row: int, last_column: int) -> None:
        """Manage state of buttons."""
        self.btn_connect.setEnabled(row >= 0)
        self.btn_save.setEnabled(row >= 0)

    @QtCore.pyqtSlot()
    def on_btn_connect_clicked(self) -> None:
        """Connect to selected Revolution Pi."""
        pi.logger.debug("AvahiSearch.on_btn_connect_clicked")
        # Open context menu under the button
        pos = self.btn_connect.pos()
        pos.setY(pos.y() + self.btn_connect.height())
        self._cm_connect_exec(self.mapToGlobal(pos))

    @QtCore.pyqtSlot()
    def on_btn_save_clicked(self) -> None:
        """Save selected Revolution Pi."""
        pi.logger.debug("AvahiSearch.on_btn_save_clicked")
        if self.tb_revpi.currentRow() == -1:
            return
        self.connect_index = self._save_connection(self.tb_revpi.currentRow(), ssh_tunnel=True)

    @QtCore.pyqtSlot()
    def on_btn_restart_clicked(self) -> None:
        """Clean up and restart search thread."""
        self._restart_search()
