import os
import sys
from mat.tiltcurve import TiltCurve
import PyQt5.QtCore as qtc
from pathlib import Path
from operator import itemgetter


class TiltCurveModel(qtc.QAbstractListModel):
    load_error = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tilt_tables = []
        try:
            directory = Path(sys._MEIPASS)
        except AttributeError:
            directory = Path(__file__).parent
        self.directory = directory / 'Calibration Tables'
        self.load_tilt_curves()

    def load_tilt_curves(self):
        tilt_table_paths = list(self.directory.glob('*.cal'))
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
        if role == qtc.Qt.DisplayRole:
            this_table = self.tilt_tables[index.row()]
            return '{} - {} ballast - {} water'.format(
                this_table.model, this_table.ballast, this_table.salinity)

    def add(self, thing):
        pos = len(self.tilt_tables)
        self.beginInsertRows(qtc.QModelIndex(), pos - 1, pos - 1)
        self.tilt_tables.append(thing)
        self.endInsertRows()
