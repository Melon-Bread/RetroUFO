#!/usr/bin/env python3
"""
Grabs the latest version of every libretro core from the build bot.
"""

__author__ = "Melon Bread"
__version__ = "0.9.0"
__license__ = "MIT"

import os
import platform
import sys
import zipfile
from shutil import rmtree
from urllib.request import urlretrieve

from PySide2.QtCore import QThread, Signal
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                               QFileDialog, QLineEdit, QPushButton, QTextEdit,
                               QVBoxLayout, QMessageBox)

URL = 'https://buildbot.libretro.com/nightly'

# These are the default core locations with normal RetroArch installs based off of 'retroarch.default.cfg`
CORE_LOCATION = {
    'linux': '{}/.config/retroarch/cores'.format(os.path.expanduser('~')),
    'apple/osx': '/Applications/RetroArch.app/Contents/Resources/cores',  # macOS
    'windows': '{}/AppData/Roaming/RetroArch/cores'.format(os.path.expanduser('~'))
}


class GrabThread(QThread):
    add_to_log = Signal(str)
    lock = Signal(bool)

    def __init__(self, _platform, _architecture, _location):
        QThread.__init__(self)
        self.platform = _platform
        self.architecture = _architecture
        self.location = _location

    def __del__(self):
        self.wait()

    def run(self):
        self.lock.emit(True)
        self.add_to_log.emit('~Starting UFO Grabber~\n')
        self.download_cores(self.platform, self.architecture)
        self.extract_cores(self.location)
        self.lock.emit(False)

    def create_dir(self, _name):
        if not os.path.isdir(_name):
            os.makedirs(_name)

    def obtain_core_list(self, _platform, _architecture):
        urlretrieve(
            '{}/{}/{}/latest/.index-extended'.format(
                URL, _platform, _architecture), 'cores/index')
        self.add_to_log.emit('Obtained core index!\n')

    def download_cores(self, _platform, _architecture):
        """ Downloads every core to the working directory """

        cores = []

        # Makes core directory to store archives if needed
        self.create_dir("cores")

        # Downloads a list of all the cores available
        self.obtain_core_list(_platform, _architecture)
        
        # Adds all the core's file names to a list
        core_index = open('cores/index')

        for line in core_index:
            file_name = line.split(' ', 2)[2:]
            cores.append(file_name[0].rstrip())
        core_index.close()
        cores.sort()

        # Downloads each core from the list
        self.add_to_log.emit('Downloading Cores\n')
        for core in cores:
            urlretrieve(
                '{}/{}/{}/latest/{}'.format(URL, _platform, _architecture,
                                            core), 'cores/{}'.format(core))
            self.add_to_log.emit('Downloaded {} ...'.format(core))

        # Removes index file for easier extraction
        os.remove('cores/index')

    def extract_cores(self, _location):
        """ Extracts each downloaded core to the RA core directory """
        self.add_to_log.emit('\nExtracting all cores to: {}\n'.format(_location))

        for file in os.listdir('cores'):
            archive = zipfile.ZipFile('cores/{}'.format(file))
            archive.extractall(_location)
            self.add_to_log.emit('Extracted {} ...'.format(file))


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle('RetroUFO')

        # Create widgets
        self.chkboxPlatformDetect = QCheckBox('Platform Auto-Detect')
        self.chkboxPlatformDetect.setChecked(True)
        self.chkboxPlatformDetect.stateChanged.connect(self.auto_detect)

        self.cmbboxPlatform = QComboBox()
        self.cmbboxPlatform.setEnabled(False)
        self.cmbboxPlatform.setEditable(False)
        self.cmbboxPlatform.addItem('Linux')
        self.cmbboxPlatform.addItem('macOS')
        self.cmbboxPlatform.addItem('Windows')

        self.cmbboxArchitecture = QComboBox()
        self.cmbboxArchitecture.setEnabled(False)
        self.cmbboxArchitecture.setEditable(False)
        self.cmbboxArchitecture.addItem('x86')
        self.cmbboxArchitecture.addItem('x86_64')

        self.chkboxLocationDetect = QCheckBox('Core Location Auto-Detect')
        self.chkboxLocationDetect.setChecked(True)
        self.chkboxLocationDetect.stateChanged.connect(self.auto_location)

        self.leditCoreLocation = QLineEdit('')
        self.leditCoreLocation.setEnabled(False)

        self.btnCoreLocation = QPushButton('...')
        self.btnCoreLocation.setEnabled(False)
        self.btnCoreLocation.clicked.connect(self.choose_location)

        self.teditLog = QTextEdit()
        self.teditLog.setReadOnly(True)

        self.tcsrLog = QTextCursor(self.teditLog.document())

        self.chkboxKeepDownload = QCheckBox('Keep Downloaded Cores')
        self.chkboxKeepDownload.setChecked(False)

        self.btnGrabCores = QPushButton('Grab Cores')
        self.btnGrabCores.clicked.connect(self.grab_cores)

        # Create layout and add widgets
        self.formLayout = QVBoxLayout()
        self.formLayout.addWidget(self.chkboxPlatformDetect)
        self.formLayout.addWidget(self.cmbboxPlatform)
        self.formLayout.addWidget(self.cmbboxArchitecture)
        self.formLayout.addWidget(self.chkboxLocationDetect)
        self.formLayout.addWidget(self.leditCoreLocation)
        self.formLayout.addWidget(self.btnCoreLocation)
        self.formLayout.addWidget(self.teditLog)
        self.formLayout.addWidget(self.chkboxKeepDownload)
        self.formLayout.addWidget(self.btnGrabCores)

        # Set dialog layout
        self.setLayout(self.formLayout)

    def auto_detect(self):
        if self.chkboxPlatformDetect.isChecked():
            self.cmbboxPlatform.setEnabled(False)
            self.cmbboxArchitecture.setEnabled(False)
        else:
            self.cmbboxPlatform.setEnabled(True)
            self.cmbboxArchitecture.setEnabled(True)

    def auto_location(self):
        if self.chkboxLocationDetect.isChecked():
            self.leditCoreLocation.setEnabled(False)
            self.btnCoreLocation.setEnabled(False)
        else:
            self.leditCoreLocation.setEnabled(True)
            self.btnCoreLocation.setEnabled(True)

    def choose_location(self):
        directory = QFileDialog.getExistingDirectory(
            self, 'Choose Target Location', os.path.expanduser('~'))

        self.leditCoreLocation.insert(directory)

    def update_log(self, _info):
        self.teditLog.insertPlainText('{}\n'.format(_info))

        # Auto scrolling on log UI
        self.teditLog.moveCursor(QTextCursor.End)

    def lock_ui(self, _lock):
        # Cycle through each widget and disable it except for log UI
        widgets = (self.formLayout.itemAt(i).widget() for i in range(self.formLayout.count()))
        for widget in widgets:
            if isinstance(widget, QTextEdit):
                pass
            else:
                widget.setDisabled(_lock)
                # Have to run these to make sure only the correct things unlock after grab thread
                self.auto_detect()
                self.auto_location()


    def grab_cores(self):
        """ Where the magic happens """
        if not self.chkboxKeepDownload.isChecked():
            self.clean_up()

        # TODO: Lock (disable) the UI elements while grabbing cores

        platform = self.get_platform()
        architecture = self.get_architecture()
        location = self.get_location()

        self.grab = GrabThread(platform, architecture, location)
        self.grab.add_to_log.connect(self.update_log)
        self.grab.lock.connect(self.lock_ui)
        self.grab.start()

    def get_platform(self):
        """ Gets the Platform and Architecture if not supplied """

        if not self.chkboxPlatformDetect.isChecked():
            if self.cmbboxPlatform.currentText() == 'macOS':
                return 'apple/osx'  # macOS
            else:
                return self.cmbboxPlatform.currentText().lower()
        else:
            if platform.system() == 'Linux':
                return 'linux'
            elif platform.system() == 'Darwin':  # macOS
                return 'apple/osx'
            elif platform.system() == 'Windows' or 'MSYS_NT' in platform.system():  # Checks for MSYS environment as well
                return 'windows'
            else:
                msgBox = QMessageBox.warning(self, 'Error', 'Platform not found or supported!', QMessageBox.Ok)
                msgBox.exec_()

    def get_architecture(self):
        """ Gets the Platform and Architecture if not supplied """

        if '64' in platform.architecture()[0]:
            return 'x86_64'

        elif '32' in platform.architecture()[0]:
            return 'x86'
        else:
            msgBox = QMessageBox.warning(self, 'Error', 'Architecture not found or supported', QMessageBox.Ok)
            msgBox.exec_()

    def get_location(self):
        if not self.chkboxLocationDetect.isChecked():
            return self.leditCoreLocation.text()
        else:
            return CORE_LOCATION[self.get_platform()]

    def clean_up(self):
        """ Removes all the downloaded files """
        if os.listdir('cores'):
            rmtree('cores/')


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
