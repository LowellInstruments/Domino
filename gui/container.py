from PyQt5.QtGui import (
    QIcon,
    QPixmap
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


class Container(Ui_MainWindow):
    def __init__(self, window):
        self.version = '0.0.1'
        self.window = window
        self.setupUi(window)
        self.window.closeEvent = self.closeEvent
        self.converter_frame = ConverterFrame()
        self.converter_frame.setupUi(self.frame_convert)
        self.setup_frame = SetupFrame()
        self.setup_frame.setupUi(self.frame_setup_file)
        self.start_stop_frame = StartStopFrame()
        self.start_stop_frame.setupUi(self.frame_start_stop)
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
        description = \
            '<a href="http://www.lowellinstruments.com">' \
            'Lowell Instruments LLC</a><br />' \
            'Domino ' + self.version + '&trade;<br /><br />' \
            'Copyright 2018-2019 by Lowell Instruments, some ' \
            'rights reserved. <br />' \
            'Source code for this application is available under ' \
            'the GPLv3 License at ' \
            '<a href="https://github.com/LowellInstruments/Domino">' \
            'https://github.com/LowellInstruments/Domino</a>'

        message = QMessageBox(self.window)
        message.setTextFormat(1)
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('About Domino')
        message.setText(description)
        message.exec_()
