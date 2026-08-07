# -*- coding: utf-8 -*-
"""Helper functions for this application."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023-2026 Sven Sager"
__license__ = "GPLv2"

import pickle
import socket
from enum import IntEnum
from http.client import CannotSendRequest
from logging import getLogger
from os import environ, remove
from os.path import exists
from queue import Queue
from re import search
from threading import Lock
from uuid import uuid4
from xmlrpc.client import Binary, ServerProxy, Transport
from configparser import ConfigParser

from PyQt5 import QtCore
import asyncssh

from . import proginit as pi
from .ssh_tunneling.server import SSHLocalTunnel

log = getLogger(__name__)

settings = QtCore.QSettings("revpimodio.org", "revpicommander")
"""Global application settings."""

homedir = environ.get("HOME", "") or environ.get("APPDATA", "")
"""Home dir of user."""


class UnixStreamTransport(Transport):
    """Transport for xmlrpc to use unix domain sockets."""

    def __init__(self, socket_path):
        super().__init__()
        self._socket_path = socket_path

    def make_connection(self, host):
        import http.client
        conn = http.client.HTTPConnection("localhost")
        conn.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.sock.connect(self._socket_path)
        return conn


class ConnectionFail(IntEnum):
    NO_XML_RPC = 1
    SSH_CONNECT = 2
    SSH_AUTH = 4
    NO_XML_RPC_VIA_TUNNEL = 9  # Includes NO_XML_RPC Bit


class WidgetData(IntEnum):
    address = 260
    acl_level = 262
    has_error = 263
    port = 264
    object_name = 265
    host_name = 267
    host_name_full = 268
    file_name = 309
    is_plc_program = 310
    revpi_settings = 320


class RevPiSettings:

    def __init__(self, load_index: int = None, settings_storage: QtCore.QSettings = None):
        """
        Revolution Pi saved settings.

        :param load_index: Load settings from index, same as .load_from_index
        :param settings_storage: Change QSettings object to work on from default to this one
        """
        self._settings = settings_storage or settings
        self.internal_id = ""

        self.name = "New connection"
        self.folder = ""
        self.address = "127.0.0.1"
        self.port = 55123
        self.timeout = 5

        self.ssh_use_tunnel = True
        self.ssh_port = 22
        self.ssh_user = "pi"
        self.ssh_saved_password = False

        self.last_dir_upload = "."
        self.last_file_upload = "."
        self.last_dir_pictory = "."
        self.last_dir_picontrol = "."
        self.last_dir_selected = "."
        self.last_pictory_file = ""
        self.last_tar_file = ""
        self.last_zip_file = ""
        self.watch_files = []
        self.watch_path = ""

        self.debug_geos = {}

        if load_index is not None:
            self.load_from_index(load_index)

    @property
    def is_unix_socket(self) -> bool:
        """Check if connection is a unix domain socket."""
        return self.address.startswith("/") or self.address.startswith("./")

    def load_from_index(self, settings_index: int) -> None:
        """Load settings from 'connections' index."""
        self._settings.beginReadArray("connections")
        self._settings.setArrayIndex(settings_index)

        # Flag as "legacy" connection to generate missing internal_id on save_settings()
        self.internal_id = self._settings.value("internal_id", "legacy", type=str)

        self.name = self._settings.value("name", type=str)
        self.folder = self._settings.value("folder", "", type=str)
        self.address = self._settings.value("address", type=str)
        self.port = self._settings.value("port", 55123, type=int)
        self.timeout = self._settings.value("timeout", 5, type=int)

        self.ssh_use_tunnel = self._settings.value("ssh_use_tunnel", True, type=bool)
        self.ssh_port = self._settings.value("ssh_port", 22, type=int)
        self.ssh_user = self._settings.value("ssh_user", "pi", type=str)
        self.ssh_saved_password = self._settings.value("ssh_saved_password", False, type=bool)

        self.last_dir_upload = self._settings.value("last_dir_upload", ".", type=str)
        self.last_file_upload = self._settings.value("last_file_upload", ".", type=str)
        self.last_dir_pictory = self._settings.value("last_dir_pictory", ".", type=str)
        self.last_dir_picontrol = self._settings.value("last_dir_picontrol", ".", type=str)
        self.last_dir_selected = self._settings.value("last_dir_selected", ".", type=str)
        self.last_pictory_file = self._settings.value("last_pictory_file", "", type=str)
        self.last_tar_file = self._settings.value("last_tar_file", "", type=str)
        self.last_zip_file = self._settings.value("last_zip_file", "", type=str)
        self.watch_files = self._settings.value("watch_files", [], type=list)
        self.watch_path = self._settings.value("watch_path", "", type=str)

        try:
            # Bytes with QSettings are a little difficult sometimes
            self.debug_geos = self._settings.value("debug_geos", {}, type=dict)
        except Exception:
            # Just drop the geos of IO windows
            pass

        # These values must exists
        if not (self.name and self.address):
            raise ValueError("Could not get all required values from saved settings")

        if not self.is_unix_socket and not self.port:
            raise ValueError("Port is required for IP connections")

        self._settings.endArray()

    def save_settings(self):
        """Save all settings."""

        count_settings = self._settings.beginReadArray("connections")

        def create_new_array_member():
            """Insert a new setting at the end of the array."""

            # Close the active array action to reopen a write action to expand the array
            self._settings.endArray()
            self._settings.beginWriteArray("connections")
            self._settings.setArrayIndex(count_settings)

            if not self.internal_id:
                self.internal_id = uuid4().hex

        if not self.internal_id:
            create_new_array_member()

        else:
            # Always search setting in array, because connection manager could reorganize array indexes
            new_setting = True
            for index in range(count_settings):
                self._settings.setArrayIndex(index)

                if self.internal_id == "legacy":
                    # Legacy connection without internal_id
                    if self._settings.value("address") == self.address:
                        # Set missing internal_id
                        self.internal_id = uuid4().hex
                        new_setting = False
                        break
                else:
                    if self._settings.value("internal_id") == self.internal_id:
                        new_setting = False
                        break

            if new_setting:
                # On this point, we iterate all settings and found none, so create new one
                create_new_array_member()

        self._settings.setValue("internal_id", self.internal_id)
        self._settings.setValue("name", self.name)
        self._settings.setValue("folder", self.folder)
        self._settings.setValue("address", self.address)
        self._settings.setValue("port", self.port)
        self._settings.setValue("timeout", self.timeout)

        # Disable SSH tunnel if unix socket is used. SSH will check the type on the remove system
        self._settings.setValue("ssh_use_tunnel", self.ssh_use_tunnel and not self.is_unix_socket)
        self._settings.setValue("ssh_port", self.ssh_port)
        self._settings.setValue("ssh_user", self.ssh_user)
        self._settings.setValue("ssh_saved_password", self.ssh_saved_password)

        self._settings.setValue("last_dir_upload", self.last_dir_upload)
        self._settings.setValue("last_file_upload", self.last_file_upload)
        self._settings.setValue("last_dir_pictory", self.last_dir_pictory)
        self._settings.setValue("last_dir_picontrol", self.last_dir_picontrol)
        self._settings.setValue("last_dir_selected", self.last_dir_selected)
        self._settings.setValue("last_pictory_file", self.last_pictory_file)
        self._settings.setValue("last_tar_file", self.last_tar_file)
        self._settings.setValue("last_zip_file", self.last_zip_file)
        self._settings.setValue("watch_files", self.watch_files)
        self._settings.setValue("watch_path", self.watch_path)
        self._settings.setValue("debug_geos", self.debug_geos)

        self._settings.endArray()


class ConnectionManager(QtCore.QThread):
    """Check connection and status for PLC program on Revolution Pi."""

    connect_error = QtCore.pyqtSignal(str, str, ConnectionFail, RevPiSettings)
    """Error header, message and reason (ConnectionFail) of a new connection after pyload_connect call."""
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
    connection_recovered = QtCore.pyqtSignal()
    """After errors the connection is established again, could have other port information (SSH)."""

    def __init__(self, parent=None, cycle_time_ms=1000):
        super().__init__(parent)

        self._cli = None
        self._cli_connect = Queue()
        self._cycle_time = cycle_time_ms
        self._has_error = False
        self._lck_cli = Lock()
        self._ps_started = False
        self._revpi = None
        self._revpi_output = None

        self.settings = RevPiSettings()

        self.ssh_tunnel_server = None  # type: SSHLocalTunnel
        self.ssh_pass = ""

        self.pyload_version = (0, 0, 0)
        """Version number of RevPiPyLoad 0.0.0 with <class 'int'> values."""
        self.pyload_version_str = ""
        """Raw string of RevPyPyLoad version, could contain rc1 at the end."""
        self.xml_funcs = []
        """Name list of all supported functions of RevPiPyLoad."""
        self.xml_mode = -1
        """ACL level for this connection (-1 on connection denied)."""
        self._xml_mode_refresh = False

    def __call_simulator(self, function_name: str, *args, default_value=None, **kwargs):
        log.debug("ConnectionManager.__call_simulator({0})".format(function_name))
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
        self.settings = RevPiSettings()

        self.ssh_pass = ""

        self.pyload_version = (0, 0, 0)
        self.pyload_version_str = ""
        self.xml_funcs.clear()
        self.xml_mode = -1

    def pyload_connect(self, revpi_settings: RevPiSettings, ssh_pass="") -> bool:
        """
        Create a new connection from settings object.

        :param revpi_settings: Revolution Pi saved connection settings
        :param ssh_pass: Use this ssh password, if revpi_settings.ssh_use_tunnel is true
        :return: True, if the connection was successfully established
        """

        # First disconnect to send signal and clean up values
        self.pyload_disconnect()

        ssh_tunnel_server = None
        ssh_tunnel_port = 0
        ssh_tunnel_socket = None

        socket.setdefaulttimeout(revpi_settings.timeout)

        if revpi_settings.ssh_use_tunnel:
            # We first connect to find out which target to tunnel
            ssh_tunnel_server = SSHLocalTunnel(
                revpi_settings.port,
                revpi_settings.address,
                revpi_settings.ssh_port
            )
            try:
                ssh_tunnel_port = ssh_tunnel_server.connect_by_credentials(revpi_settings.ssh_user, ssh_pass)

                # Check for Unix socket on remote system
                try:
                    stdout, stderr, exit_code = ssh_tunnel_server.send_cmd("cat /etc/revpipyload/revpipyload.conf")
                    if stdout:
                        config = ConfigParser()
                        config.read_string(stdout)
                        if config.has_section("XMLRPC"):
                            bindip = config.get("XMLRPC", "bindip", fallback="").strip()
                            if bindip == "socket":
                                ssh_tunnel_socket = "/run/revpipyload/xmlrpc.socket"
                            elif bindip.startswith("/") or bindip.startswith("./"):
                                ssh_tunnel_socket = bindip

                        if ssh_tunnel_socket:
                            log.debug("Using remote unix socket: %s", ssh_tunnel_socket)
                            # Forward local port 0 (dynamic) to remote unix socket
                            ssh_tunnel_server.disconnect()
                            ssh_tunnel_server = SSHLocalTunnel(
                                ssh_tunnel_socket,
                                revpi_settings.address,
                                revpi_settings.ssh_port
                            )
                            ssh_tunnel_port = ssh_tunnel_server.connect_by_credentials(
                                revpi_settings.ssh_user, ssh_pass
                            )
                        else:
                            log.debug("Using remote TCP socket: %s", bindip)

                except Exception as e:
                    log.warning(f"Could not check remote config for unix socket: {e}")

                if getattr(revpi_settings, "ssh_enable_revpipyload", False):
                    cmd_activate_pyload = "systemctl enable --now revpipyload"

                    # Test sudo requires password authentication
                    _, _, exit_code = ssh_tunnel_server.send_cmd("sudo -n true")
                    if exit_code == 0:
                        # No password required
                        ssh_tunnel_server.send_cmd(f"sudo {cmd_activate_pyload}")
                    else:
                        # Execute command with sudo password
                        _, _, exit_code = ssh_tunnel_server.send_cmd(
                            f"sudo -S {cmd_activate_pyload}",
                            stdin=ssh_pass,
                        )
                        if exit_code != 0:
                            log.error(
                                "Sudo authentification failed for user %s",
                                revpi_settings.ssh_user,
                            )
                            self.connect_error.emit(
                                self.tr("Error"), self.tr(
                                    "Can not activate RevPiPyLoad on remote RevPi.\n"
                                    f"Sudo authentification failed for user {revpi_settings.ssh_user}. "
                                    "Please activate RevPiPyLoad manually via Cockpit or CLI."
                                ),
                                ConnectionFail.NO_XML_RPC_VIA_TUNNEL,
                                revpi_settings,
                            )
                            return False

            except asyncssh.PermissionDenied:
                self.connect_error.emit(
                    self.tr("Error"), self.tr(
                        "The combination of username and password was rejected from the SSH server.\n\n"
                        "Try again."
                    ),
                    ConnectionFail.SSH_AUTH,
                    revpi_settings,
                )
                return False
            except Exception as e:
                # todo: Check some more kinds of exceptions and nice user info
                self._clear_settings()
                self.connect_error.emit(
                    self.tr("Error"), self.tr(
                        "Cannot connect to SSH server:\n\n{0}"
                    ).format(str(e)),
                    ConnectionFail.SSH_CONNECT,
                    revpi_settings,
                )
                return False

            sp = create_server_proxy(revpi_settings, ssh_tunnel_port)

        else:
            sp = create_server_proxy(revpi_settings)

        # Load values and test connection to Revolution Pi
        try:
            ma = search(r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", sp.version())
            pyload_version = int(ma.group("major")), int(ma.group("minor")), int(ma.group("patch"))
            pyload_version_str = ma.string
            xml_funcs = sp.system.listMethods()
            xml_mode = sp.xmlmodus()
        except Exception as e:
            log.exception(e)
            self.connection_error_observed.emit(str(e))

            if revpi_settings.ssh_use_tunnel:
                self.connect_error.emit(
                    self.tr("Error"), self.tr(
                        "Cannot connect to RevPiPyLoad service through SSH tunnel.\n\n"
                        "Possible reasons:\n"
                        "- RevPiPyLoad service is not running. Activate service on your RevPi.\n"
                        "- RevPiPyLoad XML-RPC service is not bound to localhost.\n"
                        "- ACL permission is not set for 127.0.0.1."
                    ),
                    ConnectionFail.NO_XML_RPC_VIA_TUNNEL,
                    revpi_settings,
                )
            else:
                self.connect_error.emit(
                    self.tr("Error"), self.tr(
                        "Cannot connect to RevPiPyLoad XML-RPC service.\n\n"
                        "Possible reasons:\n"
                        "- RevPi is offline.\n"
                        "- RevPiPyLoad service is not running. Activate service on your RevPi.\n"
                        "- RevPiPyLoad XML-RPC service is bound to localhost only.\n"
                        "- The ACL permission is not set for your IP.\n\n"
                        "Use 'Connect via SSH' to use encrypted connection or run "
                        "'sudo revpipyload_secure_installation' on RevPi to set up direct remote access."
                    ),
                    ConnectionFail.NO_XML_RPC,
                    revpi_settings,
                )

            return False

        self.settings = revpi_settings
        self.ssh_pass = ssh_pass
        self.pyload_version = pyload_version
        self.pyload_version_str = pyload_version_str
        self.xml_funcs = xml_funcs
        self.xml_mode = xml_mode

        with self._lck_cli:
            self.ssh_tunnel_server = ssh_tunnel_server
            self._cli = sp
            self._cli_connect.put_nowait((revpi_settings, ssh_tunnel_port))

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

            log.debug("Simulator destroyed.")
            self.connection_disconnected.emit()

        elif self._cli is not None:

            # Tell all widget, that we want to disconnect
            self.connection_disconnecting.emit()
            self.settings.save_settings()

            with self._lck_cli:
                if self._ps_started:
                    try:
                        self._cli.psstop()
                    except Exception:
                        pass
                self._clear_settings()
                self._cli = None

                if self.ssh_tunnel_server:
                    self.ssh_tunnel_server.disconnect()
                    self.ssh_tunnel_server = None

            self.connection_disconnected.emit()

    def pyload_simulate(self, configrsc: str, procimg: str, clean_existing: bool):
        """
        Start the simulator for piControl on local computer.

        :param configrsc: piCtory configuration
        :param procimg: Process image, which is a 4 kByte file for simulation
        :param clean_existing: Reset the file to ZERO \x00 bytes
        """
        log.debug("ConnectionManager.start_simulate")

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
            log.exception(e)
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
        log.debug("ConnectionManager.reset_simulator")
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
                self.status_changed.emit(self.tr("Simulating"), "#E3DE48")
            elif self._cli is None:
                sp = None
                self.status_changed.emit(self.tr("Not connected"), "lightblue")
            elif not self._cli_connect.empty():
                # Get new connection information to create object in this thread
                revpi_settings, ssh_tunnel_port = self._cli_connect.get()
                sp = create_server_proxy(revpi_settings, ssh_tunnel_port)
                self._cli_connect.task_done()

            if sp:
                try:
                    plc_exit_code = sp.plcexitcode()
                    if self._xml_mode_refresh:
                        self.xml_mode = sp.xmlmodus()
                        self._xml_mode_refresh = False
                except CannotSendRequest as e:
                    log.warning(e)
                except Exception as e:
                    log.warning(e)
                    self.status_changed.emit(self.tr("Server error"), "#CC6666")
                    self._has_error = True
                    self.connection_error_observed.emit("{0} | {1}".format(e, type(e)))

                    if self.ssh_tunnel_server and not self.ssh_tunnel_server.connected:
                        self.ssh_tunnel_server.disconnect()
                        ssh_tunnel_server = SSHLocalTunnel(
                            self.settings.port,
                            self.settings.address,
                            self.settings.ssh_port
                        )
                        try:
                            ssh_tunnel_port = self.ssh_tunnel_server.connect_by_credentials(
                                self.settings.ssh_user,
                                self.ssh_pass
                            )
                            sp = create_server_proxy(self.settings, ssh_tunnel_port)
                            with self._lck_cli:
                                self.ssh_tunnel_server = ssh_tunnel_server
                                self._cli = sp
                                self.connection_recovered.emit()
                        except Exception:
                            pass

                else:
                    if self._has_error:
                        self._has_error = False
                        self.connection_recovered.emit()

                    if plc_exit_code == -1:
                        self.status_changed.emit(self.tr("Running"), "green")
                    elif plc_exit_code == -2:
                        self.status_changed.emit(self.tr("PLC file not found"), "#CC6666")
                    elif plc_exit_code == -3:
                        self.status_changed.emit(self.tr("Not running (no status)"), "#E3DE48")
                    elif plc_exit_code == -9:
                        self.status_changed.emit(self.tr("Program killed"), "#CC6666")
                    elif plc_exit_code == -15:
                        self.status_changed.emit(self.tr("Program terminated"), "#CC6666")
                    elif plc_exit_code == 0:
                        self.status_changed.emit(self.tr("Not running"), "#E3DE48")
                    else:
                        self.status_changed.emit(self.tr("Finished with exit code {0}").format(plc_exit_code), "#E3DE48")

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
            log.error("Not connected while calling {0}".format(function_name))
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
                    self._has_error = True
                    log.error(e)
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
        """
        Connection proxy of actual connection.

        Use connection_recovered signal to figure out new parameters.
        """
        ssh_tunnel_port = self.ssh_tunnel_server.local_tunnel_port if self.ssh_tunnel_server else None
        return create_server_proxy(self.settings, ssh_tunnel_port)

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


def create_server_proxy(revpi_settings: RevPiSettings, ssh_tunnel_port: int = None) -> ServerProxy:
    """
    Create a ServerProxy instance based on the given settings.

    :param revpi_settings: Revolution Pi saved connection settings
    :param ssh_tunnel_port: Use this port if an SSH tunnel is already established
    :return: ServerProxy instance
    """
    if not ssh_tunnel_port and revpi_settings.is_unix_socket:
        return ServerProxy("http://localhost", transport=UnixStreamTransport(revpi_settings.address))

    if ssh_tunnel_port:
        return ServerProxy("http://127.0.0.1:{0}".format(ssh_tunnel_port))

    if revpi_settings.ssh_use_tunnel:
        # This case is usually handled by passing ssh_tunnel_port after connecting the tunnel
        return ServerProxy("http://127.0.0.1:{0}".format(revpi_settings.port))

    return ServerProxy("http://{0}:{1}".format(revpi_settings.address, revpi_settings.port))


def all_revpi_settings() -> [RevPiSettings]:
    """Get all revpi settings objects."""
    # Get length of array and close it, the RevPiSettings-class need it
    count_settings = settings.beginReadArray("connections")
    settings.endArray()
    return [RevPiSettings(i) for i in range(count_settings)]


def swap_word_order(bytes_to_swap) -> bytes:
    """Swap word order of an even byte array."""
    array_lenght = len(bytes_to_swap)
    swap_array = bytearray(bytes_to_swap)
    for i in range(0, array_lenght // 2, 2):
        swap_array[-i - 2:array_lenght - i], swap_array[i:i + 2] = \
            swap_array[i:i + 2], swap_array[-i - 2:array_lenght - i]
    return bytes(swap_array)


def import_old_settings():
    """Try to import saved connections from old storage to new setting object."""
    if settings.value("revpicommander/imported_settings", False, type=bool):
        return
    settings.setValue("revpicommander/imported_settings", True)

    old_settings = QtCore.QSettings("revpipyplc", "revpipyload")
    count_settings = old_settings.beginReadArray("connections")
    old_settings.endArray()

    for i in range(count_settings):
        try:
            revpi_setting = RevPiSettings(i, settings_storage=old_settings)
            revpi_setting._settings = settings
            revpi_setting.save_settings()
        except Exception:
            log.warning("Could not import saved connection {0}".format(i))


import_old_settings()
