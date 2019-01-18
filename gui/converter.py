# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved
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


OUTPUT_TYPE = {'Current': 'current',
               'Compass Heading': 'compass',
               'Yaw/Pitch/Roll': 'ypr'}


class ConverterFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.converter_table = None

    def setupUi(self, frame):
        super().setupUi(frame)
        self.frame = frame
        self.converter_table = ConverterTable(self.tableWidget)
        self.populate_tilt_curves()
        self.restore_last_session()
        self._connect_signals_to_slots()

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
            self.change_ouput_type)

    def change_ouput_type(self):
        if self.comboBox_output_type.currentText() == 'Current':
            self.comboBox_tilt_tables.setEnabled(True)
        else:
            self.comboBox_tilt_tables.setEnabled(False)

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

    def restore_last_session(self):
        application_data = appdata.get_userdata('domino.dat')
        self.comboBox_output_type.setCurrentText(application_data.get(
            'output_type', 'Discrete Channels'))
        tilt_curve_ind = self.comboBox_tilt_tables.findText(
            application_data.get('meter_model', ''))
        tilt_curve_ind = 0 if tilt_curve_ind == -1 else tilt_curve_ind
        self.comboBox_tilt_tables.setCurrentIndex(tilt_curve_ind)
        same_directory = application_data.get('same_directory', True)
        if same_directory:
            self.radioButton_output_same.setChecked(True)
        else:
            self.radioButton_output_directory.setChecked(True)
        self.lineEdit_output_folder.setText(
            application_data.get('output_directory', ''))

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
        self.save_session()
        parameters = self._read_conversion_parameters()
        if parameters['output_directory'] == 'error':
            return
        self.converter_table.convert_files(parameters)

    def _read_conversion_parameters(self):
        parameters = default_parameters()
        application_data = appdata.get_userdata('domino.dat')

        parameters['output_directory'] = self._get_output_directory()
        parameters['time_format'] = application_data.get('time_format',
                                                         'iso8601')
        parameters['average'] = application_data.get('average_bursts', True)
        if application_data.get('is_declination', False):
            parameters['declination'] = float(
                application_data.get('declination', 0))

        split_size = application_data.get('split')
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
        return parameters

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

    def confirm_quit(self):
        return self.converter_table.confirm_quit()
