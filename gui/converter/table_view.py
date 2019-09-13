from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


FILE_NAME = 0
STATUS = 1
SIZE = 2
START_TIME = 3
FOLDER = 4


class ConverterTable:
    def __init__(self, table_widget):
        self.tableWidget = table_widget
        self.tableWidget.setSelectionMode(1)
        self.tableWidget.setSelectionBehavior(1)
        self.tableWidget.setColumnWidth(FILE_NAME, 200)
        self.tableWidget.setColumnWidth(STATUS, 100)
        self.tableWidget.setColumnWidth(SIZE, 100)
        self.tableWidget.setColumnWidth(START_TIME, 140)
        self.tableWidget.setColumnWidth(FOLDER, 450)
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeader().setFixedHeight(30)

    def selected_row(self):
        return self.tableWidget.selectionModel().selectedRows()

    def refresh(self, model):
        self.tableWidget.setRowCount(len(model))
        for i, data_file in enumerate(model):
            self.tableWidget.setItem(i, FILE_NAME,
                                     self._table_item(data_file.filename))
            status = data_file.status
            if data_file.status.startswith('error'):
                status = 'error'
            self.tableWidget.setItem(i, STATUS, self._table_item(status))
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
        state = True if string in ['converted', 'error'] else False
        font.setBold(state)
        item.setFont(font)
        return item
