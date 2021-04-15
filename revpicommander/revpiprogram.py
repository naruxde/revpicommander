# -*- coding: utf-8 -*-
"""Revolution Pi PLC program configuration."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "GPLv3"

import gzip
import os
import tarfile
import zipfile
from shutil import rmtree
from tempfile import mkdtemp
from xmlrpc.client import Binary

from PyQt5 import QtCore, QtGui, QtWidgets

import helper
import proginit as pi
from ui.revpiprogram_ui import Ui_diag_program


class RevPiProgram(QtWidgets.QDialog, Ui_diag_program):
    """Program options of RevPiPyLoad."""

    def __init__(self, parent=None):
        super(RevPiProgram, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.dc = {}
        self.lst_files = []

        self.cbx_pictory.setEnabled(False)
        self.recover_gui()

    def _apply_acl(self):
        """Set availability of controls depending on ACL level."""

        # Setting properties require level 4
        self.cbb_plcprogram.setEnabled(helper.cm.xml_mode >= 4)
        self.txt_plcarguments.setEnabled(helper.cm.xml_mode >= 4)
        self.rbn_pythonversion_2.setEnabled(helper.cm.xml_mode >= 4)
        self.rbn_pythonversion_3.setEnabled(helper.cm.xml_mode >= 4)
        self.cbx_plcworkdir_set_uid.setEnabled(helper.cm.xml_mode >= 4)

        # Downloads require level 2
        self.btn_program_download.setEnabled(helper.cm.xml_mode >= 2)
        self.btn_pictory_download.setEnabled(helper.cm.xml_mode >= 2)
        self.btn_procimg_download.setEnabled(helper.cm.xml_mode >= 2)

        # Uploads require level 3
        self.btn_program_upload.setEnabled(helper.cm.xml_mode >= 3)
        self.btn_pictory_upload.setEnabled(helper.cm.xml_mode >= 3)

    def _changesdone(self):
        """
        Check for unsaved changes in dialog.

        :return: True, if unsaved changes was found
        """
        return \
            self.cbb_plcprogram.currentText() != self.dc.get("plcprogram", "") or \
            self.txt_plcarguments.text() != self.dc.get("plcarguments", "") or \
            self.rbn_pythonversion_2.isChecked() != (self.dc.get("pythonversion", 3) == 2) or \
            self.rbn_pythonversion_3.isChecked() != (self.dc.get("pythonversion", 3) == 3) or \
            int(self.cbx_plcworkdir_set_uid.isChecked()) != self.dc.get("plcworkdir_set_uid", 0) or \
            self.sbx_plcprogram_watchdog.value() != self.dc.get("plcprogram_watchdog", 0)

    def _load_settings(self, files_only=False):
        """Load values to GUI widgets."""
        pi.logger.debug("RevPiProgram._load_settings")

        if files_only:
            mrk_program = self.cbb_plcprogram.currentText()
        else:
            mrk_program = ""

        self.cbb_plcprogram.clear()
        self.cbb_plcprogram.addItem("")

        self.lst_files.sort()
        is_in_list = False
        for file in self.lst_files:
            if file == ".placeholder":
                continue
            self.cbb_plcprogram.addItem(file)
            check = mrk_program or self.dc.get("plcprogram", "")
            if file == check:
                is_in_list = True

        if not is_in_list:
            pi.logger.warning("File {0} is not in list".format(mrk_program or self.dc.get("plcprogram", "")))

        if files_only:
            self.cbb_plcprogram.setCurrentText(mrk_program)
        else:
            self.cbb_plcprogram.setCurrentText(self.dc.get("plcprogram", ""))
            self.txt_plcarguments.setText(self.dc.get("plcarguments", ""))
            self.rbn_pythonversion_2.setChecked(self.dc.get("pythonversion", 3) == 2)
            self.rbn_pythonversion_3.setChecked(self.dc.get("pythonversion", 3) == 3)
            self.cbx_plcworkdir_set_uid.setChecked(bool(self.dc.get("plcworkdir_set_uid", 0)))
            self.sbx_plcprogram_watchdog.setValue(self.dc.get("plcprogram_watchdog", 0))

    def accept(self) -> None:
        # todo: After upload ask for restart pcl program?
        if not self._changesdone():
            super(RevPiProgram, self).accept()
            return

        if self.cbb_plcprogram.currentText() == "":
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "You have to select a start program, before uploading the "
                    "settings."
                )
            )
            return

        ask = QtWidgets.QMessageBox.question(
            self, self.tr("Question"), self.tr(
                "The settings will be set on the Revolution Pi now.\n\n"
                "If you made changes on the 'PCL Program' section, your plc "
                "program will restart now!"
            )
        ) == QtWidgets.QMessageBox.Yes

        if not ask:
            return

        self.dc["plcprogram"] = self.cbb_plcprogram.currentText()
        self.dc["plcarguments"] = self.txt_plcarguments.text()
        self.dc["pythonversion"] = 2 if self.rbn_pythonversion_2.isChecked() else 3
        self.dc["plcworkdir_set_uid"] = int(self.cbx_plcworkdir_set_uid.isChecked())
        self.dc["plcprogram_watchdog"] = self.sbx_plcprogram_watchdog.value()

        saved = helper.cm.call_remote_function(
            "set_config", self.dc, ask,
            default_value=False
        )

        if saved:
            super(RevPiProgram, self).accept()
        else:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The settings could not be saved on the Revolution Pi!\n"
                    "Try to save the values one mor time and check the log "
                    "files of RevPiPyLoad if the error rises again."
                )
            )

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self._changesdone():
            ask = QtWidgets.QMessageBox.question(
                self, self.tr("Question"), self.tr(
                    "Do you really want to quit? \nUnsaved changes will be lost."
                )
            ) == QtWidgets.QMessageBox.Yes

            if ask:
                self.reject()
            else:
                a0.ignore()

    def exec(self) -> int:
        # Reset class values
        if not helper.cm.connected:
            return QtWidgets.QDialog.Rejected

        self.dc = helper.cm.call_remote_function("get_config", default_value={})
        self.lst_files = helper.cm.call_remote_function("get_filelist", default_value=[])
        if len(self.dc) == 0 or len(self.lst_files) == 0:
            return QtWidgets.QDialog.Rejected

        self._load_settings()
        self._apply_acl()

        return super(RevPiProgram, self).exec()

    def reject(self) -> None:
        """Reject all sub windows and reload settings."""
        self._load_settings()
        super(RevPiProgram, self).reject()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: PLC program

    def _upload_pictory(self, filename: str):
        """Upload piCtory configuration."""
        fh = open(filename, "rb")
        file_binary = Binary(fh.read())
        fh.close()

        ask = QtWidgets.QMessageBox.question(
            self, self.tr("Reset driver..."), self.tr(
                "Reset piControl driver after successful uploading new piCtory "
                "configuration?\nThe process image will be interrupted for a "
                "short time!"
            ), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
        )
        if ask == QtWidgets.QMessageBox.Cancel:
            return

        ec = helper.cm.call_remote_function(
            "set_pictoryrsc", file_binary, ask == QtWidgets.QMessageBox.Yes
        )

        if ec is None:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Got an network error while send data to Revolution Pi.\n"
                    "Please try again."
                )
            )
        elif ec == 0:
            helper.cm.program_last_pictory_file = filename
            if ask == QtWidgets.QMessageBox.Yes:
                QtWidgets.QMessageBox.information(
                    self, self.tr("Success"), self.tr(
                        "The transfer of the piCtory configuration "
                        "and the reset of piControl have been "
                        "successfully executed."
                    ),
                )
            else:
                QtWidgets.QMessageBox.information(
                    self, self.tr("Success"), self.tr(
                        "The piCtory configuration was successfully transferred."
                    )
                )

        elif ec == -1:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not process the transferred file."
                )
            )
        elif ec == -2:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Can not find main elements in piCtory file."
                )
            )
        elif ec == -4:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Contained devices could not be found on Revolution "
                    "Pi. The configuration may be from a newer piCtory version!"
                )
            )
        elif ec == -5:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Could not load RAP catalog on Revolution Pi."
                )
            )
        elif ec < 0:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The piCtory configuration could not be "
                    "written on the Revolution Pi."
                )
            )
        elif ec > 0:
            QtWidgets.QMessageBox.warning(
                self, self.tr("Warning"), self.tr(
                    "The piCtroy configuration has been saved successfully.\n"
                    "An error occurred on piControl reset!"
                )
            )

    def check_replacedir(self, rootdir: str):
        """
        Return root dir of a extracted archive an piCtory configuration.

        This function checks the root dir of a extracted directory. It
        will check the existence of a piCtory configuration will will
        return that information in the return tuple.

        :param rootdir: Dir to check
        :return: Tuple with corrected root dir and piCtory configuration
        """
        lst_dir = os.listdir(rootdir)
        if len(lst_dir) == 1 and \
                os.path.isdir(os.path.join(rootdir, lst_dir[0])):
            return os.path.join(rootdir, lst_dir[0]), None

        if len(lst_dir) == 2:
            rscfile = None
            for fname in lst_dir:
                if fname.find(".rsc"):
                    rscfile = os.path.join(rootdir, fname)
            return os.path.join(rootdir, lst_dir[0]), rscfile

        else:
            return rootdir, None

    def create_filelist(self, rootdir):
        """Create a file list of a directory.

        :param rootdir: Root dir to crate file list
        :return: File list with <class 'str'>
        """
        filelist = []
        for tup_dir in os.walk(rootdir):
            for fname in tup_dir[2]:
                filelist.append(os.path.join(tup_dir[0], fname))
        return filelist

    def recover_gui(self):
        """Load saved GUI states."""
        self.cbb_format.setCurrentIndex(helper.settings.value("program/cbb_format_index", 0, int))
        self.cbx_pictory.setChecked(helper.settings.value("program/cbx_pictory_checked", False, bool))
        self.cbx_clear.setChecked(helper.settings.value("program/cbx_clear_checked", False, bool))

    @QtCore.pyqtSlot(int)
    def on_cbb_format_currentIndexChanged(self, index: int):
        helper.settings.setValue("program/cbb_format_index", index)
        self.cbx_pictory.setEnabled(index >= 1)

    @QtCore.pyqtSlot()
    def on_btn_program_download_pressed(self):
        """Download plc program from Revolution Pi."""
        if not helper.cm.connected:
            return

        selected_dir = ""

        if self.cbb_format.currentIndex() == 0:
            # Save files as zip archive
            diag_save = QtWidgets.QFileDialog(
                self, self.tr("Save ZIP archive..."),
                os.path.join(
                    helper.cm.program_last_zip_file,
                    "{0}.zip".format(helper.cm.name)
                ),
                self.tr("ZIP archive (*.zip);;All files (*.*)")
            )
            diag_save.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            diag_save.setDefaultSuffix("zip")
            self.rejected.connect(diag_save.reject)

            if diag_save.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_save.selectedFiles()) != 1:
                return
            filename = diag_save.selectedFiles()[0]
            fh = open(filename, "wb")

            helper.cm.program_last_zip_file = filename

        elif self.cbb_format.currentIndex() == 1:
            # Save files as TarGz archive
            diag_save = QtWidgets.QFileDialog(
                self, self.tr("Save TGZ archive..."),
                os.path.join(
                    helper.cm.program_last_tar_file,
                    "{0}.tgz".format(helper.cm.name)
                ),
                self.tr("TGZ archive (*.tgz);;All files (*.*)")
            )
            diag_save.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            diag_save.setDefaultSuffix("tgz")
            self.rejected.connect(diag_save.reject)

            if diag_save.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_save.selectedFiles()) != 1:
                return
            filename = diag_save.selectedFiles()[0]
            fh = open(filename, "wb")

            helper.cm.program_last_tar_file = filename

        else:
            # Other indexes are not allowed for download
            return

        plcfile = helper.cm.call_remote_function(
            "plcdownload",
            "zip" if self.cbb_format.currentIndex() == 0 else "tar",
            self.cbx_pictory.isChecked()
        )

        if plcfile is None:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Could not load PLC program from Revolution Pi."
                )
            )

        else:
            try:
                fh.write(plcfile.data)
                fh.close()

            except Exception as e:
                pi.logger.error(e)
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error"), self.tr(
                        "Coud not save the archive or extract the files!\n"
                        "Please retry.")
                )
            else:
                QtWidgets.QMessageBox.information(
                    self, self.tr("Success"), self.tr(
                        "Transfer successfully completed."
                    )
                )

    @QtCore.pyqtSlot()
    def on_btn_program_upload_pressed(self):
        """Upload plc program to Revolution Pi."""
        if not helper.cm.connected:
            return

        dirtmp = None

        def remove_temp():
            # Remove temp dir
            if dirtmp is not None:
                rmtree(dirtmp)

        dirselect = ""
        lst_files = []
        folder_name = ""
        rscfile = None

        if self.cbb_format.currentIndex() == 0:
            # Upload zip archive content
            diag_open = QtWidgets.QFileDialog(
                self, self.tr("Upload content of ZIP archive..."),
                helper.cm.program_last_file_upload,
                self.tr("ZIP archive (*.zip);;All files (*.*)")
            )
            diag_open.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            diag_open.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            diag_open.setDefaultSuffix("zip")
            self.rejected.connect(diag_open.reject)

            if diag_open.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_open.selectedFiles()) != 1:
                return

            filename = diag_open.selectedFiles()[0]
            helper.cm.program_last_file_upload = filename
            if zipfile.is_zipfile(filename):
                dirtmp = mkdtemp()
                fhz = zipfile.ZipFile(filename)
                fhz.extractall(dirtmp)
                fhz.close()

                lst_files = self.create_filelist(dirtmp)
                dirselect, rscfile = self.check_replacedir(dirtmp)

            else:
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error"), self.tr(
                        "The selected file ist not a ZIP archive."
                    )
                )
                return

        elif self.cbb_format.currentIndex() == 1:
            # Upload TarGz content
            diag_open = QtWidgets.QFileDialog(
                self, self.tr("Upload content of TAR archive..."),
                helper.cm.program_last_file_upload,
                self.tr("TAR archive (*.tgz);;All files (*.*)")
            )
            diag_open.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            diag_open.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            diag_open.setDefaultSuffix("tgz")
            self.rejected.connect(diag_open.reject)

            if diag_open.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_open.selectedFiles()) != 1:
                return

            filename = diag_open.selectedFiles()[0]
            helper.cm.program_last_file_upload = filename
            if tarfile.is_tarfile(filename):
                dirtmp = mkdtemp()
                fht = tarfile.open(filename)
                fht.extractall(dirtmp)
                fht.close()

                lst_files = self.create_filelist(dirtmp)
                dirselect, rscfile = self.check_replacedir(dirtmp)

            else:
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error"), self.tr(
                        "The selected file ist not a TAR archive."
                    )
                )
                return

        # No files selected
        if len(lst_files) == 0:
            QtWidgets.QMessageBox.warning(
                self, self.tr("No files to upload..."), self.tr(
                    "Found no files to upload in given location or archive."
                )
            )
            remove_temp()
            return

        # Clean up directory before upload
        clean_revpi = helper.cm.call_remote_function("plcuploadclean", default_value=False)
        if self.cbx_clear.isChecked() and not clean_revpi:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "There was an error deleting the files on the Revolution Pi.\n"
                    "Upload aborted! Please try again."
                )
            )
            remove_temp()
            return

        plc_program_not_in_upload = True
        ec = 0

        for file_name in lst_files:

            if file_name == rscfile:
                # Do not send piCtory configuration
                continue

            # fixme: Fehlerabfang bei Dateilesen
            with open(file_name, "rb") as fh:

                # Generate relative file name for transfer
                if dirselect == "":
                    sendname = os.path.basename(file_name)
                else:
                    # Append folder name on complete folder transfer to crate it on Revolution Pi
                    sendname = os.path.join(
                        folder_name,
                        file_name.replace(dirselect, "")[1:]
                    )

                # Try to find given plc start program in upload files
                if sendname == self.dc.get("plcprogram", ""):
                    plc_program_not_in_upload = False

                ustatus = helper.cm.call_remote_function(
                    "plcupload", Binary(gzip.compress(fh.read())), sendname
                )
                if ustatus is None:
                    ec = -2
                    break
                elif not ustatus:
                    ec = -1
                    break

        if ec == 0:
            QtWidgets.QMessageBox.information(
                self, self.tr("Success"), self.tr(
                    "The PLC program was transferred successfully."
                )
            )
            self.lst_files = helper.cm.call_remote_function("get_filelist", default_value=[])
            self._load_settings(files_only=True)
            if plc_program_not_in_upload:
                QtWidgets.QMessageBox.warning(
                    self, self.tr("Information"), self.tr(
                        "Could not find the selected PLC start program in "
                        "uploaded files.\nThis is not an error, if the file "
                        "was already on the Revolution Pi. Check PLC start "
                        "program field"
                    )
                )

            if self.cbx_pictory.isChecked():
                if rscfile is not None:
                    self._upload_pictory(rscfile)
                else:
                    QtWidgets.QMessageBox.critical(
                        self, self.tr("Error"), self.tr(
                            "There is no piCtory configuration in this archive."
                        )
                    )

        elif ec == -1:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "The Revolution Pi could not process some parts of the transmission."
                )
            )

        elif ec == -2:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Errors occurred during transmission."
                )
            )

        remove_temp()

    # endregion # # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # region #      REGION: Control files

    @QtCore.pyqtSlot()
    def on_btn_pictory_download_pressed(self):
        """Download piCtory configuration."""
        if not helper.cm.connected:
            return

        diag_save = QtWidgets.QFileDialog(
            self, self.tr("Save piCtory file..."),
            os.path.join(
                helper.cm.program_last_dir_pictory,
                "{0}.rsc".format(helper.cm.name)
            ),
            self.tr("piCtory file (*.rsc);;All files (*.*)")
        )
        diag_save.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        diag_save.setDefaultSuffix("rsc")
        self.rejected.connect(diag_save.reject)

        if diag_save.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_save.selectedFiles()) != 1:
            return

        filename = diag_save.selectedFiles()[0]
        helper.cm.program_last_dir_pictory = os.path.dirname(filename)
        bin_buffer = helper.cm.call_remote_function("get_pictoryrsc")  # type: Binary
        if bin_buffer is None:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Could not load piCtory file from Revolution Pi."
                )
            )
        else:
            fh = open(filename, "wb")
            fh.write(bin_buffer.data)
            fh.close()

            QtWidgets.QMessageBox.information(
                self, self.tr("Success"), self.tr(
                    "piCtory configuration successfully loaded and saved to:\n{0}."
                ).format(filename)
            )

    @QtCore.pyqtSlot()
    def on_btn_pictory_upload_pressed(self):
        if not helper.cm.connected:
            return

        diag_open = QtWidgets.QFileDialog(
            self, self.tr("Upload piCtory file..."),
            helper.cm.program_last_pictory_file,
            self.tr("piCtory file (*.rsc);;All files (*.*)")
        )
        diag_open.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        diag_open.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        diag_open.setDefaultSuffix("rsc")
        self.rejected.connect(diag_open.reject)

        if diag_open.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_open.selectedFiles()) != 1:
            return

        self._upload_pictory(diag_open.selectedFiles()[0])

    @QtCore.pyqtSlot()
    def on_btn_procimg_download_pressed(self):
        """Download process image."""
        if not helper.cm.connected:
            return

        diag_save = QtWidgets.QFileDialog(
            self,
            self.tr("Save piControl file..."),
            os.path.join(
                helper.cm.program_last_dir_picontrol,
                "{0}.img".format(helper.cm.name)
            ),
            self.tr("Process image file (*.img);;All files (*.*)")
        )
        diag_save.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        diag_save.setDefaultSuffix("img")
        self.rejected.connect(diag_save.reject)

        if diag_save.exec() != QtWidgets.QFileDialog.AcceptSave or len(diag_save.selectedFiles()) != 1:
            return

        filename = diag_save.selectedFiles()[0]
        helper.cm.program_last_dir_picontrol = os.path.dirname(filename)
        bin_buffer = helper.cm.call_remote_function("get_procimg")  # type: Binary

        if bin_buffer is None:
            QtWidgets.QMessageBox.critical(
                self, self.tr("Error"), self.tr(
                    "Could not load process image from Revolution Pi."
                )
            )
        else:
            fh = open(filename, "wb")
            fh.write(bin_buffer.data)
            fh.close()

            QtWidgets.QMessageBox.information(
                self, self.tr("Success"), self.tr(
                    "Process image successfully loaded and saved to:\n{0}."
                ).format(filename)
            )

    # endregion # # # # #
