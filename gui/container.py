from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QPushButton,
    QTableWidgetItem,
)
from PyQt5.QtCore import (
    QRect,
    QSize,
)
from gui.sensor_refresher import (
    SENSOR_ORDER,
    SensorRefresher,
)
from gui.container_ui import Ui_MainWindow
from gui.start_stop_ui import Ui_Frame as StartStopFrame
from gui.converter import ConverterFrame
from gui.setup import SetupFrame


class Container(Ui_MainWindow):
    def __init__(self, window):
        self.window = window
        self.setupUi(window)
        self.converter_frame = ConverterFrame()
        self.converter_frame.setupUi(self.frame_convert)
        self.setup_frame = SetupFrame()
        self.setup_frame.setupUi(self.frame_setup_file)
        self.start_stop_frame = StartStopFrame()
        self.start_stop_frame.setupUi(self.frame_start_stop)
        self.pushButton1 = QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QRect(740, 5, 48, 48))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/icons/icons8-menu-48.png"),
                       QIcon.Normal, QIcon.Off)
        self.pushButton1.setIcon(icon)
        self.pushButton1.setIconSize(QSize(36, 36))
        self.pushButton1.setFlat(True)
        self.pushButton1.setObjectName('Preferences')
        self.create_sensor_widgets()
        self.refresher = SensorRefresher(self.start_stop_frame.tableWidget)

    def create_sensor_widgets(self):
        for index, sensor in enumerate(SENSOR_ORDER):
            self.add_item(index, 1)
            self.add_item(index, 2)

    def add_item(self, row, col):
        item = QTableWidgetItem()
        self.start_stop_frame.tableWidget.setItem(row, col, item)
