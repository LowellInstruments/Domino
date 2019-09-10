from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition, QObject
from mat.data_converter import DataConverter, default_parameters
from gui.progress_dialog import ProgressDialog
from gui import dialogs
import os


class ConversionController(QObject):
    conversion_status_signal = pyqtSignal(str, int, int)
    conversion_complete = pyqtSignal()


    def __init__(self, model, parameters):
        super().__init__()
        self.model = model
        self.file_converter = FileConverter(parameters)
        self.current_file_ind = 0
        self.file_sizes = [file.size if file.status == 'unconverted' else 0
                           for file in model]
        self.total_mb = sum(self.file_sizes)
        self._is_running = False

        self.conversion = FileConverter(self.data_file_container, parameters)
        self.progress_dialog = ProgressDialog(dialogs.Parent.id())
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
            self._check_for_errors_after_conversion)
        self.conversion.file_converted_signal.connect(
            self.converter_table.refresh)
        self.conversion.ask_overwrite_signal.connect(
            self.ask_overwrite_slot)
        self.progress_dialog.show()
        self.conversion.start()

    def convert(self):
        self._is_running = True
        count = 0
        for i, data_file in enumerate(self.model):
            if not os.path.isfile(data_file.path):
                data_file.status = 'not found'
                continue

            if not self._is_running:
                break
            if self.data_file.status != 'unconverted':
                continue
            count += 1

    def update_progress_bar(self):
        cumulative_mb = sum([size for size
                             in self.file_sizes[:self.current_file_ind]])
        cumulative_mb += (self.data_file_container[self.current_file_ind].size
                          * (percent_done / 100))
        overall_percent = cumulative_mb / self.total_mb
        overall_percent *= 100

        self.current_file_ind = i
        self.conversion_status_signal.emit(
            file.filename,
            count,
            sum([1 for x in self.file_sizes if x != 0]))


class FileConverter(QThread):
    progress_signal = pyqtSignal(int)
    file_converted_signal = pyqtSignal(str)
    ask_overwrite_signal = pyqtSignal(str)

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.data_file = None
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.converter = None
        self.overwrite = None

    def convert(self, data_file):
        self.data_file = data_file
        self.start()

    def run(self):
        repeat = False
        try:
            conversion_parameters = default_parameters()
            conversion_parameters.update(self.parameters)
            self.converter = DataConverter(self.data_file.path,
                                           conversion_parameters)
            self.converter.register_observer(self.update_progress)
            self.converter.overwrite = self._process_overwrite()
            self.converter.convert()
            if self.converter._is_running:
                # Make sure converter is still running,
                # canceled conversion isn't marked converted
                status = 'converted'
        except (FileNotFoundError, TypeError, ValueError):
            status = 'failed'
        except FileExistsError as message:
            self.ask_overwrite(self.data_file.filename)
            if self.overwrite in ['once', 'yes_to_all']:
                repeat = True
        finally:
            self.converter.source_file.close(status)
        if repeat:
            self._convert_file(self.data_file)
        self.file_converted_signal.emit()

    def update_progress(self, percent_done):
        # This is an observer function that gets notified when a data
        # page is parsed
        self.progress_signal.emit(percent_done)
        if not self._is_running:
            self.converter.cancel_conversion()

    def _process_overwrite(self):
        action_map = {
            'once': (None, True),
            'yes_to_all': ('yes_to_all', True),
            'no': (None, False),
            'no_to_all': ('no_to_all', False)
        }
        self.overwrite, overwrite_status = action_map.get(self.overwrite,
                                                          (None, False))
        return overwrite_status

    def ask_overwrite(self, filename):
        if self.overwrite is None:
            self.ask_overwrite_signal.emit(str(filename))
            self.mutex.lock()
            self.wait_condition.wait(self.mutex)
            self.mutex.unlock()

    def set_overwrite(self, state):
        self.overwrite = state
        self.wait_condition.wakeAll()

    def cancel(self):
        self._is_running = False
