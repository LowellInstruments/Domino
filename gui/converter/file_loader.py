from PyQt5.QtCore import pyqtSignal, QObject
from gui.converter.table_model import DataFile


error_map = {
    'error_type':
        'The file "{}" could not be loaded because it is the wrong '
        'file type.',
    'error_first_page':
        'The file "{}" could not be loaded because it does not '
        'contain data.',
    'error_header':
        'The file "{}" could not be loaded because it contains '
        'a header error.',
    'error_no_data':
        'The file "{}" could not be loaded because it does not ' \
        'contain data.'
}


class FileLoader(QObject):
    file_loaded_signal = pyqtSignal(object)
    file_error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        paths = self.queue.get()
        for path in paths:
            data_file = DataFile(path)
            data_file.query_file()
            error = self._check_for_errors(data_file)
            if error:
                self.file_error_signal.emit(error)
            else:
                self.file_loaded_signal.emit(data_file)
        self.finished_signal.emit()

    def _check_for_errors(self, data_file):
        if data_file.status.startswith('error'):
            return error_map[data_file.status].format(data_file.filename)
