from gui._version import __version__
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
    QSettings
)
from gui.container_ui import Ui_MainWindow
from gui.start_stop import StartStopFrame
from gui.converter_window import ConverterFrame
from gui.setup_window import SetupFrame
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from mat.version_check import VersionChecker
import gui
import platform
from Socket_Singleton import Socket_Singleton, MultipleSingletonsError
from gui import dialogs
import sys
from time_checker import TimeChecker
from PyQt5.QtWidgets import QMessageBox, QCheckBox
import humanize


RICH_TEXT = 1


class Container(Ui_MainWindow):
    def __init__(self, window):
        self.version = __version__
        self.window = window
        gui.mw = self.window
        self.setupUi(window)
        try:
            Socket_Singleton(address="127.0.0.1", strict=False, port=19818)
        except MultipleSingletonsError:
            dialogs.inform('Warning', 'Domino is already running')
            sys.exit()
        # remove icons from tabs on Mac
        if platform.system() == 'Darwin':
            self.window.resize(900, 650)
            self.window.setMinimumSize(QSize(900, 650))
            for i in range(3):
                self.tabWidget.setTabIcon(i, QIcon())
            self.centralwidget.setContentsMargins(11, 25, 11, 11)

        self.window.setStyleSheet('font-size: 13px;')
        self.window.closeEvent = self.closeEvent
        self.converter_frame = ConverterFrame()
        self.converter_frame.setupUi(self.frame_convert)
        self.setup_frame = SetupFrame()
        self.setup_frame.setupUi(self.frame_setup_file)
        self.window.setMinimumSize(self.frame_setup_file.sizeHint())
        self.start_stop_frame = StartStopFrame()
        self.start_stop_frame.setupUi(self.frame_start_stop)
        self.window.setWindowTitle('Lowell Instruments - Domino')
        self.show_about_button()
        self.old_resize = self.window.resizeEvent
        self.window.resizeEvent = self.resizeEvent
        self.check_for_updates()

        self.app_data = QSettings().value('output_options', {}, type=dict)
        self.time_checker = TimeChecker()
        if QSettings().value('show_time_error', True, type=bool):
            self.check_time()

    def show_about_button(self):
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

    def check_time(self):
        self.time_checker.time_diff.connect(self.time_check_slot)
        self.time_checker.start()

    def check_for_updates(self):
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
            'Copyright 2018-2025 by Lowell Instruments LLC, some ' \
            'rights reserved. <br />' \
            'Source code for this application is available under ' \
            'the GPLv3 License at ' \
            '<a href="https://github.com/LowellInstruments/Domino">' \
            'https://github.com/LowellInstruments/Domino</a><br />' \
            'Icons by <a href="http://icons8.com">icons8.com</a>'

        message = QMessageBox(self.window)
        message.setTextFormat(RICH_TEXT)
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
        message.setTextFormat(RICH_TEXT)
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('Update Available')
        message.setText(text)
        message.exec_()

    def time_check_slot(self, offset):
        if abs(offset) > 5:
            msg = QMessageBox(parent=self.window)
            msg.setWindowTitle('Time Alert')
            offset_str = humanize.precisedelta(offset)
            msg.setText(f'Alert: The time on your computer differs from internet time by '
                        f'{offset_str}. We recommend synchronizing your computer clock to the '
                        f'internet to avoid time errors in the future.')
            msg.setIconPixmap(QPixmap(":/icons/icons/icons8-info-48.png"))
            checkbox = QCheckBox('Do not show this dialog again')
            msg.setCheckBox(checkbox)
            msg.exec_()
            if checkbox.isChecked():
                QSettings().setValue('show_time_error', False)

class VersionCheckerThread(QThread):
    new_version_signal = pyqtSignal()

    def __init__(self, parent, version):
        super().__init__()
        self.version_checker = VersionChecker()
        self.version = version

    def run(self):
        if not self.version_checker.is_latest(self.version):
            self.new_version_signal.emit()
