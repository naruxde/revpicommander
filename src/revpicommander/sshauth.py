# -*- coding: utf-8 -*-
"""Authentication dialog for SSH."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

from logging import getLogger

import keyring
from PyQt5 import QtWidgets
from keyring.errors import KeyringError

from .ui.sshauth_ui import Ui_diag_sshauth

log = getLogger()


class SSHAuth(QtWidgets.QDialog, Ui_diag_sshauth):

    def __init__(self, user_name="", service_name: str = None, parent=None):
        """
        Ask the user for username and password or use saved entries.

        If you want to use the operating system's password storage, you have
        to set a 'service_name'. The value must be unique for your application
        or for each user, if the username is the same.

        :param user_name: Preset username, also used to check password save
        :param service_name: Identity to save passwords in os's password save
        :param parent: Qt parent for this dialog
        """
        log.debug("SSHAuth.__init__")

        super().__init__(parent)
        self.setupUi(self)

        self._in_keyring = False
        self._service_name = service_name
        self.cbx_save_password.setVisible(bool(service_name))
        self.txt_username.setText(user_name)

    def accept(self) -> None:
        log.debug("SSHAuth.accept")

        if self._service_name and self.cbx_save_password.isChecked():
            try:
                keyring.set_password(self._service_name, self.username, self.password)
            except KeyringError as e:
                log.error(e)
                self._in_keyring = False
                QtWidgets.QMessageBox.warning(
                    self, self.tr("Could not save password"), self.tr(
                        "Could not save password to operating systems password save.\n\n"
                        "Maybe your operating system does not support saving passwords. "
                        "This could be due to missing libraries or programs.\n\n"
                        "This is not an error of RevPi Commander."
                    )
                )
            else:
                self._in_keyring = True

        super().accept()

    def exec(self) -> int:
        log.debug("SSHAuth.exec")

        if self._service_name:
            try:
                saved_password = keyring.get_password(self._service_name, self.username)
            except KeyringError as e:
                log.error(e)
                self._in_keyring = False
            else:
                if saved_password:
                    self._in_keyring = True
                    self.txt_password.setText(saved_password)
                    return QtWidgets.QDialog.Accepted

        return super().exec()

    def remove_saved_password(self) -> None:
        """Remove saved password."""
        log.debug("SSHAuth.remove_saved_password")

        if self._service_name:
            try:
                keyring.delete_password(self._service_name, self.username)
            except KeyringError as e:
                log.error(e)

    @property
    def in_keyring(self) -> bool:
        """True, if password is in keyring."""
        return self._in_keyring

    @property
    def password(self) -> str:
        """Get the saved or entered password."""
        return self.txt_password.text()

    @property
    def username(self) -> str:
        """Get the entered username."""
        return self.txt_username.text()
