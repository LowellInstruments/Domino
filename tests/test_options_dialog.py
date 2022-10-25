import pytest
import sys
from PyQt5.QtWidgets import QApplication, QFrame, QDialog
from PyQt5.QtCore import Qt
from gui.options_dialog import OptionsDialog
from pathlib import Path


app = QApplication(sys.argv)


def file(file_name):
    return Path(__file__).parent / 'files' / file_name


def appdata():
    return {
    'time_format': 'legacy',
    'average_bursts': True,
    'output_format': 'csv',
    'split': 'Do not split output files'
}

@pytest.fixture
def mocked_get_userdata(mocker):
    return mocker.patch('gui.options_dialog.QSettings.value')


@pytest.fixture
def mocked_set_userdata(mocker):
    return mocker.patch('gui.options_dialog.QSettings.setValue')


@pytest.fixture
def new_ui(mocked_get_userdata):
    def _appdata(this_appdata):
        mocked_get_userdata.return_value = this_appdata
        frame = QFrame()
        ui = OptionsDialog(frame)
        return ui
    return _appdata


def test_open_options_dialog(new_ui):
    dialog = new_ui(appdata())
    assert dialog.ui.radioButton_csv.isChecked()
    assert not dialog.ui.radioButton_hdf5.isChecked()
    assert dialog.ui.comboBox_split.currentIndex() == 0
    assert dialog.ui.checkBox_average_bursts.isChecked() is True


def test_change_output_format(qtbot, new_ui):
    dialog = new_ui(appdata())
    assert dialog.ui.comboBox_split.isEnabled() is True
    qtbot.mouseClick(dialog.ui.radioButton_hdf5, Qt.LeftButton)
    assert dialog.ui.comboBox_split.isEnabled() is False
    time_group = dialog.ui.buttonGroup.buttons()
    for button in time_group:
        assert button.isEnabled() is False


def test_save(new_ui, mocked_set_userdata, mocker, qtbot):
    app_data = appdata()
    app_data['time_format'] = 'iso8601'
    app_data['average_bursts'] = False
    dialog = new_ui(app_data)
    qtbot.mouseClick(dialog.ui.pushButton_save, Qt.LeftButton)
    expected = {
        'time_format': 'iso8601',
        'average_bursts': False,
        'output_format': 'csv',
        'split': 'Do not split output files',
        'custom_cal': None,
        'voltage': False
    }
    assert [mocker.call('output_options', expected)] == \
           mocked_set_userdata.call_args_list


def test_custom_cal_enable_disable(new_ui, qtbot):
    dialog = new_ui(appdata())
    custom_cal_widgets = [dialog.ui.lineEdit_custom_cal,
                          dialog.ui.pushButton_browse]
    for widget in custom_cal_widgets:
        assert widget.isEnabled() is False
    qtbot.mouseClick(dialog.ui.radioButton_custom_cal, Qt.LeftButton)
    for widget in custom_cal_widgets:
        assert widget.isEnabled() is True


def test_open_custom_cal_file(new_ui, qtbot, mocker):
    file_mock = mocker.patch('gui.options_dialog.QFileDialog.getOpenFileName')
    path = str(file('v3_calibration.txt'))
    file_mock.return_value = [path, '']
    dialog = new_ui(appdata())
    qtbot.mouseClick(dialog.ui.radioButton_custom_cal, Qt.LeftButton)
    qtbot.mouseClick(dialog.ui.pushButton_browse, Qt.LeftButton)
    assert dialog.ui.lineEdit_custom_cal.text() == path


def test_open_custom_bad_cal_file(new_ui, qtbot, mocker):
    file_mock = mocker.patch('gui.options_dialog.QFileDialog.getOpenFileName')
    error_mock = mocker.patch(
        'gui.options_dialog.QMessageBox.warning')
    path = str(file('v3_calibration_missing_value.txt'))
    file_mock.return_value = [path, '']
    dialog = new_ui(appdata())
    qtbot.mouseClick(dialog.ui.radioButton_custom_cal, Qt.LeftButton)
    qtbot.mouseClick(dialog.ui.pushButton_browse, Qt.LeftButton)
    error_mock.assert_called_once()


def test_open_custom_cal_canceled(new_ui, qtbot, mocker):
    file_mock = mocker.patch('gui.options_dialog.QFileDialog.getOpenFileName')
    file_mock.return_value = ['', '']
    dialog = new_ui(appdata())
    qtbot.mouseClick(dialog.ui.radioButton_custom_cal, Qt.LeftButton)
    qtbot.mouseClick(dialog.ui.pushButton_browse, Qt.LeftButton)
    assert dialog.ui.lineEdit_custom_cal.text() == ''


def test_canceled(new_ui, qtbot, mocker):
    close_mock = mocker.patch('gui.options_dialog.OptionsDialog.close')
    dialog = new_ui(appdata())
    qtbot.mouseClick(dialog.ui.pushButton_cancel, Qt.LeftButton)
    qtbot.wait(100)
    close_mock.assert_called_once()
