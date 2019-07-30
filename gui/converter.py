# GPLv3 License
# Copyright (c) 2019 Lowell Instruments, LLC, some rights reserved
from gui.converter_ui import Ui_Frame
from gui.options_dialog import OptionsDialog
from gui.converter_table import ConverterTable
from PyQt5 import QtWidgets
from mat import appdata, tiltcurve
import os
import sys
import glob
from operator import itemgetter
from mat.data_converter import default_parameters
from PyQt5.QtWidgets import QMessageBox
from mat.calibration_factories import make_from_calibration_file
from gui.gui_utils import show_error, is_float, error_message


OUTPUT_TYPE = {'Current': 'current',
               'Compass Heading': 'compass',
               'Yaw/Pitch/Roll': 'ypr'}


class AboutDeclination:
    TEXT = 'Magnetic declination is the angle between magnetic north and ' \
           'true north. This angle varies depending on position on the ' \
           'Earth\'s surface.' \
           '<br><br>In order for current and compass data to ' \
           'be converted to geographic coordinates, you must enter the ' \
           'declination at your deployment site, otherwise the heading and ' \
           'velocity components will be relative to magnetic north.' \
           '<br><br>Declination can be found using a calculator such as ' \
           '<a href="http://ngdc.noaa.gov/geomag-web">NOAA\'s Declination ' \
           'Calculator</a><br /><br />' \
           'Values must be in the range [-180, 180]<br /> East is positive.'

    def __init__(self, parent):
        self.parent = parent

    def show(self):
        message = QMessageBox(self.parent)
        message.setTextFormat(1)
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('About Declination')
        message.setText(self.TEXT)
        message.exec_()


class ConverterFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.converter_table = None
        self.errors = {'declination': False}

    def setupUi(self, frame):
        super().setupUi(frame)
        self.frame = frame
        self.converter_table = ConverterTable(self.tableWidget, frame)
        self.populate_tilt_curves()
        self._connect_signals_to_slots()
        self.restore_last_session()

    def _connect_signals_to_slots(self):
        self.pushButton_add.clicked.connect(self.converter_table.add_row)
        self.pushButton_remove.clicked.connect(self.converter_table.delete_row)
        self.pushButton_clear.clicked.connect(self.converter_table.clear_table)
        self.pushButton_browse.clicked.connect(self.choose_output_directory)
        self.pushButton_convert.clicked.connect(self.convert_files)
        self.pushButton_output_options.clicked.connect(
            lambda: OptionsDialog(self.frame).exec_())
        self.buttonGroup.buttonToggled.connect(
            self.toggle_output_file_button_group)
        self.comboBox_output_type.currentIndexChanged.connect(
            self.change_output_type_slot)
        self.pushButton_help.clicked.connect(
            lambda: AboutDeclination(self.frame).show())
        self.lineEdit_declination.textEdited.connect(
            self.declination_changed_slot)

    def declination_changed_slot(self):
        declination = self.lineEdit_declination.text()
        if is_float(declination) and -180 <= float(declination) <= 180:
            error_state = False
        else:
            error_state = True
        self.errors['declination'] = error_state
        show_error(self.lineEdit_declination, error_state)

    def change_output_type_slot(self):
        if self.comboBox_output_type.currentText() == 'Current':
            self.comboBox_tilt_tables.setEnabled(True)
        else:
            self.comboBox_tilt_tables.setEnabled(False)

        if self.comboBox_output_type.currentText() == 'Discrete Channels':
            self.lineEdit_declination.setEnabled(False)
        else:
            self.lineEdit_declination.setEnabled(True)

    def populate_tilt_curves(self):
        try:
            directory = sys._MEIPASS
        except AttributeError:
            directory = os.path.dirname(__file__)
        directory = os.path.abspath(
            os.path.join(directory, 'Calibration Tables', '*.cal'))
        self.tilt_tables = glob.glob(directory)
        tilt_tables = []
        for table in self.tilt_tables:
            try:
                tilt_curve = tiltcurve.TiltCurve(table)
                tilt_curve.parse()
                tilt_tables.append([tilt_curve.model,
                                    tilt_curve.ballast,
                                    tilt_curve.salinity,
                                    tilt_curve.path])
            except (FileNotFoundError, UnicodeDecodeError, ValueError):
                QtWidgets.QMessageBox.warning(self.frame,
                                              'Error',
                                              'Error loading ' + table)

        tilt_tables.sort(key=itemgetter(1))
        tilt_tables.sort(key=itemgetter(0))
        for model, ballast, salinity, path in tilt_tables:
            self.comboBox_tilt_tables.addItem(
                '{} - {} ballast - {} water'.format(model, ballast, salinity),
                path)

    def save_session(self):
        appdata.set_userdata('domino.dat',
                             'output_type',
                             self.comboBox_output_type.currentText())
        appdata.set_userdata('domino.dat',
                             'meter_model',
                             self.comboBox_tilt_tables.currentText())
        appdata.set_userdata('domino.dat',
                             'same_directory',
                             self.radioButton_output_same.isChecked())
        appdata.set_userdata('domino.dat',
                             'output_directory',
                             self.lineEdit_output_folder.text())

        appdata.set_userdata('domino.dat', 'declination', self._declination())

    def restore_last_session(self):
        application_data = appdata.get_userdata('domino.dat')
        output_type = application_data.get('output_type', 'Discrete Channels')
        self.set_combobox(self.comboBox_output_type, output_type)

        tilt_curve = application_data.get('meter_model', '')
        self.set_combobox(self.comboBox_tilt_tables, tilt_curve)

        same_directory = application_data.get('same_directory', True)
        if same_directory:
            self.radioButton_output_same.setChecked(True)
        else:
            self.radioButton_output_directory.setChecked(True)
        self.lineEdit_output_folder.setText(
            application_data.get('output_directory', ''))
        self.lineEdit_declination.setText(
            str(application_data.get('declination', 0.0)))
        appdata.set_userdata('domino.dat', 'custom_cal', '')

    def set_combobox(self, combobox, value):
        ind = combobox.findText(value)
        ind = 0 if ind == -1 else ind
        combobox.setCurrentIndex(ind)

    def choose_output_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Select output directory')
        self.lineEdit_output_folder.setText(directory)

    def toggle_output_file_button_group(self):
        state = False if self.radioButton_output_same.isChecked() else True
        self.lineEdit_output_folder.setEnabled(state)
        self.pushButton_browse.setEnabled(state)

    def file_warning(self, file):
        msgbox = QtWidgets.QMessageBox(self.frame)
        msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        msgbox.setText('File error while scanning ' + file)
        msgbox.addButton(QtWidgets.QMessageBox.Ok)
        msgbox.exec()

    def convert_files(self):
        if any(self.errors.values()):
            error_message(self.frame, 'Error',
                          'Please correct highlighted error(s)')
            return
        self.save_session()
        parameters = self._read_conversion_parameters()
        if parameters['output_directory'] == 'error':
            return
        if parameters['calibration'] and not self.confirm_custom_cal():
            return
        self.converter_table.convert_files(parameters)

    def _read_conversion_parameters(self):
        parameters = default_parameters()
        application_data = appdata.get_userdata('domino.dat')

        parameters['output_directory'] = self._get_output_directory()
        parameters['time_format'] = application_data.get('time_format',
                                                         'iso8601')
        parameters['average'] = application_data.get('average_bursts', True)

        split_size = application_data.get('split',
                                          'Do not split output files')
        if split_size != 'Do not split output files':
            parameters['split'] = int(split_size.split(' ')[0])

        output_format = application_data.get('output_format')

        if self.comboBox_output_type.currentText() == 'Current':
            parameters['output_type'] = 'current'
            parameters['tilt_curve'] = tiltcurve.TiltCurve(
                self.comboBox_tilt_tables.currentData())
        else:
            output_type = OUTPUT_TYPE.get(
                self.comboBox_output_type.currentText(), 'discrete')
            parameters['output_type'] = output_type

        parameters['output_format'] = application_data.get('output_format',
                                                           'csv')
        parameters['declination'] = self._declination()
        parameters['calibration'] = self._load_calibration_file(
            application_data.get('custom_cal', None))
        return parameters

    def _load_calibration_file(self, path):
        if not path:
            return None
        try:
            calibration = make_from_calibration_file(path)
        except ValueError:
            calibration = None
        return calibration

    def _declination(self):
        try:
            declination = float(self.lineEdit_declination.text())
        except ValueError:
            declination = 0
        return declination

    def _get_output_directory(self):
        if self.radioButton_output_directory.isChecked():
            directory = self.lineEdit_output_folder.text()
            if not os.path.isdir(directory):
                QtWidgets.QMessageBox.warning(
                                    self.frame,
                                    'Select Folder',
                                    'You must select a valid output path')
                return 'error'
            return directory

    def confirm_custom_cal(self):
        text = 'You currently have a custom calibration file selected. ' \
               'This calibration will be applied to all the files in the ' \
               'conversion queue. Are you sure you want to apply it?'
        answer = QtWidgets.QMessageBox.warning(
                    self.frame,
                    'Confirm Custom Calibration',
                    text,
                    QMessageBox.Yes | QMessageBox.Cancel)
        return answer == QMessageBox.Yes

    def confirm_quit(self):
        return self.converter_table.confirm_quit()
