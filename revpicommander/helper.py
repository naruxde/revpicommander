# -*- coding: utf-8 -*-
"""Helper functions for this application."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2020 Sven Sager"
__license__ = "GPLv3"

import pickle
import socket
from enum import IntEnum
from http.client import CannotSendRequest
from os import environ, remove
from os.path import exists
from queue import Queue
from threading import Lock
from xmlrpc.client import Binary, ServerProxy

from PyQt5 import QtCore

import proginit as pi


class WidgetData(IntEnum):
    address = 260
    replace_ios_config = 261
    acl_level = 262
    has_error = 263
    port = 264
    object_name = 265
    timeout = 266
    last_dir_upload = 301
    last_file_upload = 302
    last_dir_pictory = 303
    last_dir_picontrol = 304
    last_dir_selected = 305
    last_pictory_file = 306
    last_tar_file = 307
    last_zip_file = 308
    file_name = 309
    watch_files = 310
    watch_path = 311
    debug_geos = 312


class ConnectionManager(QtCore.QThread):
    """Check connection and status for PLC program on Revolution Pi."""

    connection_established = QtCore.pyqtSignal()
    """New connection established successfully with <class 'ServerProxy'>."""
    connection_disconnected = QtCore.pyqtSignal()
    """Connection disconnected."""
    connection_disconnecting = QtCore.pyqtSignal()
    """Signal emitted before closing connection."""
    connection_error_observed = QtCore.pyqtSignal(str)
    """This will be triggered, if a connection error was detected."""
    status_changed = QtCore.pyqtSignal(str, str)
    """Status message and color suggestion."""

    def __init__(self, parent=None, cycle_time_ms=1000):
        super(ConnectionManager, self).__init__(parent)

        self._cli = None
        self._cli_connect = Queue()
        self._cycle_time = cycle_time_ms
        self._lck_cli = Lock()
        self._ps_started = False
        self._revpi = None
        self._revpi_output = None

        self.address = ""
        self.name = ""
        self.port = 55123

        # Sync this with revpiplclist to preserve settings
        self.program_last_dir_upload = ""
        self.program_last_file_upload = ""
        self.program_last_dir_pictory = ""
        self.program_last_dir_picontrol = ""
        self.program_last_dir_selected = ""
        self.program_last_pictory_file = ""
        self.program_last_tar_file = ""
        self.program_last_zip_file = ""
        self.develop_watch_files = []
        self.develop_watch_path = ""
        self.debug_geos = {}

        self.pyload_version = (0, 0, 0)
        """Version number of RevPiPyLoad 0.0.0 with <class 'int'> values."""
        self.xml_funcs = []
        """Name list of all supported functions of RevPiPyLoad."""
        self.xml_mode = -1
        """ACL level for this connection (-1 on connection denied)."""
        self._xml_mode_refresh = False

    def __call_simulator(self, function_name: str, *args, default_value=None, **kwargs):
        pi.logger.debug("ConnectionManager.__call_simulator({0})".format(function_name))
        if function_name == "ps_values":
            if self._revpi.readprocimg():
                bytebuff = bytearray()
                for dev in self._revpi.device:
                    bytebuff += bytes(dev)
                return Binary(bytes(bytebuff))

        elif function_name == "ps_setvalue":
            # args: 0=device, 1=io, 2=value
            device = args[0]
            io = args[1]
            if type(args[2]) == Binary:
                value = args[2].data
            else:
                value = args[2]

            try:
                # Write new value to IO
                self._revpi.io[io].set_value(value)
            except Exception as e:
                return [device, io, False, str(e)]

            return [device, io, True, ""]

        elif function_name == "psstart":
            self._revpi.autorefresh_all()
            return True

        elif function_name == "psstop":
            self._revpi.exit(full=False)
            return True

        elif function_name == "ps_devices":
            return [(dev.position, dev.name) for dev in self._revpi.device]

        elif function_name == "ps_inps":
            return self.__simulator_ios("inp")

        elif function_name == "ps_outs":
            return self.__simulator_ios("out")

        else:
            return default_value

    def __simulator_ios(self, iotype: str):
        dict_ios = {}
        for dev in self._revpi.device:
            dict_ios[dev.position] = []

            if iotype == "inp":
                lst_io = dev.get_inputs()
            elif iotype == "out":
                lst_io = dev.get_outputs()
            else:
                lst_io = []

            for io in lst_io:
                dict_ios[dev.position].append([
                    io.name,
                    1 if io._bitlength == 1 else int(io._bitlength / 8),
                    io._slc_address.start + dev.offset,
                    io.bmk,
                    io._bitaddress,
                    io._byteorder,
                    io._signed,
                ])
        return Binary(pickle.dumps(dict_ios))

    def _clear_settings(self):
        """Clear connection settings."""
        self.address = ""
        self.name = ""
        self.port = 55123
        self.pyload_version = (0, 0, 0)
        self.xml_funcs.clear()
        self.xml_mode = -1

        self.program_last_dir_upload = ""
        self.program_last_file_upload = ""
        self.program_last_dir_pictory = ""
        self.program_last_dir_picontrol = ""
        self.program_last_dir_selected = ""
        self.program_last_pictory_file = ""
        self.program_last_tar_file = ""
        self.program_last_zip_file = ""
        self.develop_watch_files = []
        self.develop_watch_path = ""
        self.debug_geos = {}

    def _save_settings(self):
        """Save settings to named Revolution Pi."""
        for i in range(settings.beginReadArray("connections")):
            settings.setArrayIndex(i)
            if settings.value("address") != self.address:
                # Search used connection, because connection manager could reorganize array
                continue

            settings.setValue("last_dir_upload", self.program_last_dir_upload)
            settings.setValue("last_file_upload", self.program_last_file_upload)
            settings.setValue("last_dir_pictory", self.program_last_dir_pictory)
            settings.setValue("last_dir_picontrol", self.program_last_dir_picontrol)
            settings.setValue("last_dir_selected", self.program_last_dir_selected)
            settings.setValue("last_pictory_file", self.program_last_pictory_file)
            settings.setValue("last_tar_file", self.program_last_tar_file)
            settings.setValue("last_zip_file", self.program_last_zip_file)
            settings.setValue("watch_files", self.develop_watch_files)
            settings.setValue("watch_path", self.develop_watch_path)
            settings.setValue("debug_geos", self.debug_geos)

            break

        settings.endArray()

    def pyload_connect(self, settings_index: int):
        """
        Create a new connection from settings object.

        :param settings_index: Index of settings array 'connections'
        :return: True, if the connection was successfully established
        """

        # First disconnect to send signal and clean up values
        self.pyload_disconnect()

        settings.beginReadArray("connections")
        settings.setArrayIndex(settings_index)

        address = settings.value("address", str)
        name = settings.value("name", str)
        port = settings.value("port", 55123, int)
        timeout = settings.value("timeout", 5, int)

        self.program_last_dir_upload = settings.value("last_dir_upload", ".", str)
        self.program_last_file_upload = settings.value("last_file_upload", ".", str)
        self.program_last_dir_pictory = settings.value("last_dir_pictory", ".", str)
        self.program_last_dir_picontrol = settings.value("last_dir_picontrol", ".", str)
        self.program_last_dir_selected = settings.value("last_dir_selected", ".", str)
        self.program_last_pictory_file = settings.value("last_pictory_file", "{0}.rsc".format(name), str)
        self.program_last_tar_file = settings.value("last_tar_file", "{0}.tgz".format(name), str)
        self.program_last_zip_file = settings.value("last_zip_file", "{0}.zip".format(name), str)
        self.develop_watch_files = settings.value("watch_files", [], list)
        self.develop_watch_path = settings.value("watch_path", "", str)
        self.debug_geos = settings.value("debug_geos", {}, dict)

        settings.endArray()

        socket.setdefaulttimeout(2)
        sp = ServerProxy("http://{0}:{1}".format(address, port))

        # Load values and test connection to Revolution Pi
        try:
            pyload_version = tuple(map(int, sp.version().split(".")))
            xml_funcs = sp.system.listMethods()
            xml_mode = sp.xmlmodus()
        except Exception as e:
            pi.logger.exception(e)
            self.connection_error_observed.emit(str(e))
            return False

        self.address = address
        self.name = name
        self.port = port
        self.pyload_version = pyload_version
        self.xml_funcs = xml_funcs
        self.xml_mode = xml_mode

        with self._lck_cli:
            socket.setdefaulttimeout(timeout)
            self._cli = sp
            self._cli_connect.put_nowait((address, port))

        self.connection_established.emit()

        return True

    def pyload_disconnect(self):
        """Disconnect from Revolution Pi."""
        if self._revpi is not None:
            self.connection_disconnecting.emit()

            self._revpi.cleanup()
            self._revpi_output.cleanup()
            if settings.value("simulator/stop_remove", False, bool):
                remove(self._revpi.procimg)
            self._revpi = None
            self._revpi_output = None

            pi.logger.debug("Simulator destroyed.")
            self.connection_disconnected.emit()

        elif self._cli is not None:

            # Tell all widget, that we want do disconnect, to save the settings
            self.connection_disconnecting.emit()
            self._save_settings()

            with self._lck_cli:
                if self._ps_started:
                    try:
                        self._cli.psstop()
                    except Exception:
                        pass
                self._clear_settings()
                self._cli = None

            self.connection_disconnected.emit()

    def pyload_simulate(self, configrsc: str, procimg: str, clean_existing: bool):
        """Start the simulator for piControl on local computer."""
        pi.logger.debug("ConnectionManager.start_simulate")

        if not exists(procimg) or clean_existing:
            with open(procimg, "wb") as fh:
                fh.write(b'\x00' * 4096)

        try:
            import revpimodio2

            # Prepare process image with default values for outputs
            self._revpi_output = revpimodio2.RevPiModIO(configrsc=configrsc, procimg=procimg)
            self._revpi_output.setdefaultvalues()
            self._revpi_output.writeprocimg()

            # This is our simulator to work with
            self._revpi = revpimodio2.RevPiModIO(simulator=True, configrsc=configrsc, procimg=procimg)
            self._revpi.setdefaultvalues()
            self._revpi.writeprocimg()

            self.xml_funcs = ["psstart", "psstop", "ps_devices", "ps_inps", "ps_outs", "ps_values", "ps_setvalue"]

            self.connection_established.emit()

        except Exception as e:
            pi.logger.exception(e)
            self.connection_error_observed.emit(str(e))
            self._revpi_output = None
            self._revpi = None
            if settings.value("simulator/stop_remove", False, bool):
                remove(procimg)

        return self._revpi is not None

    def refresh_xml_mode(self):
        """Refresh XML ACL level after some change could be done."""
        self._xml_mode_refresh = True

    def reset_simulator(self):
        """Reset all io to piCtory defaults."""
        pi.logger.debug("ConnectionManager.reset_simulator")
        if settings.value("simulator/restart_zero", False, bool):
            with open(self._revpi.procimg, "wb") as fh:
                fh.write(b'\x00' * 4096)
            self._revpi.readprocimg()
        else:
            self._revpi_output.writeprocimg()
            self._revpi.setdefaultvalues()
            self._revpi.writeprocimg()

    def run(self):
        """Thread worker to check status of RevPiPyLoad."""
        self.setPriority(QtCore.QThread.NormalPriority)

        sp = None
        while not self.isInterruptionRequested():

            if self._revpi is not None:
                sp = None
                self.status_changed.emit("SIMULATING", "yellow")
            elif self._cli is None:
                sp = None
                self.status_changed.emit("NOT CONNECTED", "lightblue")
            elif not self._cli_connect.empty():
                # Get new connection information to create object in this thread
                item = self._cli_connect.get()
                sp = ServerProxy("http://{0}:{1}".format(*item))
                self._cli_connect.task_done()

            if sp:
                try:
                    plc_exit_code = sp.plcexitcode()
                    if self._xml_mode_refresh:
                        self.xml_mode = sp.xmlmodus()
                        self._xml_mode_refresh = False
                except CannotSendRequest as e:
                    pi.logger.warning(e)
                except Exception as e:
                    pi.logger.warning(e)
                    self.status_changed.emit("SERVER ERROR", "red")
                    self.connection_error_observed.emit("{0} | {1}".format(e, type(e)))
                else:
                    if plc_exit_code == -1:
                        self.status_changed.emit("RUNNING", "green")
                    elif plc_exit_code == -2:
                        self.status_changed.emit("FILE NOT FOUND", "red")
                    elif plc_exit_code == -3:
                        self.status_changed.emit("NOT RUNNING (NO STATUS)", "yellow")
                    elif plc_exit_code == -9:
                        self.status_changed.emit("PROGRAM KILLED", "red")
                    elif plc_exit_code == -15:
                        self.status_changed.emit("PROGRAM TERMED", "red")
                    elif plc_exit_code == 0:
                        self.status_changed.emit("NOT RUNNING", "yellow")
                    else:
                        self.status_changed.emit("FINISHED WITH CODE {0}".format(plc_exit_code), "yellow")

            self.msleep(self._cycle_time)

    def call_remote_function(self, function_name: str, *args, default_value=None, raise_exception=False, **kwargs):
        """
        Save call of a remote function with given name and parameters on Revolution Pi.

        :param function_name: Function to call on RevPiPyLoad
        :param args: Functions arguments
        :param default_value: Default value will be returned on error
        :param raise_exception: Will raise the exception returned from server
        :param kwargs: Functions key word arguments
        :return: Return value of remote function or default_value
        """
        if self._cli is None and self._revpi is None:
            pi.logger.error("Not connected while calling {0}".format(function_name))
            if raise_exception:
                raise ConnectionError("Connection manager not connected")
            return default_value

        reload_funcs = False
        if function_name == "psstart":
            self._ps_started = True
            reload_funcs = True
        elif function_name == "psstop":
            self._ps_started = False
            reload_funcs = True

        # On connection problems do not freeze
        if self._lck_cli.acquire(timeout=1.0):
            if self._revpi is not None:
                # Redirect call to simulator
                return_value = self.__call_simulator(function_name, *args, default_value=default_value, **kwargs)
            else:
                try:
                    return_value = getattr(self._cli, function_name)(*args, **kwargs)
                    if reload_funcs:
                        self.xml_funcs = self._cli.system.listMethods()
                except Exception as e:
                    pi.logger.error(e)
                    if raise_exception:
                        self._lck_cli.release()
                        raise
                    return_value = default_value

            self._lck_cli.release()
            return return_value

        elif raise_exception:
            raise ConnectionError("Can not get lock of connection")

        return default_value

    def get_cli(self):
        """Connection proxy of actual connection."""
        if self.address and self.port:
            return ServerProxy("http://{0}:{1}".format(self.address, self.port))
        else:
            return None

    @property
    def connected(self) -> bool:
        """True if we have an active connection."""
        return self._cli is not None

    @property
    def simulating(self) -> bool:
        """True, if simulating mode is running."""
        return self._revpi is not None

    @property
    def simulating_configrsc(self) -> str:
        return self._revpi.configrsc if self._revpi else ""

    @property
    def simulating_procimg(self) -> str:
        return self._revpi.procimg if self._revpi else ""


cm = ConnectionManager()
"""Clobal connection manager instance."""

settings = QtCore.QSettings("revpipyplc", "revpipyload")
"""Global application settings."""

homedir = environ.get("HOME", "") or environ.get("APPDATA", "")
"""Home dir of user."""
