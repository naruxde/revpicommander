# -*- coding: utf-8 -*-
"""Revolution Pi search with zeroconf."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

import webbrowser
from logging import getLogger
from re import compile
from sys import platform

from PyQt5 import QtCore, QtGui, QtWidgets
from zeroconf import IPVersion, ServiceBrowser, Zeroconf

from . import helper
from .helper import RevPiSettings, WidgetData, all_revpi_settings
from .ui.avahisearch_ui import Ui_diag_search

log = getLogger(__name__)


class AvahiSearchThread(QtCore.QThread):
    """Search thread for Revolution Pi with installed RevPiPyLoad."""
    added = QtCore.pyqtSignal(str, str, int, str, str)
    removed = QtCore.pyqtSignal(str, str)
    updated = QtCore.pyqtSignal(str, str, int, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cycle_wait_ms = 1000

        self.re_posix = compile(
            r"(?P<ip>(\d{1,3}\.){3}\d{1,3}).*"
            r"(?P<mac>([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})"
        )

    def remove_service(self, zeroconf: Zeroconf, conf_type: str, name: str) -> None:
        """Revolution Pi disappeared."""
        log.debug("AvahiSearchThread.remove_service")
        self.removed.emit(name, conf_type)

    def add_service(self, zeroconf: Zeroconf, conf_type: str, name: str) -> None:
        """New Revolution Pi found."""
        log.debug("AvahiSearchThread.add_service")
        info = zeroconf.get_service_info(conf_type, name)
        if not info:
            return

        for ip in info.parsed_addresses(IPVersion.V4Only):
            self.added.emit(name, info.server, info.port, conf_type, ip)

    def update_service(self, zeroconf: Zeroconf, conf_type: str, name: str) -> None:
        """New data of revolution pi"""
        log.debug("AvahiSearchThread.add_service")
        info = zeroconf.get_service_info(conf_type, name)
        if not info:
            return

        for ip in info.parsed_addresses(IPVersion.V4Only):
            self.updated.emit(name, info.server, info.port, conf_type, ip)

    def run(self) -> None:
        log.debug("Started zero conf discovery.")
        zeroconf = Zeroconf()
        revpi_browser = ServiceBrowser(zeroconf, "_revpipyload._tcp.local.", self)
        while not self.isInterruptionRequested():
            # Just hanging around :)
            self.msleep(self._cycle_wait_ms)
        zeroconf.close()
        log.debug("Stopped zero conf discovery.")


class AvahiSearch(QtWidgets.QDialog, Ui_diag_search):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Global variables to let parent decide other actions
        self.connect_settings = None
        self.just_save = False

        # Local variables
        self.clipboard = QtGui.QGuiApplication.clipboard()
        self._th_zero_conf = AvahiSearchThread(self)

        self.tb_revpi.setColumnWidth(0, 250)
        self.btn_connect.setEnabled(False)
        self.btn_save.setEnabled(False)

        self.restoreGeometry(helper.settings.value("avahisearch/geo", b''))
        column_sizes = helper.settings.value("avahisearch/column_sizes", [], type=list)
        if len(column_sizes) == self.tb_revpi.columnCount():
            for i in range(self.tb_revpi.columnCount()):
                self.tb_revpi.setColumnWidth(i, int(column_sizes[i]))

        # Global context menus
        self.cm_connect_actions = QtWidgets.QMenu(self)
        self.cm_connect_actions.addAction(self.act_connect_ssh)
        self.cm_connect_actions.addAction(self.act_connect_xmlrpc)

        self.cm_quick_actions = QtWidgets.QMenu(self)
        self.cm_quick_actions.addAction(self.act_connect)
        self.cm_quick_actions.addAction(self.act_connect_ssh)
        self.cm_quick_actions.addAction(self.act_connect_xmlrpc)
        self.cm_quick_actions.addSeparator()
        self.cm_quick_actions.addAction(self.act_open_pictory)
        self.cm_quick_actions.addSeparator()
        self.cm_quick_actions.addAction(self.act_copy_host)
        self.cm_quick_actions.addAction(self.act_copy_ip)

        self.tb_revpi.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tb_revpi.customContextMenuRequested.connect(self._cm_quick_exec)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def _cm_quick_exec(self, position: QtCore.QPoint) -> None:
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]

        revpi_settings = bool(item.data(WidgetData.revpi_settings))
        self.act_connect.setVisible(revpi_settings)
        self.act_connect_ssh.setVisible(not revpi_settings)
        self.act_connect_xmlrpc.setVisible(not revpi_settings)

        sender = self.sender()
        self.cm_quick_actions.exec(sender.mapToGlobal(position))

        self.act_connect.setVisible(True)
        self.act_connect_ssh.setVisible(True)
        self.act_connect_xmlrpc.setVisible(True)

    @staticmethod
    def _find_settings(address: str):
        """Find all settings with known avahi_id."""
        return [
            revpi_setting
            for revpi_setting in all_revpi_settings()
            if revpi_setting.address.lower() == address.lower()
        ]

    def _restart_search(self) -> None:
        """Clean up and restart search thread."""
        while self.tb_revpi.rowCount() > 0:
            # Remove each row, a .clean would destroy the columns
            self.tb_revpi.removeRow(0)

        self._th_zero_conf.requestInterruption()

        self._th_zero_conf = AvahiSearchThread(self)
        self._th_zero_conf.added.connect(self.on_avahi_added)
        self._th_zero_conf.updated.connect(self.on_avahi_added)
        self._th_zero_conf.removed.connect(self.on_avahi_removed)
        self._th_zero_conf.start()

    def _create_settings_object(self, row: int, ssh_tunnel: bool) -> RevPiSettings or None:
        """
        Create settings object from given row to settings.

        :param row: Row with connection data
        :param ssh_tunnel: Save as SSH tunnel connection
        :return: RevPi settings with data from avahi search and default values
        """
        item = self.tb_revpi.item(row, 0)
        if not item:
            return None

        settings = RevPiSettings()
        settings.folder = self.tr("Auto discovered")
        settings.name = item.data(WidgetData.host_name)
        settings.address = item.data(WidgetData.address)
        settings.port = item.data(WidgetData.port)
        settings.ssh_use_tunnel = ssh_tunnel

        return settings

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        helper.settings.setValue("avahisearch/geo", self.saveGeometry())
        helper.settings.setValue("avahisearch/column_sizes", [
            self.tb_revpi.columnWidth(i)
            for i in range(self.tb_revpi.columnCount())
        ])

    def exec(self) -> int:
        self.connect_settings = None
        self.just_save = False
        self._restart_search()
        rc = super().exec()
        self._th_zero_conf.requestInterruption()
        return rc

    @QtCore.pyqtSlot()
    def on_act_connect_triggered(self) -> None:
        """Connect via existing settings or ask for type."""
        log.debug("AvahiSearch.on_act_connect_triggered")
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]

        revpi_settings = item.data(WidgetData.revpi_settings)  # type: RevPiSettings
        if not revpi_settings:
            return
        self.connect_settings = revpi_settings
        self.accept()

    @QtCore.pyqtSlot()
    def on_act_connect_ssh_triggered(self) -> None:
        """Create new revpi settings with ssh, save and connect."""
        log.debug("AvahiSearch.on_act_connect_ssh_triggered")
        if self.tb_revpi.currentRow() == -1:
            return

        revpi_settings = self._create_settings_object(self.tb_revpi.currentRow(), True)
        revpi_settings.save_settings()
        self.connect_settings = revpi_settings
        self.accept()

    @QtCore.pyqtSlot()
    def on_act_connect_xmlrpc_triggered(self) -> None:
        """Create new revpi settings with XML-RPC, save and connect."""
        log.debug("AvahiSearch.on_act_connect_xmlrpc_triggered")
        if self.tb_revpi.currentRow() == -1:
            return

        revpi_settings = self._create_settings_object(self.tb_revpi.currentRow(), False)
        revpi_settings.save_settings()
        self.connect_settings = revpi_settings
        self.accept()

    @QtCore.pyqtSlot()
    def on_act_copy_host_triggered(self) -> None:
        """Copy hostname of selected item to clipboard."""
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]

        # Use just the hostname on Windows systems, it can not resolve .local addresses
        self.clipboard.setText(
            item.data(WidgetData.host_name) if platform == "win32"
            else item.data(WidgetData.host_name_full)
        )

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

        # We should use the hostname on macOS to let safari connect in link local mode (for linux nice too)
        webbrowser.open("http://{0}/".format(item.data(
            WidgetData.address if platform == "win32"
            else WidgetData.host_name_full
        )))

    @QtCore.pyqtSlot(str, str, int, str, str)
    def on_avahi_added(self, avahi_id: str, server: str, port: int, conf_type: str, ip: str) -> None:
        """New Revolution Pi found."""

        def update_tb_revpi_row(row_index: int):
            host_name_full = server[:-1]
            host_name = host_name_full[:host_name_full.find(".")]

            item_name = self.tb_revpi.item(row_index, 0)
            item_name.setData(WidgetData.address, ip)
            item_name.setData(WidgetData.port, port)
            item_name.setData(WidgetData.host_name_full, host_name_full)
            item_name.setData(WidgetData.host_name, host_name)

            revpi_settings = item_name.data(WidgetData.revpi_settings)  # type: RevPiSettings
            if revpi_settings:
                # Generate the name of saved revpi and show the avahi-name in brackets
                settings_text = "{0}/{1}".format(revpi_settings.folder, revpi_settings.name) \
                    if revpi_settings.folder \
                    else revpi_settings.name
                if revpi_settings.ssh_use_tunnel:
                    settings_text += self.tr(" over SSH")
                item_name.setText("{0} ({1})".format(settings_text, host_name))
            else:
                item_name.setText(host_name)
            item_name.setToolTip(item_name.text())

            item_ip = self.tb_revpi.item(row_index, 1)
            item_ip.setText(ip)
            item_ip.setToolTip(item_name.text())

        lst_existing = self._find_settings(ip)

        exists = False
        for i in range(self.tb_revpi.rowCount()):
            item_tb_revpi = self.tb_revpi.item(i, 0)
            if item_tb_revpi.data(WidgetData.object_name) == avahi_id:
                # Object already discovered
                update_tb_revpi_row(i)
                exists = True

        if not exists:
            for known_settings in lst_existing or [None]:
                item_name = QtWidgets.QTableWidgetItem()

                item_name.setIcon(QtGui.QIcon(":/main/ico/cpu.ico"))
                item_name.setData(WidgetData.object_name, avahi_id)
                item_name.setData(WidgetData.revpi_settings, known_settings)

                index = self.tb_revpi.rowCount()
                self.tb_revpi.insertRow(index)
                self.tb_revpi.setItem(index, 0, item_name)
                self.tb_revpi.setItem(index, 1, QtWidgets.QTableWidgetItem())

                update_tb_revpi_row(index)

    @QtCore.pyqtSlot(str, str)
    def on_avahi_removed(self, avahi_id: str, conf_type: str) -> None:
        """Revolution Pi disappeared."""
        for i in range(self.tb_revpi.rowCount()):
            if self.tb_revpi.item(i, 0).data(WidgetData.object_name) == avahi_id:
                self.tb_revpi.removeRow(i)
                break

    @QtCore.pyqtSlot(int, int)
    def on_tb_revpi_cellDoubleClicked(self, row: int, column: int) -> None:
        """Connect to double-clicked Revolution Pi."""
        log.debug("AvahiSearch.on_tb_revpi_cellDoubleClicked")
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]

        revpi_settings = bool(item.data(WidgetData.revpi_settings))
        if revpi_settings:
            self.act_connect.trigger()
        else:
            cur = QtGui.QCursor()
            self.cm_connect_actions.exec(cur.pos())

    @QtCore.pyqtSlot(int, int, int, int)
    def on_tb_revpi_currentCellChanged(self, row: int, column: int, last_row: int, last_column: int) -> None:
        """Manage state of buttons."""
        self.btn_connect.setEnabled(row >= 0)
        self.btn_save.setEnabled(row >= 0)

    @QtCore.pyqtSlot()
    def on_btn_connect_clicked(self) -> None:
        """Connect to selected Revolution Pi."""
        log.debug("AvahiSearch.on_btn_connect_clicked")
        selected_items = self.tb_revpi.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]

        revpi_settings = bool(item.data(WidgetData.revpi_settings))
        if revpi_settings:
            self.act_connect.trigger()
        else:
            pos_context_menu = self.btn_connect.pos()
            pos_context_menu.setY(pos_context_menu.y() + self.btn_connect.height())
            self.cm_connect_actions.exec(self.mapToGlobal(pos_context_menu))

    @QtCore.pyqtSlot()
    def on_btn_save_clicked(self) -> None:
        """Save selected Revolution Pi."""
        log.debug("AvahiSearch.on_btn_save_clicked")
        row_index = self.tb_revpi.currentRow()
        if row_index == -1:
            return
        self.connect_settings = self._create_settings_object(row_index, True)
        self.just_save = True
        self.accept()

    @QtCore.pyqtSlot()
    def on_btn_restart_clicked(self) -> None:
        """Clean up and restart search thread."""
        self._restart_search()
