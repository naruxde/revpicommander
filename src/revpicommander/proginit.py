# -*- coding: utf-8 -*-
"""Global program initialization."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

import logging
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from os import R_OK, W_OK, access
from os.path import abspath, dirname, join

# Program name
programname = "revpicommander"

# Set to True, if you want to save config file
conf_rw = False

conf = ConfigParser()
logger = logging.getLogger()
pidfile = "/var/run/{0}.pid".format(programname)


def cleanup():
    """Clean up program."""
    # Shutdown logging system
    logging.shutdown()


def reconfigure_logger():
    """Configure logging module of program."""
    # Clear all log handler
    for lhandler in logger.handlers.copy():
        lhandler.close()
        logger.removeHandler(lhandler)

    # Create new log handler
    logformat = logging.Formatter(
        "{asctime} [{levelname:8}] {message}",
        datefmt="%Y-%m-%d %H:%M:%S", style="{"
    )
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
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARNING
    logger.setLevel(loglevel)


def reload_conf():
    """Reload config file."""
    if "conffile" in pargs:

        # Check config file
        if not access(pargs.conffile, R_OK):
            raise RuntimeError(
                "can not access config file '{0}'".format(pargs.conffile)
            )
        if conf_rw and not access(pargs.conffile, W_OK):
            raise RuntimeError(
                "can not write to config file '{0}'".format(pargs.conffile)
            )

        # Create global config
        global conf
        logger.info("loading config file: {0}".format(pargs.conffile))
        conf.read(pargs.conffile)


# Generate command arguments of the program
parser = ArgumentParser(
    prog=programname,
    description="Program description"
)
parser.add_argument(
    "-f", "--logfile", dest="logfile",
    help="Save log entries to this file"
)
parser.add_argument(
    "-v", "--verbose", action="count", dest="verbose", default=0,
    help="Switch on verbose logging"
)
# The __main__ script will process the version number argument
parser.add_argument("--version", action="store_true", help="Print version number of program and exit")
pargs = parser.parse_args()

# Check important objects and set to default if they do not exists
if "verbose" not in pargs:
    pargs.verbose = 0

# Get absolute paths
pwd = abspath(".")

# Configure logger
if "logfile" in pargs and pargs.logfile is not None \
        and dirname(pargs.logfile) == "":
    pargs.logfile = join(pwd, pargs.logfile)
reconfigure_logger()

# Initialize configparser of globalconfig
if "conffile" in pargs and dirname(pargs.conffile) == "":
    pargs.conffile = join(pwd, pargs.conffile)

# Load configuration - Comment out, if you do that in your own program
reload_conf()
