from pathlib import Path
from mat.data_file_factory import load_data_file, WrongFileTypeError
from datetime import datetime
from mat.sensor_data_file import NoDataError
from PyQt5 import QtCore, QtGui


class DataFile:
    def __init__(self, path):
        self.path = path
        self.folder = str(Path(path).parent)
        self.filename = Path(path).name
        self.size = None
        self.size_str = None
        self.start_time = None
        self.status = None
        self.header_error = None

    def query_file(self):
        try:
            data_file = load_data_file(self.path)
            self.header_error = data_file.header_error
        except WrongFileTypeError:
            self.status = 'error_type'
            return
        except (KeyError, ValueError):
            self.status = 'error_header'
            return
        except NoDataError:
            self.status = 'error_no_data'
            return

        if len(data_file.page_times()) == 0:
            self.status = 'error_first_page'
            return
        self.size = data_file.file_size() / 1024 ** 2
        self.size_str = '{:.3f}MB'.format(data_file.file_size() / 1024 ** 2)
        start_time = data_file.page_times()[0]
        self.start_time = datetime.utcfromtimestamp(start_time).isoformat()
        data_file.close()
        self.status = 'unconverted'


class DataFileContainer(QtCore.QAbstractTableModel):

    headers = [
        ('Files to Convert', QtCore.QSize(200, 30)),
        ('Status', QtCore.QSize(100, 30)),
        ('Size', QtCore.QSize(100, 30)),
        ('Start Time', QtCore.QSize(140, 30)),
        ('Containing Folder', QtCore.QSize(450, 30))
    ]

    def __init__(self):
        super().__init__()
        self._data_files = []
        self._observers = []

    def rowCount(self, parent):
        return len(self._data_files)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        row, column = index.row(), index.column()
        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                return self._data_files[row].filename
            elif column == 1:
                status = self._data_files[row].status
                if status.startswith('error'):
                    status = 'error'
                return status.capitalize()
            elif column == 2:
                return self._data_files[row].size_str
            elif column == 3:
                return self._data_files[row].start_time
            elif column == 4:
                return self._data_files[row].folder
        if role == QtCore.Qt.FontRole:
            status = self._data_files[row].status
            if column == 1:
                if status.startswith('error') or status == 'converted':
                    font = QtGui.QFont()
                    font.setBold(True)
                    return font

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return self.headers[section][0]
            elif role == QtCore.Qt.SizeHintRole:
                return self.headers[section][1]
            elif role == QtCore.Qt.FontRole:
                font = QtGui.QFont()
                font.setBold(True)
                return font

    def add_file(self, data_file):
        if self._check_for_duplicate(data_file):
            return
        n_files = len(self._data_files)
        self.beginInsertRows(QtCore.QModelIndex(), n_files, n_files)
        self._data_files.append(data_file)
        self.endInsertRows()

    def _check_for_duplicate(self, data_file):
        if data_file.path in [file.path for file in self._data_files]:
            return True
        return False

    def clear(self):
        self.beginResetModel()
        self._data_files.clear()
        self.endResetModel()

    def delete(self, index):
        self.beginResetModel()
        del self._data_files[index]
        self.endResetModel()

    def change_status(self, obj, new_status):
        ind = self._data_files.index(obj)
        self.beginResetModel()
        self._data_files[ind].status = new_status
        self.endResetModel()

    def remove_error_files(self):
        self._data_files = [file for file in self._data_files if
                            not file.status.startswith('error')]
        #self.notify_observers()

    def reset_converted(self):
        for file in self._data_files:
            if file.status == 'converted':
                file.status = 'unconverted'
        #self.notify_observers()

    def reset_errors(self):
        for file in self._data_files:
            if file.status.startswith('error'):
                file.status = 'unconverted'
        #self.notify_observers()

    def unconverted(self):
        # returns the number of unconverted files
        status = [1 for f in self._data_files if f.status != 'converted']
        return sum(status)

    def convertable(self):
        convertable = 0
        for file in self._data_files:
            if not(file.status.startswith('error')):
                convertable += 1
        return convertable

    def errors(self):
        return sum([1 for f in self if f.status.startswith('error')])

    def __getitem__(self, index):
        return self._data_files[index]

    def __iter__(self):
        for file in self._data_files:
            yield file

    def __len__(self):
        return len(self._data_files)
