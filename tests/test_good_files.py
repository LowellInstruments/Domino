from gui.converter import ConverterFrame
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtCore import Qt
import sys


def reference_file(file_name):
    return Path(__file__).parent / 'good_files' / file_name


def test_calibrate(qtbot):
    app = QApplication(sys.argv)
    ui = ConverterFrame()
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

