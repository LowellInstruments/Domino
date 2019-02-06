from gui import converter
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtCore import Qt
import sys
from mock import patch, Mock
from contextlib import contextmanager
import pytest


app = QApplication(sys.argv)


def reference_file(file_name):
    return Path(__file__).parent / 'good_files' / file_name


app_data = {'time_format': 'iso8601',
            'average_bursts': True,
            'output_format': 'csv',
            'split': 'Do not split output files',
            'output_type': 'Discrete Channels',
            'meter_model': 'TCM-1 - 0 ballast - Fresh water',
            'same_directory': True,
            'output_directory': '',
            'declination': 0.0,
            'last_directory': '',
            'custom_cal': '',
            'setup_file_directory': ''}


@pytest.fixture
def mocked_get_userdata(mocker):
    return mocker.patch('gui.converter.appdata.get_userdata')


@pytest.fixture
def mocked_set_userdata(mocker):
    return mocker.patch('gui.converter.appdata.set_userdata')


@pytest.fixture
def new_ui(mocked_get_userdata, mocked_set_userdata):
    def _appdata(this_appdata):
        mocked_get_userdata.return_value = this_appdata
        ui = converter.ConverterFrame()
        frame = QFrame()
        ui.setupUi(frame)
        return ui
    return _appdata


def load_and_convert_file(file, ui, bot):
    file = reference_file(file)
    load_signal = ui.converter_table.file_loader.load_complete_signal
    with bot.waitSignal(load_signal, timeout=1000) as blocker:
        ui.converter_table.file_loader.load_files([str(file)])
    complete_signal = ui.converter_table.conversion.conversion_complete
    with bot.waitSignal(complete_signal, timeout=10000) as blocker:
        bot.mouseClick(ui.pushButton_convert, Qt.LeftButton)


def test_one(new_ui, qtbot):
    test_app_data = app_data.copy()
    test_app_data['time_format'] = 'elapsed'
    ui = new_ui(app_data)
    load_and_convert_file('ScenarioA.lid', ui, qtbot)

