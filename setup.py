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
    version="0.9.0",
    python_requires="~=3.4",
    requires=["PyQt5", "zeroconf"],

    scripts=["data/revpicommander"],
    data_files=[
        ("share/applications", ["data/revpicommander.desktop"]),
        ("share/icons/hicolor/32x32/apps", ["data/revpicommander.png"]),
        ("share/revpicommander", glob("revpicommander/*.py")),
        ("share/revpicommander/revpimodio2", glob("lib/revpimodio2/revpimodio2/*.py")),
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
    "Dieses Programm startet beim Systemstart ein angegebenes Python PLC\n"
    "Programm. Es überwacht das Programm und startet es im Fehlerfall neu.\n"
    "Bei Abstruz kann das gesamte /dev/piControl0 auf 0x00 gesettz werden.\n"
    "Außerdem stellt es einen XML-RPC Server bereit, über den die Software\n"
    "auf den RevPi geladen werden kann. Das Prozessabbild kann über ein Tool\n"
    "zur Laufzeit überwacht werden.",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    license="GPLv3",
    cmdclass={"install_egg_info": MyEggInfo},
)
