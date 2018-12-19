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


class TestQueryThread(TestCase):
    @patch('gui.start_stop.LoggerController')
    def test_refresh(self, fake_logger_controller):
        thread = LoggerQueryThread({})

    @patch('gui.start_stop.LoggerQueryThread')
    def test_not_connected_gui_strings(self, fake_query):
        app = QApplication(sys.argv)
        Frame = QFrame()
        ui = StartStopFrame()
        ui.setupUi(Frame)
        for widget_name, string in start_stop_clear.DEFAULTS:
            widget = getattr(ui, widget_name)
            widget.setText('Nothing burger')
            assert(widget.text() != string)
        start_stop_clear.clear_gui(ui)
        for widget_name, string in start_stop_clear.DEFAULTS:
            widget = getattr(ui, widget_name)
            assert(widget.text() == string)
        fake_query.assert_called()


    # @patch('gui.start_stop.LoggerController')
    # def test_run(self, fake_logger_controller):
    #     type(fake_logger_controller).is_connected = \
    #         PropertyMock(return_value=True)
    #     thread = LoggerQueryThread({})
    #     #thread.start()
    #
    # @patch('gui.start_stop.TimeUpdater.sleep', side_effect=InterruptedError)
    # def test_time_updater(self, fake_time):
    #     updater = TimeUpdater()
    #     slot = MagicMock()
    #     updater.time_signal.connect(slot)
    #     updater.start()



        # app = QApplication(sys.argv)
        # Frame = QFrame()
        # ui = StartStopFrame()
        # ui.setupUi(Frame)


        # assert ("%.3f" % EXAMPLE_READINGS['ax'][0] ==
        #         container.start_stop_frame.tableWidget.item(0, 2).text())
        # assert (str(int(EXAMPLE_READINGS['mx'][0])) ==
        #         container.start_stop_frame.tableWidget.item(3, 2).text())

#     def test_empty_refresh(self):
#         with _get_sensor_readings_patch(return_value={}):
#             container = Container(QMainWindow())
#             container.refresher.refresh()
#             assert ('No' ==
#                     container.start_stop_frame.tableWidget.item(0, 1).text())
#
#     def test_temp_interval_changed(self):
#         with _get_sensor_readings_patch(return_value={}):
#             container = Container(QMainWindow())
#             frame = container.setup_frame
#             interval_widget = frame.comboBox_temp_interval
#             initial_tri = frame.setup_file._setup_dict['TRI']
#             index = interval_widget.currentIndex()
#             interval_widget.setCurrentIndex(index + 1)
#             container.setup_frame.interval_changed('temperature')
#             assert initial_tri != frame.setup_file._setup_dict['TRI']
#
#     def test_orient_interval_changed(self):
#         with _get_sensor_readings_patch(return_value={}):
#             container = Container(QMainWindow())
#             frame = container.setup_frame
#             interval_widget = frame.comboBox_orient_interval
#             initial_tri = frame.setup_file._setup_dict['ORI']
#             index = interval_widget.currentIndex()
#             interval_widget.setCurrentIndex(index + 1)
#             container.setup_frame.interval_changed('orientation')
#             assert initial_tri != frame.setup_file._setup_dict['ORI']
#
#     def test_refresh_error(self):
#         with _get_sensor_readings_patch(new=_raise_runtime_error):
#             container = Container(QMainWindow())
#             container.refresher.refresh()
#             assert ('No' ==
#                     container.start_stop_frame.tableWidget.item(0, 1).text())
#
#     def test_readings_are_none(self):
#         with _get_sensor_readings_patch(return_value=None):
#             container = Container(QMainWindow())
#             container.refresher.refresh()
#             assert ('No' ==
#                     container.start_stop_frame.tableWidget.item(0, 1).text())
#
#
# def _raise_runtime_error(unused):
#     raise RuntimeError
#
#
# @contextmanager
# def _get_sensor_readings_patch(**kwargs):
#     with patch("gui.sensor_refresher.LoggerController.open_port",
#                return_value=True):
#         with patch("gui.sensor_refresher.LoggerController.get_sensor_readings",
#                    **kwargs):
#             yield
