# GPLv3 License
# Copyright (c) 2019 Lowell Instruments, LLC, some rights reserved
from gui.converter_ui import Ui_Frame
from gui.options_dialog import OptionsDialog
from mat import appdata, tiltcurve
import os
import sys
import glob
from operator import itemgetter
from mat.data_converter import default_parameters
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from mat.calibration_factories import make_from_calibration_file
from gui.gui_utils import error_message

from gui.converter.file_converter import FileConverter
from gui.progress_dialog import ProgressDialog
from gui import dialogs
from gui.converter import (
    table_model,
    table_view,
    table_controller,
    file_loader,
    file_converter,
    declination_model,
    declination_view,
    declination_controller
)

OUTPUT_TYPE = {'Current': 'current',
               'Compass Heading': 'compass',
               'Yaw/Pitch/Roll': 'ypr'}


class ConverterFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.table_controller = None

        self.conversion = None
        self.progress_dialog = None


    def setupUi(self, frame):
        super().setupUi(frame)
        self.frame = frame

        # Models
        self.data_file_container = table_model.DataFileContainer()
        self.dec_model = declination_model.Declination()

        # Views
        self.table_view = table_view.ConverterTable(self.tableWidget)
        self.dec_view = declination_view.DeclinationView(
            self.lineEdit_declination)

        # Controllers
        self.table_controller = table_controller.TableController(
            self.data_file_container, self.table_view)
        self.dec_controller = declination_controller.DeclinationController(
            self.dec_model, self.dec_view)
        self.file_loader = file_loader.LoaderController(
            self.data_file_container)

        self.populate_tilt_curves()
        self._connect_signals_to_slots()
        self.restore_last_session()

    def _connect_signals_to_slots(self):
        self.pushButton_add.clicked.connect(self.file_loader.add_row)
        self.pushButton_remove.clicked.connect(
            self.table_controller.delete_selected_rows)
        self.pushButton_clear.clicked.connect(self.table_controller.clear)
        self.pushButton_convert.clicked.connect(self.convert_files)

        self.pushButton_browse.clicked.connect(self.choose_output_directory)

        self.pushButton_output_options.clicked.connect(
            lambda: OptionsDialog(self.frame).exec_())
        self.buttonGroup.buttonToggled.connect(
            self.toggle_output_file_button_group)
        self.comboBox_output_type.currentIndexChanged.connect(
            self.change_output_type_slot)
        self.pushButton_help.clicked.connect(
            lambda: dialogs.about_declination())

        self.file_loader.load_error_signal.connect(
            self.load_error_slot)

    def load_error_slot(self, error_str):
        QMessageBox.warning(self.frame, 'File Load Error', error_str)

    def _check_for_errors_after_conversion(self):
        errors = ['failed', 'not found']
        if any([file.status in errors for file in self.data_file_container]):
            dialogs.file_conversion_error()

    def convert_files(self):
        parameters = self._read_conversion_parameters()
        terminate_conditions = [
            lambda: self.check_error_states(),
            lambda: parameters['output_directory'] == 'error',
            lambda: (parameters['calibration'] is not None
                     and not dialogs.confirm_custom_cal()),
            lambda: len(self.data_file_container) == 0,
            lambda: not self.check_for_unconverted()
        ]

        if self.check_terminate_conditions(terminate_conditions):
            return

        self.save_session()
        self.converter = file_converter.ConverterController(
            self.data_file_container, parameters)
        self.converter.convert()

    def check_terminate_conditions(self, conditions):
        for condition in conditions:
            if condition():
                return True
        return False

    def check_for_unconverted(self):
        status = True
        if not self.data_file_container.unconverted():
            status = False
            if dialogs.prompt_mark_unconverted():
                self.data_file_container.reset_converted()
                status = True
        return status

    def check_error_states(self):
        if self.dec_model.error_state:
            error_message(self.frame, 'Error',
                          'Please correct declination')
            return True
        return False

    def change_output_type_slot(self):
        state = self.comboBox_output_type.currentText() == 'Current'
        self.comboBox_tilt_tables.setEnabled(state)

        state = self.comboBox_output_type.currentText() != 'Discrete Channels'
        self.dec_model.set_enabled(state)

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
                QMessageBox.warning(self.frame,
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
        app_data = appdata.get_userdata('domino.dat')
        output_type = app_data.get('output_type', 'Discrete Channels')
        self.set_combobox(self.comboBox_output_type, output_type)

        tilt_curve = app_data.get('meter_model', '')
        self.set_combobox(self.comboBox_tilt_tables, tilt_curve)

        same_directory = app_data.get('same_directory', True)
        if same_directory:
            self.radioButton_output_same.setChecked(True)
        else:
            self.radioButton_output_directory.setChecked(True)
        self.lineEdit_output_folder.setText(
            app_data.get('output_directory', ''))
        self.dec_model.declination = str(app_data.get('declination', 0.0))
        appdata.set_userdata('domino.dat', 'custom_cal', '')

    def set_combobox(self, combobox, value):
        ind = combobox.findText(value)
        ind = 0 if ind == -1 else ind
        combobox.setCurrentIndex(ind)

    def choose_output_directory(self):
        directory = QFileDialog.getExistingDirectory(
            caption='Select output directory')
        self.lineEdit_output_folder.setText(directory)

    def toggle_output_file_button_group(self):
        state = False if self.radioButton_output_same.isChecked() else True
        self.lineEdit_output_folder.setEnabled(state)
        self.pushButton_browse.setEnabled(state)

    def _read_conversion_parameters(self):
        parameters = default_parameters()
        app_data = appdata.get_userdata('domino.dat')
        parameters['output_directory'] = self._get_output_directory()
        parameters['time_format'] = app_data.get('time_format', 'iso8601')
        parameters['average'] = app_data.get('average_bursts', True)
        split_size = app_data.get('split', 'Do not split output files')
        if split_size != 'Do not split output files':
            parameters['split'] = int(split_size.split(' ')[0])

        if self.comboBox_output_type.currentText() == 'Current':
            parameters['output_type'] = 'current'
            parameters['tilt_curve'] = tiltcurve.TiltCurve(
                self.comboBox_tilt_tables.currentData())
        else:
            output_type = OUTPUT_TYPE.get(
                self.comboBox_output_type.currentText(),
                'discrete')
            parameters['output_type'] = output_type

        parameters['output_format'] = app_data.get('output_format', 'csv')
        if not self.dec_model.error_state:
            declination = self.dec_model.declination
        else:
            declination = 0
        parameters['declination'] = declination
        parameters['calibration'] = self._load_calibration_file(
            app_data.get('custom_cal', None))
        return parameters

    def _load_calibration_file(self, path):
        if not path:
            return None
        try:
            calibration = make_from_calibration_file(path)
        except ValueError:
            calibration = None
        return calibration

    def _get_output_directory(self):
        if self.radioButton_output_directory.isChecked():
            directory = self.lineEdit_output_folder.text()
            if not os.path.isdir(directory):
                QMessageBox.warning(
                                    self.frame,
                                    'Select Folder',
                                    'You must select a valid output path')
                return 'error'
            return directory

    def confirm_quit(self):
        if len(self.data_file_container) == 0:
            return True
        status = [file.status for file in self.data_file_container]
        if any([True for s in status if s == 'unconverted']):
            return dialogs.confirm_quit()
        else:
            return True
