from gui.converter.file_loader import FileLoader
import pytest
from queue import Queue
from PyQt5.QtCore import QThread


FILES = ['file1.lid', 'file2.lid', 'file3.lid']


@pytest.fixture
def queue():
    q = Queue()
    q.put(list(FILES))
    return q

@pytest.fixture
def file_loader():
    def file_injector(files):
        q = Queue()
        q.put(files)
        loader = FileLoader(q)
        thread = QThread()
        loader.finished_signal.connect(thread.quit)
        loader.moveToThread(thread)
        thread.start()
        return loader, thread
    return file_injector


def test_create(queue):
    assert FileLoader(queue)


def test_load_good_files(qtbot, queue, mocker, file_loader):
    filename = 'bad_file.lid'
    loader, thread = file_loader(FILES)
    file_mock = mocker.patch('gui.converter.file_loader.DataFile')
    file_mock.return_value.status = 'converted'
    file_mock.return_value.filename = filename
    with qtbot.wait_signal(thread.finished):
        with qtbot.wait_signals([loader.file_loaded_signal]*3):
            loader.run()
    assert thread.isFinished()


def test_load_error(qtbot, queue, mocker, file_loader):
    filename = 'bad_file.lid'
    error_type = 'error_first_page'
    loader, thread = file_loader([filename])
    file_mock = mocker.patch('gui.converter.file_loader.DataFile')
    file_mock.return_value.status = error_type
    file_mock.return_value.filename = filename
    with qtbot.wait_signal(thread.finished):
        with qtbot.wait_signal(loader.file_error_signal):
            loader.run()
    assert thread.isFinished()

    # expected_message = file_loader.error_map[error_type].format(filename)
    #assert blocker.args[0] == expected_message
