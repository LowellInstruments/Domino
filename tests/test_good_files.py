from gui import converter_window
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtCore import Qt
import sys
import pytest
from tests.utils import compare_files
from mat.data_converter import default_parameters


PARAMETERS = [
    (
        'file1.lid',
        ['AccelMag', 'Temperature'],
        {'average': False}),
    (
        'file1.lid',
        ['AccelMag', 'Temperature'],
        {'average': False, 'time_format': 'legacy'}),
    (
        'file1.lid',
        ['YawPitchRoll', 'Temperature'],
        {'average': True, 'time_format': 'iso8601', 'output_type': 'ypr'}),
    (
        'file1.lid',
        ['YawPitchRoll'],
        {'average': True, 'time_format': 'legacy', 'output_type': 'ypr'}),
    (
        'file1.lid',
        ['YawPitchRoll'],
        {'average': False, 'time_format': 'iso8601', 'output_type': 'ypr'}),
    (
        'file1.lid',
        ['YawPitchRoll'],
        {'average': False, 'time_format': 'legacy', 'output_type': 'ypr'}),
    (
        'file1.lid',
        ['Heading'],
        {'average': False, 'time_format': 'iso8601', 'output_type': 'compass', 'declination': 0}),
    (
        'file1.lid',
        ['Heading'],
        {'average': False, 'time_format': 'iso8601', 'output_type': 'compass', 'declination': 45}),
    (
        'file1.lid',
        ['Heading'],
        {'average': False, 'time_format': 'iso8601', 'output_type': 'compass', 'declination': -70})
]


def expected_filename(filename, this_type, params):
    types_map = {
        'AccelMag': 'MA',
        'Temperature': 'T',
        'YawPitchRoll': 'YPR',
        'Heading': 'HEADING'}
    stem = Path(filename).stem
    type = types_map[this_type]
    time = 'iso' if params['time_format'] == 'iso8601' else 'legacy'
    avg = 'yes' if params['average'] is True else 'no'
    filename_parts = [stem, type, time, avg]
    if params['declination'] != 0:
        filename_parts.append(str(params['declination']))
    return '_'.join(filename_parts) + '.expect'


app = QApplication(sys.argv)


def full_path(file_name):
    return Path(__file__).parent / 'good_files' / file_name


@pytest.fixture
def new_ui(mocker):
    overwrite_mock = mocker.patch(
        'gui.converter.file_converter.FileConverter._process_overwrite')
    overwrite_mock.return_value = ('yes_to_all', True)
    ui = converter_window.ConverterFrame()
    frame = QFrame()
    ui.setupUi(frame)
    return ui


def compare(reference_file, test_file):
    ref_path = full_path(reference_file)
    test_path = full_path(test_file)
    compare_files(ref_path, test_path)


@pytest.mark.parametrize('input,types,params', PARAMETERS)
def test_parameters(input, types, params, new_ui, qtbot, mocker):
    file = full_path(input)
    all_params = default_parameters()
    all_params.update(params)
    file_mock = mocker.patch('gui.converter_window.dialogs.open_lid_file')
    file_mock.return_value = [[str(file)], None]
    new_ui._read_output_options = lambda: all_params
    with qtbot.waitSignal(new_ui.file_loader.finished_signal, timeout=1000):
        qtbot.mouseClick(new_ui.pushButton_add, Qt.LeftButton)
    complete_signal = new_ui.converter.conversion_complete
    with qtbot.waitSignal(complete_signal, timeout=4000) as blocker:
        # ui.convert_files()
        qtbot.mouseClick(new_ui.pushButton_convert, Qt.LeftButton)
    for t in types:
        expect = expected_filename(input, t, all_params)
        converted = '{}_{}.csv'.format(input[:-4], t)
        compare(expect, converted)
