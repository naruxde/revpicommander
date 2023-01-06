# -*- coding: utf-8 -*-
"""Authentication dialog for SSH."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

from enum import Enum

from PyQt5 import QtWidgets

from revpicommander.ui.sshauth_ui import Ui_diag_sshauth


class SSHAuthType(Enum):
    PASS = "pass"
    KEYS = "keys"

class SSHAuth(QtWidgets.QDialog, Ui_diag_sshauth):
    """Version information window."""

    def __init__(self, auth_type: SSHAuthType, parent=None):
        super(SSHAuth, self).__init__(parent)
        self.setupUi(self)

        self.wid_password.setVisible(auth_type is SSHAuthType.PASS)
        self.wid_keys.setVisible(auth_type is SSHAuthType.KEYS)

    @property
    def password(self) -> str:
        return self.txt_password.text()

    @property
    def username(self) -> str:
        return self.txt_username.text()

    @username.setter
    def username(self, value: str):
        self.txt_username.setText(value)
