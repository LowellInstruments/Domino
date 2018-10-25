# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved
from gui.converter_ui import Ui_Frame
from gui.progress_dialog import ProgressDialog
from gui.options_dialog import OptionsDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from mat import appdata, tiltcurve
import os
import sys
import glob
from operator import itemgetter
from gui.file_management import FileConverter, FileLoader
from PyQt5.QtCore import Qt
from gui.data_file import DataFileContainer

COMBOBOX_CURRENT = 'Current'
COMBOBOX_COMPASS = 'Compass Heading'
COMBOBOX_HDF5 = 'Hierarchical Data Format 5 (.hdf5)'
FILE_NAME = 0
FOLDER = 1
SIZE = 2
START_TIME = 3


class ConverterFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.file_queue = []
        self.active_conversion_ind = 0
        self.selected_row = None
        self.data_file_container = DataFileContainer()
        self.file_loader = FileLoader(self.data_file_container)

    def setupUi(self, frame):
        super().setupUi(frame)
        self.frame = frame
        self.pushButton_add.clicked.connect(self.add_row)
        self.pushButton_remove.clicked.connect(self.delete_row)
        self.pushButton_browse.clicked.connect(self.choose_output_directory)
        self.pushButton_convert.clicked.connect(self.convert_files)
        self.pushButton_output_options.clicked.connect(self.show_options)
        self.buttonGroup.buttonToggled.connect(
            self.toggle_output_file_button_group)
        self.comboBox_output_type.currentIndexChanged.connect(
            self.change_ouput_type)
        self.tableWidget.clicked.connect(self.table_click)
        self.file_loader.load_complete_signal.connect(
            self.extend_file_list_slot)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 140)
        self.tableWidget.setColumnWidth(4, 140)
        self.populate_tilt_curves()
        self.restore_last_session()

    def add_row(self):
        file_paths = self._open_file()
        if not file_paths[0]:
            return
        self._update_recent_directory_appdata(file_paths[0][0])
        self.file_loader.load_files(file_paths[0])

    def _open_file(self):
        application_data = appdata.get_userdata('converter-1.dat')
        last_directory = (application_data['last_directory']
                          if 'last_directory' in application_data else '')
        file_paths = QtWidgets.QFileDialog.getOpenFileNames(
            self.frame,
            'Open Lowell Instruments Data File',
            last_directory,
            'Data Files (*.lid *.lis)')
        return file_paths

    def _update_recent_directory_appdata(self, file_path):
        directory = os.path.dirname(file_path)
        appdata.set_userdata('converter-1.dat', 'last_directory', directory)

    def delete_row(self):
        row_objects = self.tableWidget.selectionModel().selectedRows()
        rows = []
        for row in row_objects:
            file = self.tableWidget.item(row.row(), 0).data(Qt.UserRole)
            self.data_file_container.delete(file)
        self.refresh_table()

    def delete_table(self):
        if len(self.data_file_container) > 0:
            reply = QtWidgets.QMessageBox.question(
                self.frame,
                'Confirm',
                'Are you sure you want to clear the file list?')
            if reply == QtWidgets.QMessageBox.Yes:
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.removeRow(0)
                self.data_file_container.clear()

    def refresh_table(self):
        self.tableWidget.setRowCount(len(self.data_file_container))
        for i, data_file in enumerate(self.data_file_container):
            file_name = self._add_symbol(data_file.filename, data_file.status)
            file_name_item = self._table_item(file_name)
            file_name_item.setData(Qt.UserRole, id(data_file))
            self.tableWidget.setItem(i, FILE_NAME, file_name_item)

            self.tableWidget.setItem(i, FOLDER,
                                     self._table_item(data_file.folder))
            self.tableWidget.setItem(i, SIZE,
                                     self._table_item(data_file.size_str))
            self.tableWidget.setItem(i, START_TIME,
                                     self._table_item(data_file.start_time))

    def _table_item(self, string):
        item = QtWidgets.QTableWidgetItem(string)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        return item

    def _add_symbol(self, filename, status):
        symbol_map = {'converted': '\u2714',
                      'failed': '\u2718',
                      'file_error': '\u2718'}
        symbol = symbol_map.get(status)
        if not symbol:
            return filename
        return '{} {}'.format(symbol, filename)

    def change_ouput_type(self):
        if self.comboBox_output_type.currentText() == COMBOBOX_CURRENT:
            self.comboBox_tilt_tables.setEnabled(True)
        else:
            self.comboBox_tilt_tables.setEnabled(False)

    def show_options(self):
        OptionsDialog(self.frame).exec_()

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
        appdata.set_userdata('converter-1.dat',
                             'output_type',
                             self.comboBox_output_type.currentText())
        appdata.set_userdata('converter-1.dat',
                             'output_format',
                             self.comboBox_output_format.currentText())
        appdata.set_userdata('converter-1.dat',
                             'meter_model',
                             self.comboBox_tilt_tables.currentText())
        appdata.set_userdata('converter-1.dat',
                             'same_directory',
                             self.radioButton_output_same.isChecked())
        appdata.set_userdata('converter-1.dat',
                             'output_directory',
                             self.lineEdit_output_folder.text())

    def restore_last_session(self):
        application_data = appdata.get_userdata('converter-1.dat')
        self.comboBox_output_type.setCurrentText(application_data.get(
            'output_type', 'Discrete Channels'))
        self.comboBox_output_format.setCurrentText(application_data.get(
            'output_format', 'Comma Separated Value (.csv) - (slow)'))
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

    def table_click(self, cell):
        self.selected_row = cell.row()
        self.tableWidget.selectRow(self.selected_row)

    def extend_file_list_slot(self, container):
        self.data_file_container = container
        self.refresh_table()

    def conversion_complete_slot(self):
        self.refresh_table()

    def file_warning(self, file):
        msgbox = QtWidgets.QMessageBox(self.frame)
        msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        msgbox.setText('File error while scanning ' + file)
        msgbox.addButton(QtWidgets.QMessageBox.Ok)
        msgbox.exec()

    def convert_files(self):
        self.save_session()
        if len(self.data_file_container) == 0:
            return

        application_data = appdata.get_userdata('converter-1.dat')
        parameters = {'output_directory': None,
                      'output_format': 'csv',
                      'output_type': 'discrete',
                      'average': True,
                      'tilt_curve': None,
                      'time_format': 'iso8601',
                      'declination': 0}
        # 'custom_calibration': None -- temporarily removed from above dict
        if self.radioButton_output_directory.isChecked():
            parameters['output_directory'] = self.lineEdit_output_folder.text()
            if not os.path.isdir(self.lineEdit_output_folder.text()):
                QtWidgets.QMessageBox.warning(self.frame,
                                              'Select Folder',
                                              'You must select an output path')
                return

        parameters['time_format'] = application_data.get('time_format',
                                                         'iso8601')
        parameters['average'] = application_data.get('average_bursts', True)
        if application_data.get('is_declination', False):
            parameters['declination'] = float(
                application_data.get('declination', 0))

        if self.comboBox_output_type.currentText() == COMBOBOX_CURRENT:
            parameters['output_type'] = 'current'
            parameters['tilt_curve'] = tiltcurve.TiltCurve(
                self.comboBox_tilt_tables.currentData())

        elif self.comboBox_output_type.currentText() == COMBOBOX_COMPASS:
            parameters['output_type'] = 'compass'

        if self.comboBox_output_format.currentText() == COMBOBOX_HDF5:
            parameters['output_format'] = 'hdf5'

        # pass the files and parameters off to the FileConverter
        # thread for processing

        self.conversion = FileConverter(self.data_file_container, parameters)
        self.progress_dialog = ProgressDialog(self.frame)
        self.progress_dialog.ui.pushButton.clicked.connect(
            self.conversion.cancel)
        self.progress_dialog.ui.pushButton.clicked.connect(
            self.progress_dialog.click_cancel)

        self.conversion.progress_signal.connect(
            self.progress_dialog.update_progress)
        self.conversion.conversion_status_signal.connect(
            self.progress_dialog.update_status)
        self.conversion.conversion_complete.connect(
            self.progress_dialog.conversion_complete)
        self.conversion.conversion_complete.connect(
            self.conversion_complete_slot)

        self.progress_dialog.show()
        self.conversion.start()

    def closeEvent(self, event):
        if len(self.data_file_container) == 0:
            event.accept()
            return

        status = [table_item.conversion_status
                  for table_item in self.data_file_container]
        if any([True for s in status if s == 'unconverted']):
            reply = QtWidgets.QMessageBox.question(
                self.frame,
                'Confirm Quit',
                'There are unconverted file in the queue. '
                'Are you sure you want to quit?')
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
