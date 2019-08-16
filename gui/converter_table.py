from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


FILE_NAME = 0
STATUS = 1
SIZE = 2
START_TIME = 3
FOLDER = 4


class ConverterTable:
    def __init__(self, tableWidget, data_file_container):
        self.tableWidget = tableWidget
        self.data_file_container = data_file_container
        self.tableWidget.setSelectionMode(1)
        self.tableWidget.setSelectionBehavior(1)
        self.tableWidget.setColumnWidth(FILE_NAME, 200)
        self.tableWidget.setColumnWidth(STATUS, 100)
        self.tableWidget.setColumnWidth(SIZE, 100)
        self.tableWidget.setColumnWidth(START_TIME, 140)
        self.tableWidget.setColumnWidth(FOLDER, 450)
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeader().setFixedHeight(30)

    def delete_selected_rows(self):
        row_objects = self.tableWidget.selectionModel().selectedRows()
        for row in row_objects:
            self.data_file_container.delete(row.row())
        self.refresh()

    def clear_table(self):
        if len(self.data_file_container) == 0:
            return
        self.data_file_container.clear()
        self.refresh()

    def refresh(self):
        self.tableWidget.setRowCount(len(self.data_file_container))
        for i, data_file in enumerate(self.data_file_container):
            self.tableWidget.setItem(i, FILE_NAME,
                                     self._table_item(data_file.filename))
            self.tableWidget.setItem(i, STATUS,
                                     self._table_item(data_file.status))
            self.tableWidget.setItem(i, FOLDER,
                                     self._table_item(data_file.folder))
            self.tableWidget.setItem(i, SIZE,
                                     self._table_item(data_file.size_str))
            self.tableWidget.setItem(i, START_TIME,
                                     self._table_item(data_file.start_time))

    def _table_item(self, string):
        item = QtWidgets.QTableWidgetItem(string)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        font = QtGui.QFont()
        state = True if string == 'converted' else False
        font.setBold(state)
        item.setFont(font)
        return item
