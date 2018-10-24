from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from mat.data_converter import DataConverter, ConversionParameters
from copy import deepcopy
import os


class FileConverter(QThread):
    progress_signal = pyqtSignal(int, int)
    conversion_status_signal = pyqtSignal(str, int, int)
    conversion_complete = pyqtSignal(list)

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
