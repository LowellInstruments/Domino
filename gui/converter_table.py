from mat import appdata
from gui.file_management import FileConverter, FileLoader
from PyQt5.QtCore import Qt
from gui.data_file import DataFileContainer
from PyQt5 import QtWidgets, QtCore
from gui.progress_dialog import ProgressDialog
import os


FILE_NAME = 0
FOLDER = 1
SIZE = 2
START_TIME = 3


class ConverterTable:
    def __init__(self, tableWidget, parent):
        self.tableWidget = tableWidget
        self.parent = parent
        self.data_file_container = DataFileContainer()
        self.file_loader = FileLoader(self.data_file_container)
        self.tableWidget.setSelectionMode(1)
        self.tableWidget.setSelectionBehavior(1)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 140)
        self.tableWidget.setColumnWidth(4, 140)
        self.file_loader.load_complete_signal.connect(
            lambda: self.refresh_table())
        self.file_loader.load_error_signal.connect(
            self.load_error_slot)

    def add_row(self):
        file_paths = self._open_file()
        if not file_paths[0]:
            return
        self._update_recent_directory_appdata(file_paths[0][0])
        self.file_loader.load_files(file_paths[0])

    def _open_file(self):
        application_data = appdata.get_userdata('domino.dat')
        last_directory = (application_data['last_directory']
                          if 'last_directory' in application_data else '')
        file_paths = QtWidgets.QFileDialog.getOpenFileNames(
            self.tableWidget.window(),
            'Open Lowell Instruments Data File',
            last_directory,
            'Data Files (*.lid *.lis)')
        return file_paths

    def _update_recent_directory_appdata(self, file_path):
        directory = os.path.dirname(file_path)
        appdata.set_userdata('domino.dat', 'last_directory', directory)

    def load_error_slot(self, error_str):
        QtWidgets.QMessageBox.warning(self.parent, 'File Load Error',
                                      error_str)

    def delete_row(self):
        row_objects = self.tableWidget.selectionModel().selectedRows()
        for row in row_objects:
            self.data_file_container.delete(row.row())
        self.refresh_table()

    def clear_table(self):
        if len(self.data_file_container) == 0:
            return
        self.data_file_container.clear()
        self.refresh_table()

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

    def convert_files(self, parameters):
        if len(self.data_file_container) == 0:
            return
        self.conversion = FileConverter(self.data_file_container, parameters)
        self.progress_dialog = ProgressDialog(self.tableWidget.window())
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
            lambda: self.refresh_table())
        self.conversion.conversion_complete.connect(
            self._check_for_errors_after_conversion)
        self.progress_dialog.show()
        self.conversion.start()

    def _check_for_errors_after_conversion(self):
        success = True
        for file in self.data_file_container:
            if file.status != 'converted':
                success = False
        if not success:
            error_str = 'One or more files could not be converted.'
            QtWidgets.QMessageBox.warning(self.parent, 'Conversion Error',
                                          error_str)

    def confirm_quit(self):
        if len(self.data_file_container) == 0:
            return True
        status = [file.status for file in self.data_file_container]
        if any([True for s in status if s == 'unconverted']):
            reply = QtWidgets.QMessageBox.question(
                self.tableWidget.window(),
                'Confirm Quit',
                'There are unconverted files in the queue. '
                'Are you sure you want to quit?')
            return reply == QtWidgets.QMessageBox.Yes
        else:
            return True
