from mat import appdata
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from gui.converter.table_model import DataFile
import os
from gui import dialogs
from gui.gui_utils import error_message


class LoaderController(QObject):
    def __init__(self, model):
        super().__init__()
        #  model is the same object as TableController
        self.model = model
        self.file_loader = FileLoader()
        self.file_loader.load_complete_signal.connect(self.file_loaded)

    # slot
    def add_row(self):
        # called when "Add file" is clicked in the main gui
        file_paths = self._open_file()
        if not file_paths[0]:
            return
        self._update_recent_directory_appdata(file_paths[0][0])
        # pass the file list to the loader thread
        # files will be returned via signals to the "file_loaded" method
        self.file_loader.load_files(file_paths[0])

    # slot
    def file_loaded(self, data_file):
        # receives data_file as a signal from the file_loader thread
        if self._check_for_errors(data_file):
            return
        self.model.add_file(data_file)

    def _open_file(self):
        application_data = appdata.get_userdata('domino.dat')
        last_directory = (application_data['last_directory']
                          if 'last_directory' in application_data else '')
        file_paths = dialogs.open_lid_file(last_directory)
        return file_paths

    def _update_recent_directory_appdata(self, file_path):
        directory = os.path.dirname(file_path)
        appdata.set_userdata('domino.dat', 'last_directory', directory)

    def _check_for_errors(self, data_file):
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
                'contain data.'}
        if data_file.status.startswith('error'):
            error_str = error_map[data_file.status].format(data_file.filename)
            error_message(dialogs.Parent.id(),
                          'Load error',
                          error_str)
            return True


class FileLoader(QThread):
    load_complete_signal = pyqtSignal(DataFile)

    def load_files(self, paths):
        self.paths = paths
        self.run()

    def run(self):
        for path in self.paths:
            data_file = DataFile(path)
            data_file.query_file()
            self.load_complete_signal.emit(data_file)
