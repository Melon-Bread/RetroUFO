#!/usr/bin/env python3
"""
Grabs the latest version of every libretro core from the build bot.
"""

__author__ = "Melon Bread"
__version__ = "0.8.0"
__license__ = "MIT"

import sys

from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QComboBox, QCheckBox, QPushButton, QFileDialog, \
    QVBoxLayout, QTextEdit


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle('RetroUFO')

        # Create widgets
        self.chkboxPlatformDetect = QCheckBox('Platform Auto-Detect')
        self.chkboxPlatformDetect.setChecked(True)
        self.chkboxPlatformDetect.stateChanged.connect(self.auto_platform)

        self.cmbboxPlatform = QComboBox()
        self.cmbboxPlatform.setEnabled(False)
        self.cmbboxPlatform.setEditable(False)
        self.cmbboxPlatform.addItem('Linux')
        self.cmbboxPlatform.addItem('Windows')

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

        self.btnGrabCores = QPushButton('Grab Cores')
        self.btnGrabCores.clicked.connect(self.download_cores())

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.chkboxPlatformDetect)
        layout.addWidget(self.cmbboxPlatform)
        layout.addWidget(self.chkboxLocationDetect)
        layout.addWidget(self.leditCoreLocation)
        layout.addWidget(self.btnCoreLocation)
        layout.addWidget(self.teditLog)
        layout.addWidget(self.btnGrabCores)

        # Set dialog layout
        self.setLayout(layout)

    def auto_platform(self):
        if self.chkboxPlatformDetect.isChecked():
            self.cmbboxPlatform.setEnabled(False)
        else:
            self.cmbboxPlatform.setEnabled(True)

    def auto_location(self):
        if self.chkboxLocationDetect.isChecked():
            self.leditCoreLocation.setEnabled(False)
            self.btnCoreLocation.setEnabled(False)
        else:
            self.leditCoreLocation.setEnabled(True)
            self.btnCoreLocation.setEnabled(True)

    def choose_location(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Target Location', '/home')

        self.leditCoreLocation.insert(directory)

    def download_cores(self):
        pass


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
