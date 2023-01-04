# -*- coding: utf-8 -*-
"""Setupscript for RevPiCommander."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "GPLv3"

from setuptools import find_namespace_packages, setup

setup(
    name="revpicommander",
    version="0.9.10rc1",

    packages=find_namespace_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,

    install_requires=[
        "PyQt5",
        "revpimodio2",
        "zeroconf"
    ],
    entry_points={
        'console_scripts': [
            'revpicommander = revpicommander.revpicommander:main',
        ],
        'gui_scripts': [
            'RevPiCommander = revpicommander.revpicommander:main',
        ],
    },

    url="https://revpimodio.org/revpipyplc/",
    license="GPLv3",
    author="Sven Sager",
    author_email="akira@narux.de",
    maintainer="Sven Sager",
    maintainer_email="akira@revpimodio.org",
    description="GUI for Revolution Pi to upload programs and do IO-Checks",
    long_description="The RevPiCommander is a GUI tool to manage your revolution Pi over the\n"
                     "network. You can search for RevPis in your network, manage the settings\n"
                     "of RevPiPyLoad and do IO checks on your local machine. Developing your\n"
                     "control program is very easy with the developer, upload and debug it\n"
                     "over the network.",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
