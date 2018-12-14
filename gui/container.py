from PyQt5.QtGui import (
    QIcon,
    QPixmap
)
from PyQt5.QtWidgets import (
    QPushButton,
    QTableWidgetItem,
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
        self.pushButton1.setGeometry(QRect(740, 5, 48, 48))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/icons/icons8-about-36.png"),
                       QIcon.Normal, QIcon.Off)
        self.pushButton1.setIcon(icon)
        self.pushButton1.setIconSize(QSize(36, 36))
        self.pushButton1.setFlat(True)
        self.pushButton1.setObjectName('about')
        self.pushButton1.clicked.connect(self.about)
    #     self.create_sensor_widgets()
    #     self.refresher = SensorRefresher(self.start_stop_frame.tableWidget)
    #
    # def create_sensor_widgets(self):
    #     for index, sensor in enumerate(GUI_SENSOR_INFO.keys()):
    #         self.add_item(index, 1)
    #         self.add_item(index, 2)
    #
    # def add_item(self, row, col):
    #     item = QTableWidgetItem()
    #     self.start_stop_frame.tableWidget.setItem(row, col, item)

    def closeEvent(self, event):
        if self.converter_frame.confirm_quit():
            event.accept()
        else:
            event.ignore()

    def about(self):
        description = 'Lowell Instruments LLC\n' \
                      'Domino ' + self.version + '\n\n' \
                      'www.lowellinstruments.com'
        QMessageBox.information(self.window, 'Domino', description)