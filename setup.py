# -*- coding: utf-8 -*-
"""Setupscript for RevPiCommander."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "GPLv3"

from setuptools import find_namespace_packages, setup

from src.revpicommander import __version__

setup(
    name="revpicommander",
    version=__version__,

    packages=find_namespace_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,

    install_requires=[
        "keyring",
        "PyQt5",
        "paramiko",
        "revpimodio2",
        "zeroconf"
    ],
    entry_points={
        'gui_scripts': [
            'revpicommander-gui = revpicommander.revpicommander:main',
        ],
    },

    platforms=["all"],

    url="https://revpimodio.org/revpipyplc/",
    license="GPLv3",
    author="Sven Sager",
    author_email="akira@narux.de",
    maintainer="Sven Sager",
    maintainer_email="akira@revpimodio.org",
    description="GUI for Revolution Pi to upload programs and do IO-Checks",
    long_description="The RevPiCommander is a GUI tool to manage your Revolution Pi over the\n"
                     "network. You can search for RevPis in your network, manage the settings\n"
                     "of RevPiPyLoad and do IO checks on your local machine. Developing your\n"
                     "control program is very easy with the developer, upload and debug it\n"
                     "over the network.",
    keywords=["revpi", "revolution pi", "revpimodio", "plc"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
