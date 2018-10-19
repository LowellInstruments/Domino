from numpy import ndarray
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidgetItem,
)
from PyQt5.QtCore import (
    QRect,
    QSize,
    QTimer,
)
from gui.container_ui import Ui_MainWindow
from gui.start_stop_ui import Ui_Frame as StartStopFrame
from gui.converter_ui import Ui_Frame as ConverterFrame
from gui.setup import SetupFrame
from mat.logger_controller import LoggerController
import sys


SENSOR_ORDER = ['ax', 'ay', 'az', 'mx', 'my', 'mz', 'temp', 'batt']


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
        self.refresh = SensorRefresh(self.start_stop_frame.tableWidget)

    def create_sensor_widgets(self):
        for index, sensor in enumerate(SENSOR_ORDER):
            self.add_item(index, 1)
            self.add_item(index, 2)

    def add_item(self, row, col):
        item = QTableWidgetItem()
        self.start_stop_frame.tableWidget.setItem(row, col, item)


class SensorRefresh(QTimer):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self._translate = QApplication.translate
        self.logger_controller = LoggerController()
        self.timeout.connect(self.refresh)
        self.start(1000)

    def refresh(self):
        readings = {}
        try:
            self.logger_controller.open_port()
            readings = self.logger_controller.get_sensor_readings()
        except RuntimeError:
            pass
        for index, sensor in enumerate(SENSOR_ORDER):
            self._set_item_text(index, 1, enabled_string(sensor, readings))
            self._set_item_text(index, 2, value_string(sensor, readings))
        self.logger_controller.close()

    def _set_item_text(self, row, col, value):
        item = self.widget.item(row, col)
        item.setText(self._translate("Frame", value))


def enabled_string(sensor, readings):
    if sensor in readings:
        return "Yes"
    return "No"


def value_string(sensor, readings):
    reading = readings.get(sensor, '')
    if isinstance(reading, ndarray):
        return str(reading[0])
    return str(reading)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()  # create a main window
    ui = Container(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
