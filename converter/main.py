# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QThread
from converter.main_ui import Ui_MainWindow
import converter.progress
import converter.options
from mat import appdata, tiltcurve
import os
import sys
from datetime import datetime
import time
import glob
from operator import itemgetter
from copy import deepcopy
from mat.data_converter import DataConverter, ConversionParameters
from mat.data_file_factory import load_data_file

COMBOBOX_CURRENT = 'Current'
COMBOBOX_COMPASS = 'Compass Heading'
COMBOBOX_HDF5 = 'Hierarchical Data Format 5 (.hdf5)'


class MyGui(Ui_MainWindow):
    def __init__(self, window):
        self.version = 'Converter 0.9.3'
        self.window = window
        self.setupUi(window)
        self.actionAdd.triggered.connect(self.open_file)
        self.actionConvert.triggered.connect(self.convert_files)
        self.actionDelete.triggered.connect(self.delete_row)
        self.actionClearList.triggered.connect(self.delete_table)
        self.actionVisit_Lowell_Instruments_Website.triggered.connect(
            self.visit_website)
        self.actionAdd_File_s.triggered.connect(self.open_file)
        self.actionConvert_Files.triggered.connect(self.convert_files)
        self.pushButton_browse.clicked.connect(self.choose_output_directory)
        self.pushButton_output_options.clicked.connect(self.show_options)
        self.buttonGroup.buttonToggled.connect(
            self.toggle_output_file_button_group)
        self.comboBox_output_type.currentIndexChanged.connect(
            self.change_ouput_type)
        self.actionOpen_Output_Foler.triggered.connect(self.open_output_foler)
        self.actionAbout.triggered.connect(self.about_slot)
        # self.checkBox_output_same_source.stateChanged.connect(self.checkbox_same_source)
        # self.checkBox_output_same_source.setChecked(True)
        self.tableWidget.clicked.connect(self.table_click)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 140)
        self.tableWidget.setColumnWidth(4, 140)
        self.file_list = []
        self.file_queue = []
        self.active_conversion_ind = 0
        self.populate_tilt_curves()
        self.selected_row = None
        self.restore_last_session()
        # self.window.closeEvent = self.closeEvent
        self.file_loader = None
        self.actionAbout.setText(self.version)

    def about_slot(self):
        QtWidgets.QMessageBox.about(self.window,
                                    'About Converter',
                                    'Lowell Instruments 2018\n' + self.version)

    def open_output_foler(self):
        if os.path.isdir(self.lineEditOutputFolder.text()):
            os.system('explorer.exe "{}"'.format(
                self.lineEditOutputFolder.text().replace('/', '\\')))
        else:
            QtWidgets.QMessageBox.warning(self.window,
                                          'Select Folder',
                                          'You must select an output path')

    def change_ouput_type(self):
        if self.comboBox_output_type.currentText() == COMBOBOX_CURRENT:
            self.comboBox_tilt_tables.setEnabled(True)
        else:
            self.comboBox_tilt_tables.setEnabled(False)

    def closeEvent(self, event):
        if not self.file_list:
            event.accept()
            return

        status = [table_item.conversion_status
                  for table_item in self.file_list]
        if any([True for s in status if s == 'unconverted']):
            reply = QtWidgets.QMessageBox.question(
                self.window,
                'Confirm Quit',
                'There are unconverted file in the queue. '
                'Are you sure you want to quit?')
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def visit_website(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(
            'http://lowellinstruments.com'))

    def show_options(self):
        OptionsDialog(self.window).exec_()

    def delete_row(self):
        row_objects = self.tableWidget.selectionModel().selectedRows()
        rows = []
        for row in row_objects:
            rows.append(row.row())

        rows.sort(reverse=True)
        for row in rows:
            self.tableWidget.removeRow(row)

        self.file_list = [row for i, row in enumerate(self.file_list)
                          if i not in rows]
        self.refresh_table()

    def delete_table(self):
        if len(self.file_list) > 0:
            reply = QtWidgets.QMessageBox.question(
                self.window,
                'Confirm',
                'Are you sure you want to clear the file list?')
            if reply == QtWidgets.QMessageBox.Yes:
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.removeRow(0)
                self.file_list = []

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
                QtWidgets.QMessageBox.warning(self.window,
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
                             self.radioButtonOutputSame.isChecked())
        appdata.set_userdata('converter-1.dat',
                             'output_directory',
                             self.lineEditOutputFolder.text())

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
            self.radioButtonOutputSame.setChecked(True)
        else:
            self.radioButtonOutputDirectory.setChecked(True)
        self.lineEditOutputFolder.setText(
            application_data.get('output_directory', ''))

    def choose_output_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            caption='Select output directory')
        self.lineEditOutputFolder.setText(directory)

    def toggle_output_file_button_group(self):
        state = False if self.radioButtonOutputSame.isChecked() else True
        self.lineEditOutputFolder.setEnabled(state)
        self.pushButton_browse.setEnabled(state)
        self.actionOpen_Output_Foler.setEnabled(state)

    def table_click(self, cell):
        self.selected_row = cell.row()
        self.tableWidget.selectRow(self.selected_row)

    def open_file(self):
        application_data = appdata.get_userdata('converter-1.dat')
        last_directory = (application_data['last_directory']
                          if 'last_directory' in application_data else '')
        file_paths = QtWidgets.QFileDialog.getOpenFileNames(
            self.window,
            'Open Lowell Instruments Data File',
            last_directory,
            'Data Files (*.lid *.lis)')

        if not file_paths[0]:
            return

        directory = os.path.dirname(file_paths[0][0])
        appdata.set_userdata('converter-1.dat', 'last_directory', directory)
        existing_file_paths = [this_file.path for this_file in self.file_list]
        self.file_loader = FileLoader(file_paths[0], existing_file_paths)
        self.file_loader.load_complete_signal.connect(
            self.extend_file_list_slot)
        self.file_loader.load_error_signal.connect(self.file_warning)
        self.file_loader.start()

    def extend_file_list_slot(self, new_files):
        self.file_list.extend(new_files)
        self.refresh_table()

    def conversion_complete_slot(self, file_list):
        self.file_list = file_list
        self.refresh_table()

    def refresh_table(self):
        self.tableWidget.setRowCount(len(self.file_list))
        for i, table_item in enumerate(self.file_list):
            if table_item.conversion_status == 'unconverted':
                self.tableWidget.setItem(
                    i, 0, self.make_table_widget(table_item.filename))
            elif table_item.conversion_status == 'converted':
                self.tableWidget.setItem(
                    i, 0, self.make_table_widget('\u2714 ' +
                                                 table_item.filename))
            elif table_item.conversion_status == 'failed':
                self.tableWidget.setItem(
                    i, 0, self.make_table_widget('\u2718 ' +
                                                 table_item.filename))
            self.tableWidget.setItem(
                i, 1, self.make_table_widget(table_item.folder))
            self.tableWidget.setItem(
                i, 2, self.make_table_widget(
                    '{:.3f}MB'.format(table_item.size)))
            self.tableWidget.setItem(
                i, 3, self.make_table_widget(table_item.start_time))
            self.tableWidget.setItem(
                i, 4, self.make_table_widget(table_item.end_time))

    def make_table_widget(self, string):
        item = QtWidgets.QTableWidgetItem(string)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        return item

    def file_warning(self, file):
        msgbox = QtWidgets.QMessageBox(self.window)
        msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        msgbox.setText('File error while scanning ' + file)
        msgbox.addButton(QtWidgets.QMessageBox.Ok)
        msgbox.exec()

    def convert_files(self):
        self.save_session()
        if not self.file_list:
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
        if self.radioButtonOutputDirectory.isChecked():
            parameters['output_directory'] = self.lineEditOutputFolder.text()
            if not os.path.isdir(self.lineEditOutputFolder.text()):
                QtWidgets.QMessageBox.warning(self.window,
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

        self.conversion = FileConverter(self.file_list, parameters)
        self.progress_dialog = ProgressDialog(self.window)
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


class FileLoader(QThread):
    load_complete_signal = QtCore.pyqtSignal(list)
    load_error_signal = QtCore.pyqtSignal(str)

    def __init__(self, new_paths, existing_paths):
        """
        new_paths are the paths to the files to be added to the list
        existing_paths contains a list of the existing TableItem object paths
        """
        super().__init__()
        self.new_paths = new_paths
        self.existing_paths = existing_paths
        self.new_files = []

    def run(self):
        for this_path in self.new_paths:
            if this_path not in self.existing_paths:
                try:
                    table_item = TableItem(this_path)
                    self.load_complete_signal.emit([table_item])
                except (FileNotFoundError, TypeError, ValueError):
                    self.load_error_signal.emit(this_path)


class FileConverter(QThread):
    progress_signal = QtCore.pyqtSignal(int, int)
    conversion_status_signal = QtCore.pyqtSignal(str, int, int)
    conversion_complete = QtCore.pyqtSignal(list)

    def __init__(self, table_items, parameters):
        # parameters is a dict of parameters required by FileConverter
        super().__init__()
        self.table_items = deepcopy(table_items)
        self.parameters = parameters
        self.current_file_ind = 0
        self.total_mb = sum([this_item.size for this_item in self.table_items])
        self._is_running = True
        self.converter = None

    def run(self):
        for i, this_table_item in enumerate(self.table_items):
            if not self._is_running:
                break
            self.current_file_ind = i
            self.conversion_status_signal.emit(this_table_item.filename,
                                               i+1,
                                               len(self.table_items))
            if not os.path.isfile(this_table_item.path):
                self.table_items[i].conversion_status = 'file_not_found'
                continue
            try:
                conversion_parameters = ConversionParameters(
                                            this_table_item.path,
                                            **self.parameters)
                self.converter = DataConverter(conversion_parameters)
                self.converter.register_observer(self.update_progress)
                self.converter.convert()
                self.table_items[i].conversion_status = 'converted'
            except (FileNotFoundError, TypeError, ValueError):
                self.table_items[i].conversion_status = 'failed'
        self.conversion_complete.emit(self.table_items)

    def update_progress(self, percent_done):
        # This is an observer function that gets notified when a data
        # page is parsed
        if not self._is_running:
            self.converter.cancel_conversion()
        cumulative_mb = sum([table_item.size for table_item
                             in self.table_items[:self.current_file_ind]])
        cumulative_mb += (self.table_items[self.current_file_ind].size *
                          (percent_done/100))
        overall_percent = cumulative_mb / self.total_mb
        overall_percent *= 100
        self.progress_signal.emit(percent_done, overall_percent)

    def cancel(self):
        self._is_running = False


class TableItem:
    def __init__(self, path):
        data_file = load_data_file(path)
        self.path = path
        self.folder, self.filename = os.path.split(os.path.abspath(path))
        self.size = data_file.file_size() / 1024 ** 2
        start_time = data_file.page_times()[0]
        self.start_time = datetime.utcfromtimestamp(start_time).isoformat()
        self.end_time = datetime.utcfromtimestamp(0).isoformat()
        self.conversion_status = 'unconverted'


class ProgressDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = converter.progress.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('File Conversion Progress')

    def update_progress(self, percent, overall_percent):
        self.ui.progressBar_file.setValue(percent)
        self.ui.progressBar_total.setValue(overall_percent)
        if percent == 100:
            time.sleep(0.5)

    def update_status(self, filename, i, total_files):
        self.ui.progressBar_file.setValue(0)
        self.ui.label_status.setText(
            'Converting {} - File {} of {}'.format(filename, i, total_files))

    def conversion_complete(self):
        self.close()

    def click_cancel(self):
        self.ui.label_status.setText('Canceling conversion...')
        self.ui.pushButton.setEnabled(False)


class OptionsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = converter.options.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('File Output Options')
        self.ui.pushButton_save.clicked.connect(self.save)
        self.ui.pushButton_cancel.clicked.connect(self.cancel)
        self.button_mapping = {'radioButton_iso8601_time': 'iso8601',
                               'radioButton_legacy_time': 'legacy',
                               'radioButton_elapsed_time': 'elapsed',
                               'radioButton_posix_time': 'posix',
                               'iso8601': 'radioButton_iso8601_time',
                               'legacy': 'radioButton_legacy_time',
                               'elapsed': 'radioButton_elapsed_time',
                               'posix': 'radioButton_posix_time'}
        self.load_saved()

    def load_saved(self):
        application_data = appdata.get_userdata('converter-1.dat')
        time_format = application_data.get('time_format', 'iso8601')
        time_format_button_name = self.button_mapping[time_format]
        getattr(self.ui, time_format_button_name).setChecked(True)
        self.ui.checkBox_average_bursts.setChecked(application_data.get(
            'average_bursts', True))
        self.ui.checkBox_declination.setChecked(application_data.get(
            'is_declination', True))
        self.ui.lineEdit_declination.setText(application_data.get(
            'declination', '0'))

    def save(self):
        button_name = self.ui.buttonGroup.checkedButton().objectName()
        appdata.set_userdata('converter-1.dat',
                             'time_format',
                             self.button_mapping[button_name])
        appdata.set_userdata('converter-1.dat',
                             'average_bursts',
                             self.ui.checkBox_average_bursts.isChecked())
        appdata.set_userdata('converter-1.dat',
                             'is_declination',
                             self.ui.checkBox_declination.isChecked())
        appdata.set_userdata('converter-1.dat',
                             'declination',
                             self.ui.lineEdit_declination.text())
        self.hide()

    def cancel(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()  # create a main window
    ui = MyGui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
