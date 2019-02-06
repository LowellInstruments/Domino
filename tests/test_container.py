import sys
from unittest import TestCase
from unittest.mock import patch

from numpy import array
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame
)
from gui.start_stop import LoggerQueryThread, TimeUpdater, StartStopFrame
from gui import start_stop_clear

app = QApplication(sys.argv)

EXAMPLE_READINGS = {
    'light_raw': 0,
    'light': array([100.]),
    'pressure_raw': 0,
    'pressure': array([3.]),
    'temp_raw': 34521,
    'ax_raw': 3832,
    'ay_raw': -856,
    'az_raw': 64,
    'mx_raw': 354,
    'my_raw': 749,
    'mz_raw': 462,
    'batt': 3.698,
    'ax': array([-0.97425495]),
    'ay': array([0.22238327]),
    'az': array([-0.01883975]),
    'mx': array([-727.26475252]),
    'my': array([7.88806673]),
    'mz': array([60.46760516]),
    'temp': array([22.57383603])
}
EMPTY_READINGS = {}
SENSORS_COMMAND = {'get_sensor_readings':
                       {'interval': 100, 'update_fcn': 'Sensors', 'init': []}}
LOGGER_INFO = ('logger_info', {'SN': '9987654', 'CA': 24.0, 'BA': 3200,
                               'MN': 'MAT-1', 'DP': 16, 'PC': '0'})


class FakeSerial:
    def __init__(self):
        self.is_connected = False
        self.calls = 0

    def open_port(self, com_port=None):
        self.is_connected = True
        return self.is_connected

    def get_sensor_readings(self):
        self.is_connected = False
        return EXAMPLE_READINGS
