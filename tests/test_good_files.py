from gui import converter
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtCore import Qt
import sys
from mock import patch


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


@patch('gui.converter.appdata.get_userdata', return_value=app_data)
@patch('gui.converter.appdata.set_userdata')
def test_calibrate(set_appdata, get_appdata, qtbot):

    app = QApplication(sys.argv)
    ui = converter.ConverterFrame()
    frame = QFrame()
    ui.setupUi(frame)
    qtbot.add_widget(app)
    load_signal = ui.converter_table.file_loader.load_complete_signal
    with qtbot.waitSignal(load_signal) as blocker:
        file = reference_file('ScenarioA.lid')
        ui.converter_table.file_loader.load_files([str(file)])
    complete_signal = ui.converter_table.conversion.conversion_complete
    with qtbot.waitSignal(complete_signal, timeout=10000) as blocker:
        qtbot.mouseClick(ui.pushButton_convert, Qt.LeftButton)
