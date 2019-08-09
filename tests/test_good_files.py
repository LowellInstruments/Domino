from gui import converter
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtCore import Qt
import sys
import pytest
from tests.utils import compare_files


PARAMETERS = [
    (
        'ScenarioA.lid',
        ['AccelMag', 'Temperature'],
        {'average_bursts': False}),
    (
        'ScenarioA.lid',
        ['AccelMag', 'Temperature'],
        {'average_bursts': False, 'time_format': 'elapsed'}),
    (
        'ScenarioB.lid',
        ['Temperature'],
        {'average_bursts': False}
    )
]



app = QApplication(sys.argv)


def full_path(file_name):
    return Path(__file__).parent / 'good_files' / file_name


@pytest.fixture
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
    file = full_path(file)
    load_signal = ui.converter_table.file_loader.load_complete_signal
    with bot.waitSignal(load_signal, timeout=1000) as blocker:
        ui.converter_table.file_loader.load_files([str(file)])
    complete_signal = ui.converter_table.conversion.conversion_complete
    with bot.waitSignal(complete_signal, timeout=10000) as blocker:
        bot.mouseClick(ui.pushButton_convert, Qt.LeftButton)


def compare(reference_file, test_file):
    ref_path = full_path(reference_file)
    test_path = full_path(test_file)
    compare_files(ref_path, test_path)


@pytest.mark.parametrize('input,types,params', PARAMETERS)
def test_parameters(input, types, params, new_ui, qtbot, app_data):
    app_data.update(params)
    ui = new_ui(app_data)
    load_and_convert_file(input, ui, qtbot)
    for t in types:
        expect = input[:-4] + '_' + t + '.expect'
        converted = input[:-4] + '_' + t + '.csv'
        compare(expect, converted)

# def test_scenarioA_heading_posix(new_ui, qtbot, app_data):
#     app_data['time_format'] = 'posix'
#     app_data['output_type'] = 'Compass Heading'
#     ui = new_ui(app_data)
#     load_and_convert_file('ScenarioA.lid', ui, qtbot)
#     compare('ScenarioA_Heading.expect', 'ScenarioA_Heading.csv')
#     compare('ScenarioA_T_POSIX.expect', 'ScenarioA_Temperature.csv')
#
#
# def test_ScenarioA_t_elapsed(new_ui, qtbot, app_data):
#     app_data['time_format'] = 'elapsed'
#     ui = new_ui(app_data)
#     load_and_convert_file('ScenarioA.lid', ui, qtbot)
#     compare('ScenarioA_T_Elapsed.expect', 'ScenarioA_Temperature.csv')
#
#
# def test_ScenarioA_t_iso(new_ui, qtbot, app_data):
#     app_data['time_format'] = 'iso8601'
#     ui = new_ui(app_data)
#     load_and_convert_file('ScenarioA.lid', ui, qtbot)
#     compare('ScenarioA_T_ISO.expect', 'ScenarioA_Temperature.csv')
#
#
# def test_ScenarioA_t_legacy(new_ui, qtbot, app_data):
#     app_data['time_format'] = 'legacy'
#     ui = new_ui(app_data)
#     load_and_convert_file('ScenarioA.lid', ui, qtbot)
#     compare('ScenarioA_T_legacy.expect', 'ScenarioA_Temperature.csv')