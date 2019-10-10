from gui import converter_window
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtCore import Qt
import sys
import pytest
from tests.utils import compare_files


def file(file_name):
    return Path(__file__).parent / 'good_files' / file_name


def app_data():
    return {'time_format': 'iso8601',
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
    return mocker.patch('gui.converter_window.appdata')


@pytest.fixture
def mocked_set_userdata():
    return mocker.patch('gui.converter.file_loader.appdata')


@pytest.fixture
def new_ui(mocked_get_userdata):
    def _appdata(this_appdata):
        mocked_get_userdata.return_value = this_appdata
        ui = converter_window.ConverterFrame()
        frame = QFrame()
        ui.setupUi(frame)
        return ui
    return _appdata


def test_convert_file(qtbot, new_ui, mocker):
    open_file_mock = mocker.patch('gui.converter_window.dialogs.open_lid_file')
    open_file_mock.return_value = [[str(file('Calibrate.lid'))], None]
    ui = new_ui(app_data())
    with qtbot.wait_signal(ui.file_loader.file_loader.load_complete_signal):
        qtbot.mouseClick(ui.pushButton_add, Qt.LeftButton)

