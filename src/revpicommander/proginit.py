# -*- coding: utf-8 -*-
"""Global program initialization."""
# SPDX-FileCopyrightText: 2018-2023 Sven Sager
# SPDX-License-Identifier: LGPL-2.0-or-later
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018-2023 Sven Sager"
__license__ = "LGPL-2.0-or-later"
__version__ = "1.3.1"

import logging
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from os import R_OK, W_OK, access, environ, getpid, remove
from os.path import abspath, dirname, exists, join
from shutil import copy, move
from threading import Event

try:
    # Import program version from meta data module of your program
    from . import __version__ as external_version
except Exception:
    external_version = None

# Program name
programname = "revpicommander"
program_version = external_version

conf_rw = False  # If you want so save the configuration with .save_conf() set to True
conf_rw_save = False  # Create new conf file in same directory and move to old one
conf_rw_backup = False  # Keep a backup of old conf file [filename].bak
_extend_daemon_startup_timeout = 0.0  # Default startup timeout is 90 seconds

conf = ConfigParser()
logger = logging.getLogger()
pidfile = "/var/run/{0}.pid".format(programname)
_daemon_started_up = Event()
_daemon_main_pid = getpid()
_systemd_notify = environ.get("NOTIFY_SOCKET", None)
if _systemd_notify:
    from socket import AF_UNIX, SOCK_DGRAM, socket

    # Set up the notification socket for systemd communication
    _systemd_socket = socket(family=AF_UNIX, type=SOCK_DGRAM)
    if _extend_daemon_startup_timeout:
        # Extend systemd TimeoutStartSec by defined timeout extension in micro seconds
        _systemd_socket.sendto(
            f"EXTEND_TIMEOUT_USEC={_extend_daemon_startup_timeout * 1000000}\n",
            _systemd_notify,
        )


def can_be_forked():
    """
    Check the possibility of forking the process.

    Under certain circumstances, a process cannot be forked. These include
    certain build settings or packaging, as well as the missing function on
    some operating systems.

    :return: True, if forking is possible
    """
    from sys import platform

    # Windows operating system does not support the .fork() call
    if platform.startswith("win"):
        return False

    # A PyInstaller bundle does not support the .fork() call
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return False

    return True


def cleanup():
    """
    Clean up before exit the program.

    This function must be called at the end of the program. It flushes
    the logging buffers and deletes the PID file in daemon mode.
    """
    if pargs.daemon and exists(pidfile):
        remove(pidfile)

    # Shutdown logging system
    logging.shutdown()

    # Close logfile
    if pargs.daemon:
        sys.stdout.close()


def reconfigure_logger():
    """Configure logging module of program."""

    class FilterDebug(logging.Filter):
        """Set this filter to log handler if verbose level is > 1."""

        def filter(self, record: logging.LogRecord) -> bool:
            remove_record = False

            # Remove paramiko ssh module
            remove_record = remove_record or record.name.startswith("paramiko")

            return not remove_record

    # Clear all log handler
    for lhandler in logger.handlers.copy():
        lhandler.close()
        logger.removeHandler(lhandler)

    if pargs.daemon:
        # Create daemon log file
        fh_logfile = open("/var/log/{0}.log".format(programname), "a")

        # Close stdout and use logfile
        sys.stdout.close()
        sys.stdout = fh_logfile
        sys.stderr = sys.stdout

    # Create new log handler
    if pargs.verbose > 2:
        log_frm = "{asctime} [{levelname:8}] {name} {message}"
    else:
        log_frm = "{asctime} [{levelname:8}] {message}"
    logformat = logging.Formatter(log_frm, datefmt="%Y-%m-%d %H:%M:%S", style="{")
    lhandler = logging.StreamHandler(sys.stdout)
    lhandler.setFormatter(logformat)
    logger.addHandler(lhandler)

    if "logfile" in pargs and pargs.logfile is not None:
        # Write logs to a logfile
        lhandler = logging.FileHandler(filename=pargs.logfile)
        lhandler.setFormatter(logformat)
        logger.addHandler(lhandler)

    # Loglevel auswerten
    if pargs.verbose == 1:
        loglevel = logging.INFO
    elif pargs.verbose > 1:
        lhandler.addFilter(FilterDebug())
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARNING
    logger.setLevel(loglevel)


def reload_conf(clear_load=False) -> None:
    """
    Reload config file.

    After successful reload, call set_startup_complete() function to inform
    systemd that all functions are available again.

    If keys are commented out in conf file, they will still be in the conf file.
    To remove not existing keys set clear_load to True.

    :param clear_load: Clear conf before reload
    """
    if _systemd_notify:
        # Inform systemd about reloading configuration
        _systemd_socket.sendto(b"RELOADING=1\n", _systemd_notify)

        # Reset started up event for the set_startup_complete function
        _daemon_started_up.clear()

    if "conffile" in pargs:
        # Check config file
        if not access(pargs.conffile, R_OK):
            raise RuntimeError("can not access config file '{0}'".format(pargs.conffile))
        if conf_rw:
            if (conf_rw_save or conf_rw_backup) and not access(dirname(pargs.conffile), W_OK):
                raise RuntimeError(
                    "can not wirte to directory '{0}' to create files"
                    "".format(dirname(pargs.conffile))
                )
            if not access(pargs.conffile, W_OK):
                raise RuntimeError("can not write to config file '{0}'".format(pargs.conffile))

        if clear_load:
            # Clear all sections and do not create a new instance
            for section in conf.sections():
                conf.remove_section(section)

        # Read configuration
        logger.info("loading config file: {0}".format(pargs.conffile))
        conf.read(pargs.conffile)


