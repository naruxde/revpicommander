# -*- coding: utf-8 -*-
"""Setupscript fuer RevPiPyLoad."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "LGPLv3"

import distutils.command.install_egg_info
from distutils.core import setup
from glob import glob


class MyEggInfo(distutils.command.install_egg_info.install_egg_info):

    u"""Disable egg_info installation, seems pointless for a non-library."""

    def run(self):
        u"""just pass egg_info."""
        pass


setup(
    version="0.9.3",
    python_requires="~=3.4",
    requires=["PyQt5", "revpimodio2", "zeroconf"],

    scripts=["data/revpicommander"],
    data_files=[
        ("share/applications", ["data/revpicommander.desktop"]),
        ("share/icons/hicolor/32x32/apps", ["data/revpicommander.png"]),
        ("share/revpicommander", glob("revpicommander/*.py")),
        ("share/revpicommander/ui", glob("include/ui/*.py")),
        ("share/revpicommander/locale/", glob("revpicommander/locale/*.qm")),
    ],

    # Additional meta-data
    name="revpicommander",
    author="Sven Sager",
    author_email="akira@narux.de",
    maintainer="Sven Sager",
    maintainer_email="akira@revpimodio.org",
    url="https://revpimodio.org/revpipyplc/",
    description="GUI for Revolution Pi to upload programs and do IO-Checks",
    long_description=""
    "The RevPiCommander is a GUI tool to manage your revolution Pi over the\n"
    "network. You can search for RevPis in your network, manage the settings\n"
    "of RevPiPyLoad and do IO checks on your local machine. Developing your\n"
    "control program is very easy with the developer, upload and debug it\n"
    "over the network.",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    license="GPLv3",
    cmdclass={"install_egg_info": MyEggInfo},
)
