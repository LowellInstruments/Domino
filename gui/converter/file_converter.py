from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition, QObject
from mat.data_converter import DataConverter, default_parameters
from gui.progress_dialog import ProgressDialog
from gui import dialogs
import os


class ConverterController(QObject):
    conversion_complete = pyqtSignal()

    def __init__(self, model, parameters):
        super().__init__()
        self.model = model
        self.parameters = parameters
        self.progress_dialog = ProgressDialog(dialogs.Parent.id())

    def convert(self):
        if len(self.model) == 0:
            return
        self.converter = FileConverter(self.model, self.parameters)
        self.progress_dialog.ui.pushButton.clicked.connect(
            self.converter.cancel)
        self.progress_dialog.ui.pushButton.clicked.connect(
            self.progress_dialog.click_cancel)
        self.converter.progress_signal.connect(
            self.progress_dialog.update_progress)
        self.converter.conversion_status_signal.connect(
            self.progress_dialog.update_status)
        self.converter.conversion_complete.connect(
            self.progress_dialog.conversion_complete)
        self.converter.conversion_complete.connect(
            self.model.notify_observers)
        self.converter.conversion_complete.connect(self.finished)
        self.converter.ask_overwrite_signal.connect(self.ask_overwrite)
        self.progress_dialog.show()
        self.converter.start()

    # slot
    def ask_overwrite(self, filename):
        response = dialogs.ask_overwrite(filename)
        self.converter.set_overwrite(response)

    # slot
    def finished(self):
        self.conversion_complete.emit()


class FileConverter(QThread):
    progress_signal = pyqtSignal(int, int)
    conversion_status_signal = pyqtSignal(str, int, int)
    file_converted_signal = pyqtSignal()
    conversion_complete = pyqtSignal()
    ask_overwrite_signal = pyqtSignal(str)

    def __init__(self, data_file_container, parameters):
        # parameters is a dict of parameters required by FileConverter
        super().__init__()
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.data_file_container = data_file_container
        self.parameters = parameters
        self.current_file_ind = 0
        self.file_sizes = [file.size if file.status == 'unconverted' else 0
                           for file in data_file_container]
        self.total_mb = sum(self.file_sizes)
        self._is_running = False
        self.converter = None
        self.overwrite = None

    def run(self):
        self._is_running = True
        count = 0
        for i, file in enumerate(self.data_file_container):
            if not self._is_running:
                break
            if file.status != 'unconverted':
                continue
            count += 1
            self.current_file_ind = i
            self.conversion_status_signal.emit(
                file.filename,
                count,
                sum([1 for x in self.file_sizes if x != 0]))
            if not os.path.isfile(file.path):
                file.status = 'not found'
                continue
            self._convert_file(file)
            self.file_converted_signal.emit()
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
        repeat = False
        try:
            conversion_parameters = default_parameters()
            conversion_parameters.update(self.parameters)
            self.converter = DataConverter(file.path, conversion_parameters)
            self.converter.register_observer(self.update_progress)
            self.converter.overwrite = self._process_overwrite()
            self.converter.convert()
            file.status = 'converted'
        except (FileNotFoundError, TypeError, ValueError):
            file.status = 'failed'
        except FileExistsError as message:
            self.ask_overwrite(file.filename)
            if self.overwrite in ['once', 'yes_to_all']:
                repeat = True
        finally:
            self.converter.source_file.close()

        # check for the case that the conversion was canceled
        if not self.converter._is_running:
            file.status = 'unconverted'

        if repeat:
            self._convert_file(file)

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
