from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from mat.data_converter import DataConverter, default_parameters
import os


class FileLoader(QThread):
    load_complete_signal = pyqtSignal()
    load_error_signal = pyqtSignal(str)

    def __init__(self, data_file_container):
        super().__init__()
        self.paths = None
        self.data_file_container = data_file_container

    def load_files(self, paths):
        self.paths = paths
        self.run()

    def run(self):
        self.data_file_container.add_files(self.paths)
        self._check_for_errors()
        self.load_complete_signal.emit()

    def _check_for_errors(self):
        error_map = {
            'error_type':
                'The file "{}" could not be loaded because it is the wrong '
                'file type.',
            'error_first_page':
                'The file "{}" could not be loaded because it does not '
                'contain data.',
            'error_header':
                'The file "{}" could not be loaded because it contains '
                'a header error.'}
        for file in self.data_file_container:
            status = file.status
            if status.startswith('error'):
                error_str = error_map[status].format(file.filename)
                self.load_error_signal.emit(error_str)
        self.data_file_container.remove_error_files()

class FileConverter(QThread):
    progress_signal = pyqtSignal(int, int)
    conversion_status_signal = pyqtSignal(str, int, int)
    conversion_complete = pyqtSignal()

    def __init__(self, data_file_container, parameters):
        # parameters is a dict of parameters required by FileConverter
        super().__init__()
        self.data_file_container = data_file_container
        self.parameters = parameters
        self.current_file_ind = 0
        self.file_sizes = [file.size for file in data_file_container]
        self.total_mb = sum(self.file_sizes)
        self._is_running = False
        self.converter = None

    def run(self):
        self._is_running = True
        for i, file in enumerate(self.data_file_container):
            if not self._is_running:
                break
            self.current_file_ind = i
            self.conversion_status_signal.emit(file.filename,
                                               i+1,
                                               len(self.data_file_container))
            if not os.path.isfile(file.path):
                file.status = 'file_not_found'
                continue
            self._convert_file(file)
        self.conversion_complete.emit()

    def update_progress(self, percent_done):
        # This is an observer function that gets notified when a data
        # page is parsed
        if not self._is_running:
            self.converter.cancel_conversion()
        cumulative_mb = sum([size for size
                             in self.file_sizes[:self.current_file_ind]])
        cumulative_mb += (self.data_file_container[self.current_file_ind].size
                          * (percent_done/100))
        overall_percent = cumulative_mb / self.total_mb
        overall_percent *= 100
        self.progress_signal.emit(percent_done, overall_percent)

    def _convert_file(self, file):
        self.current_file = file
        try:
            conversion_parameters = default_parameters()
            conversion_parameters.update(self.parameters)
            self.converter = DataConverter(file.path, conversion_parameters)
            self.converter.register_observer(self.update_progress)
            self.converter.convert()
            file.status = 'converted'
        except (FileNotFoundError, TypeError, ValueError):
            file.status = 'failed'

    def cancel(self):
        self._is_running = False