def save_conf():
    """Save configuration."""
    if not conf_rw:
        raise RuntimeError("You have to set conf_rw to True.")
    if "conffile" in pargs:
        if conf_rw_backup:
            copy(pargs.conffile, pargs.conffile + ".bak")
        if conf_rw_save:
            with open(pargs.conffile + ".new", "w") as fh:
                conf.write(fh)
            move(pargs.conffile + ".new", pargs.conffile)
        else:
            with open(pargs.conffile, "w") as fh:
                conf.write(fh)


def startup_complete():
    """
    Call this when the daemon is completely started.

    When a daemon is started, it may take some time for everything to be
    available. This function notifies the init system when all functions of
    this daemon are available so that the starts of further daemons can be
    properly timed.

    The systemd unit file that is supposed to start this demon must be set
    to 'Type=notify'. If the daemon supports reloading the settings,
    'ExecReload=/bin/kill -HUP $MAINPID' must also be set. The daemon must
    call this function again after the reload in order to signal systemd the
    completed reload.

    If systemd is available from version 250 and the daemon supports reloading
    the settings, 'Type=notify-reload' can be used without 'ExecReload'. The
    type 'notify-reload' is preferable if possible, as the reloading of the
    daemon is also synchronized with systemd.

    If the '--fork' parameter is used, the main process ends after calling
    this function to prevent the further start of demons by other init systems.
    """
    if _daemon_started_up.is_set():
        # Everyone was notified about complete start, if set
        return

    if _systemd_notify:
        # Inform systemd about complete startup of daemon process
        _systemd_socket.sendto(b"READY=1\n", _systemd_notify)

    if pargs.daemon:
        from os import kill

        # Send SIGTERM signal to main process
        kill(_daemon_main_pid, 15)

    _daemon_started_up.set()


# Generate command arguments of the program
parser = ArgumentParser(
    prog=programname,
    # todo: Add program description for help
    description="Program description",
)
parser.add_argument("--version", action="version", version=f"%(prog)s {program_version}")
parser.add_argument(
    "-f",
    "--logfile",
    dest="logfile",
    help="save log entries to this file",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    dest="verbose",
    default=0,
    help="switch on verbose logging",
)
# If packed with opensource licenses, add argument to print license information about bundled modules
open_source_licenses = join(dirname(__file__), "open-source-licenses", "open-source-licenses.txt")
if exists(open_source_licenses):
    parser.add_argument(
        "--open-source-licenses",
        action="store_true",
        dest="oss_licenses",
        help="print packed open-source-licenses and exit",
    )
pargs = parser.parse_args()

# Process open-source-licenses argument, if set (only affects bundled apps)
if "oss_licenses" in pargs and pargs.oss_licenses:
    with open(open_source_licenses, "r") as fh:
        sys.stdout.write(fh.read())
    sys.exit(0)

# Check important objects and set to default if they do not exists
if "daemon" not in pargs:
    pargs.daemon = False
if "verbose" not in pargs:
    pargs.verbose = 0

# Check if the program should run as a daemon
if pargs.daemon:
    # Check if daemon is already running
    if exists(pidfile):
        logger.error("Program already running as daemon. Check '{0}'".format(pidfile))
        sys.exit(1)

    # Fork to daemon
    from os import fork

    pid = fork()
    if pid > 0:
        # Main process waits for exit till startup is complete
        from os import kill
        from signal import SIGKILL, SIGTERM, signal

        # Catch the TERM signal, which will be sent from the forked process after startup_complete
        signal(SIGTERM, lambda number, frame: _daemon_started_up.set())

        # Use the default timeout of 90 seconds from systemd also for the '--daemon' flag
        if not _daemon_started_up.wait(90.0 + _extend_daemon_startup_timeout):
            sys.stderr.write(
                "Run into startup complete timout! Killing fork and exit main process\n"
            )
            kill(pid, SIGKILL)
            sys.exit(1)

        # Main process writes pidfile with pid of forked process
        with open(pidfile, "w") as f:
            f.write(str(pid))

        sys.exit(0)

# Get absolute paths
pwd = abspath(".")

# Configure logger
if "logfile" in pargs and pargs.logfile is not None and dirname(pargs.logfile) == "":
    pargs.logfile = join(pwd, pargs.logfile)
reconfigure_logger()

# Initialize configparser of globalconfig
if "conffile" in pargs and dirname(pargs.conffile) == "":
    pargs.conffile = join(pwd, pargs.conffile)

# Load configuration - Comment out, if you do that in your own program
reload_conf()
