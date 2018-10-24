from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from datetime import datetime
from mat.data_file_factory import load_data_file
import os


class FileLoader(QThread):
    load_complete_signal = pyqtSignal(list)
    load_error_signal = pyqtSignal(str)

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
