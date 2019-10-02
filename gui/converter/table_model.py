from pathlib import Path
from mat.data_file_factory import load_data_file, WrongFileTypeError
from datetime import datetime
from mat.sensor_data_file import NoDataError


class DataFile:
    def __init__(self, path):
        self.path = path
        self.folder = str(Path(path).parent)
        self.filename = Path(path).name
        self.size = None
        self.size_str = None
        self.start_time = None
        self.status = None

    def query_file(self):
        try:
            data_file = load_data_file(self.path)
            data_file.page_times()
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


class DataFileContainer:
    def __init__(self):
        self._data_files = []
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer(self)

    def add_file(self, data_file):
        if self._check_for_duplicate(data_file):
            return
        self._data_files.append(data_file)
        self.notify_observers()

    def _check_for_duplicate(self, data_file):
        if data_file.path in [file.path for file in self._data_files]:
            return True
        return False

    def clear(self):
        self._data_files.clear()
        self.notify_observers()

    def delete(self, index):
        del self._data_files[index]
        self.notify_observers()

    def remove_error_files(self):
        self._data_files = [file for file in self._data_files if
                            not file.status.startswith('error')]
        self.notify_observers()

    def reset_converted(self):
        for file in self._data_files:
            if file.status == 'converted':
                file.status = 'unconverted'
        self.notify_observers()

    def reset_errors(self):
        for file in self._data_files:
            if file.status.startswith('error'):
                file.status = 'unconverted'
        self.notify_observers()

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
