from pathlib import Path
from mat.data_file_factory import load_data_file, WrongFileTypeError
from datetime import datetime


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

    def add_files(self, paths):
        for path in paths:
            if self._check_for_duplicate(path):
                continue
            data_file = DataFile(path)
            data_file.query_file()
            self._data_files.append(data_file)

    def _check_for_duplicate(self, path):
        if path in [file.path for file in self._data_files]:
            return True
        return False

    def clear(self):
        self._data_files.clear()

    def delete(self, index):
        del self._data_files[index]

    def remove_error_files(self):
        self._data_files = [file for file in self._data_files if
                            not file.status.startswith('error')]

    def reset_converted(self):
        for file in self._data_files:
            if file.status == 'converted':
                file.status = 'unconverted'

    def __getitem__(self, index):
        return self._data_files[index]

    def __iter__(self):
        for file in self._data_files:
            yield file

    def __len__(self):
        return len(self._data_files)
