from mat.tiltcurve import TiltCurve
from PyQt5 import QtCore


class TiltCurveModel(QtCore.QAbstractListModel):
    load_error = QtCore.pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.tilt_tables = []
        self.directory = directory
        self.load_tilt_curves()

    def load_tilt_curves(self):
        tilt_table_paths = self.directory.glob('*.cal')
        for path in tilt_table_paths:
            try:
                this_table = TiltCurve(path)
                self.tilt_tables.append(this_table)
            except (FileNotFoundError, UnicodeDecodeError, ValueError):
                self.load_error.emit('Error loading ' + str(path))
        self.tilt_tables.sort()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tilt_tables)

    def data(self, index, role=None):
        this_table = self.tilt_tables[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return '{} - {} ballast - {} water'.format(
                this_table.model, this_table.ballast, this_table.salinity)
        elif role == QtCore.Qt.UserRole:
            return this_table

    def add(self, thing):
        pos = len(self.tilt_tables)
        self.beginInsertRows(QtCore.QModelIndex(), pos - 1, pos - 1)
        self.tilt_tables.append(thing)
        self.endInsertRows()
