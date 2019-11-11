# GPLv3 License
# Copyright (c) 2019 Lowell Instruments, LLC, some rights reserved
from gui.converter_ui import Ui_Frame
from gui.options_dialog import OptionsDialog
import os
from mat.data_converter import default_parameters
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QAbstractItemView
from PyQt5.QtCore import QSettings, QThread, Qt
from mat.calibration_factories import make_from_calibration_file
from gui.gui_utils import application_directory
from gui import dialogs
from gui.converter import (
    table_model,
    file_loader,
    file_converter,
    declination_model
)
from gui.converter.session import restore_last_session, save_session
from queue import Queue
from pathlib import Path
from gui.tilt_curve_model import TiltCurveModel
from gui.gui_utils import show_error


OUTPUT_TYPE = {'Current': 'current',
               'Compass Heading': 'compass',
               'Yaw/Pitch/Roll': 'ypr',
               'Cable Attitude': 'cable'}


class ConverterFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.file_queue = Queue()
        self.conversion = None
        self.progress_dialog = None
        self.settings = QSettings()
        self.thread = QThread()
        self.converter = file_converter.ConverterController()

    def setupUi(self, frame):
        super().setupUi(frame)
        self.frame = frame

        # Configure table
        self.tableView.horizontalHeader().setSectionsClickable(False)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Define models
        self.data_file_container = table_model.DataFileContainer()
        self.dec_model = declination_model.Declination()
        self.tilt_model = TiltCurveModel(
            application_directory() / 'Calibration Tables')

        # Connect models
        self.tableView.setModel(self.data_file_container)
        self.tableView.resizeColumnsToContents()
        self.comboBox_tilt_tables.setModel(self.tilt_model)

        self.file_loader = file_loader.FileLoader(self.file_queue)
        self._connect_signals_to_slots()
        restore_last_session(self)

    def _connect_signals_to_slots(self):
        self.pushButton_add.clicked.connect(self.add_files)
        self.file_loader.file_loaded_signal.connect(self.file_loaded)
        self.file_loader.file_error_signal.connect(self.file_error)
        self.pushButton_remove.clicked.connect(self.delete_row)
        self.pushButton_clear.clicked.connect(self.data_file_container.clear)
        self.pushButton_convert.clicked.connect(self.convert_files)
        self.pushButton_browse.clicked.connect(self.choose_output_directory)
        self.pushButton_output_options.clicked.connect(
            lambda: OptionsDialog(self.frame).exec_())
        self.buttonGroup.buttonToggled.connect(
            self.toggle_output_file_button_group)
        self.comboBox_output_type.currentIndexChanged.connect(
            self.change_output_type_slot)
        self.pushButton_help.clicked.connect(dialogs.about_declination)
        self.lineEdit_declination.textChanged.connect(self.declination_changed)
        self.dec_model.update_signal.connect(self.update_declination)
        self.data_file_container.rowsInserted.connect(self.enable_buttons)
        self.data_file_container.rowsRemoved.connect(self.enable_buttons)
        self.data_file_container.modelReset.connect(self.enable_buttons)

    def enable_buttons(self):
        state = True if len(self.data_file_container) > 0 else False
        buttons = [
            self.pushButton_remove,
            self.pushButton_clear,
            self.pushButton_convert]
        for button in buttons:
            button.setEnabled(state)

    """
    Methods for loading files
    """
    # slot
    def add_files(self):
        directory = self.settings.value('last_directory', '', type=str)
        file_paths = dialogs.open_lid_file(directory)
        if not file_paths[0]:
            return
        directory = Path(file_paths[0][0]).parent
        self.settings.setValue('last_directory', str(directory))
        self.file_queue.put(file_paths[0])
        self.file_loader.run()

    # slot
    def delete_row(self):
        row_objects = self.tableView.selectionModel().selectedRows()
        for row in row_objects:
            self.data_file_container.delete(row.row())

    # slot
    def file_loaded(self, file):
        if file.header_error:
            dialogs.header_error(file.filename, file.header_error)
        self.data_file_container.add_file(file)

    # slot
    def file_error(self, message):
        dialogs.error_message('Load Error', message)

    def _start_thread(self):
        self.file_loader.moveToThread(self.thread)
        self.file_loader.finished_signal.connect(self.thread.quit)
        self.thread.start()

    """
    Convert files
    """
    def convert_files(self):
        self.remove_error_files()
        parameters = self._read_output_options()
        terminate_conditions = [
            lambda: self.check_error_states(),
            lambda: parameters['output_directory'] == 'error',
            lambda: len(self.data_file_container) == 0,
            lambda: (parameters['calibration'] is not None
                     and not dialogs.confirm_custom_cal()),
            lambda: (self.data_file_container.unconverted() == 0
                     and not self.reset_converted())
        ]

        if self.check_terminate_conditions(terminate_conditions):
            return

        save_session(self)
        self.converter.model = self.data_file_container
        self.converter.parameters = parameters
        self.converter.convert()

    def check_terminate_conditions(self, conditions):
        for condition in conditions:
            if condition():
                return True
        return False

    def reset_converted(self):
        if self.data_file_container.convertable() > 0:
            if dialogs.prompt_mark_unconverted():
                self.data_file_container.reset_converted()
                return True
        return False

    def remove_error_files(self):
        if self.data_file_container.errors():
            answer = dialogs.ask_remove_error_files()
            if answer == 'Remove':
                self.data_file_container.remove_error_files()
            elif answer == 'Retry':
                self.data_file_container.reset_errors()

    def check_error_states(self):
        if self.dec_model.error_state:
            dialogs.error_message('Error', 'Please correct declination')
            return True
        return False

    # slot
    def change_output_type_slot(self):
        state = self.comboBox_output_type.currentText() == 'Current'
        self.comboBox_tilt_tables.setEnabled(state)
        disabled = ['Discrete Channels', 'Cable Attitude']
        state = self.comboBox_output_type.currentText() in disabled
        self.dec_model.set_enabled(not state)

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

    def _read_output_options(self):
        parameters = default_parameters()
        app_data = self.settings.value('output_options', {}, type=dict)
        parameters['output_directory'] = self._get_output_directory()
        parameters['time_format'] = app_data.get('time_format', 'iso8601')
        parameters['average'] = app_data.get('average_bursts', True)
        custom_cal_path = app_data.get('custom_cal', None)
        if custom_cal_path:
            try:
                custom_cal = make_from_calibration_file(custom_cal_path)
                parameters['calibration'] = custom_cal
            except:
                pass
        split_size = app_data.get('split', 'Do not split output files')
        if split_size != 'Do not split output files':
            parameters['split'] = int(split_size.split(' ')[0])

        if self.comboBox_output_type.currentText() == 'Current':
            parameters['output_type'] = 'current'
            parameters['tilt_curve'] = \
                self.comboBox_tilt_tables.currentData()
        else:
            output_type = OUTPUT_TYPE.get(
                self.comboBox_output_type.currentText(),
                'discrete')
            parameters['output_type'] = output_type

        parameters['output_format'] = app_data.get('output_format', 'csv')
        parameters['declination'] = self.dec_model.declination_value()
        return parameters

    """
    Methods for declination
    """
    # slot
    def declination_changed(self):
        self.dec_model.declination = self.lineEdit_declination.text()

    # slot
    def update_declination(self):
        self.lineEdit_declination.setText(str(self.dec_model.declination))
        show_error(self.lineEdit_declination, self.dec_model.error_state)
        self.lineEdit_declination.setEnabled(self.dec_model.enabled)

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
