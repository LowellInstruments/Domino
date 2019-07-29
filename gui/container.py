from PyQt5.QtGui import (
    QIcon,
    QPixmap,
    QIcon
)
from PyQt5.QtWidgets import (
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import (
    QRect,
    QSize,
)
from gui.container_ui import Ui_MainWindow
from gui.start_stop import StartStopFrame
from gui.converter import ConverterFrame
from gui.setup import SetupFrame
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from mat.version_check import VersionChecker


class Container(Ui_MainWindow):
    def __init__(self, window):
        self.version = '0.6.0.1'
        self.window = window
        self.setupUi(window)
        self.window.closeEvent = self.closeEvent
        self.converter_frame = ConverterFrame()
        self.converter_frame.setupUi(self.frame_convert)
        self.setup_frame = SetupFrame()
        self.setup_frame.setupUi(self.frame_setup_file)
        self.start_stop_frame = StartStopFrame()
        self.start_stop_frame.setupUi(self.frame_start_stop)
        self.window.setWindowTitle('Lowell Instruments - Domino {}'
                                   .format(self.version))
        self.pushButton1 = QPushButton(self.centralwidget)
        x_pos = self.window.width() - 60
        self.pushButton1.setGeometry(QRect(x_pos, 5, 48, 48))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/icons/icons8-about-36.png"),
                       QIcon.Normal, QIcon.Off)
        self.pushButton1.setIcon(icon)
        self.pushButton1.setIconSize(QSize(36, 36))
        self.pushButton1.setFlat(True)
        self.pushButton1.setObjectName('about')
        self.pushButton1.clicked.connect(self.about)
        self.old_resize = self.window.resizeEvent
        self.window.resizeEvent = self.resizeEvent
        self.start_version_check()

    def start_version_check(self):
        self.version_check = VersionCheckerThread(self.window, self.version)
        self.version_check.new_version_signal.connect(self.new_version_found)
        self.version_check.start()

    def resizeEvent(self, event):
        self.old_resize(event)
        x_pos = self.window.width() - 60
        self.pushButton1.setGeometry(QRect(x_pos, 5, 48, 48))

    def closeEvent(self, event):
        if self.converter_frame.confirm_quit():
            event.accept()
        else:
            event.ignore()

    def about(self):
        logo = QIcon()
        logo.addPixmap(
            QPixmap(':/icons/icons/lowell_logo_fullsize.png'),
            QIcon.Normal, QIcon.Off)
        description = \
            '<a href="http://www.lowellinstruments.com">' \
            'Lowell Instruments LLC</a><br />' \
            'Domino' + '&trade; ' + self.version + '<br /><br />' \
            'Copyright 2018-2019 by Lowell Instruments, some ' \
            'rights reserved. <br />' \
            'Source code for this application is available under ' \
            'the GPLv3 License at ' \
            '<a href="https://github.com/LowellInstruments/Domino">' \
            'https://github.com/LowellInstruments/Domino</a><br />' \
            'Icons by <a href="http://icons8.com">icons8.com</a>'

        message = QMessageBox(self.window)
        message.setTextFormat(1)
        message.setIconPixmap(
            QPixmap(':/icons/icons/lowell_logo_fullsize.png'))
        message.setWindowTitle('About Domino')
        message.setText(description)
        message.exec_()

    def new_version_found(self):
        text = 'A new version of Domino is available. Please visit ' \
               'the Lowell Instruments ' \
               '<a href="https://lowellinstruments.com/downloads/">' \
               'downloads</a> page for the latest version.'
        message = QMessageBox(self.window)
        message.setTextFormat(1)
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('Update Available')
        message.setText(text)
        message.exec_()


class VersionCheckerThread(QThread):
    new_version_signal = pyqtSignal()

    def __init__(self, parent, version):
        super().__init__()
        self.version_checker = VersionChecker()
        self.version = version

    def run(self):
        if not self.version_checker.is_latest(self.version):
            self.new_version_signal.emit()
