from numpy import ndarray
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from mat.logger_controller import LoggerController


SENSOR_ORDER = ['ax', 'ay', 'az', 'mx', 'my', 'mz', 'temp', 'batt']
INT_SENSORS = ['mx', 'my', 'mz']


class SensorRefresher(QTimer):
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
        return _format_value(sensor, reading[0])
    return _format_value(sensor, reading)


def _format_value(sensor, value):
    if value == '':
        return value
    if sensor in INT_SENSORS:
        return str(int(value))
    return "%.3f" % value
