import sys
from unittest import TestCase
from unittest.mock import patch
from contextlib import contextmanager

from numpy import array
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from gui.container import Container


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


class TestContainer(TestCase):
    def test_refresh(self):
        with _get_sensor_readings_patch(return_value=EXAMPLE_READINGS):
            container = Container(QMainWindow())
            container.refresher.refresh()
            assert (str(EXAMPLE_READINGS['ax'][0]) ==
                    container.start_stop_frame.tableWidget.item(0, 2).text())

    def test_empty_refresh(self):
        with _get_sensor_readings_patch(return_value={}):
            container = Container(QMainWindow())
            container.refresher.refresh()
            assert ('No' ==
                    container.start_stop_frame.tableWidget.item(0, 1).text())

    def test_temp_interval_changed(self):
        with _get_sensor_readings_patch(return_value={}):
            container = Container(QMainWindow())
            frame = container.setup_frame
            initial_tri = frame.setup_file._setup_dict['TRI']
            index = frame.interval_widget['temperature'].currentIndex()
            frame.interval_widget['temperature'].setCurrentIndex(index + 1)
            container.setup_frame.temp_interval_changed()
            assert initial_tri != frame.setup_file._setup_dict['TRI']

    def test_orient_interval_changed(self):
        with _get_sensor_readings_patch(return_value={}):
            container = Container(QMainWindow())
            frame = container.setup_frame
            initial_tri = frame.setup_file._setup_dict['ORI']
            index = frame.interval_widget['orientation'].currentIndex()
            frame.interval_widget['orientation'].setCurrentIndex(index + 1)
            container.setup_frame.orient_interval_changed()
            assert initial_tri != frame.setup_file._setup_dict['ORI']

    def test_refresh_error(self):
        with _get_sensor_readings_patch(new=_raise_runtime_error):
            container = Container(QMainWindow())
            container.refresher.refresh()
            assert ('No' ==
                    container.start_stop_frame.tableWidget.item(0, 1).text())


def _raise_runtime_error(unused):
    raise RuntimeError


@contextmanager
def _get_sensor_readings_patch(**kwargs):
    with patch("gui.sensor_refresher.LoggerController.open_port",
               return_value=True):
        with patch("gui.sensor_refresher.LoggerController.get_sensor_readings",
                   **kwargs):
            yield
