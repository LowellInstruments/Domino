from gui.start_stop_ui import Ui_Frame
from PyQt5.QtCore import QThread, pyqtSignal
from mat.logger_controller import LoggerController
from datetime import datetime
from gui.start_stop_elements import build_commands
from queue import Queue


class StartStopFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.commands = None
        self.logger = None

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.commands = build_commands('gui/commands.yml', self)
        self.logger = LoggerQueryThread(self.commands)
        self.logger.query_update.connect(self.query_slot)
        self.logger.start()
        self.time_updater = TimeUpdater()
        self.time_updater.time_signal.connect(self.update_time_slot)
        self.time_updater.start()
        self.pushButton_sync_clock.clicked.connect(
            lambda: self.logger.queue.put('sync_time'))
        self.pushButton_start.clicked.connect(self.run)
        self.pushButton_stop.clicked.connect(self.stop)

    def query_slot(self, query_results):
        tag, data = query_results
        if data:
            self.commands[tag]['update'].update(data)

    def run(self):
        self.pushButton_sync_clock.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.logger.queue.put('RUN')

    def stop(self):
        self.pushButton_stop.setEnabled(False)
        self.logger.queue.put('STP')

    def update_time_slot(self, time_str):
        self.label_computer_time.setText('Computer Time: {}'.format(time_str))


class TimeUpdater(QThread):
    time_signal = pyqtSignal(str)

    def run(self):
        while True:
            time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            self.time_signal.emit(time)
            self.sleep(1)


class LoggerQueryThread(QThread):
    query_update = pyqtSignal(tuple)

    def __init__(self, commands):
        super().__init__()
        self.commands = commands
        self.controller = LoggerController()
        self.queue = Queue()

    def sync_time(self):
        self._sync_time = True

    def run(self):
        self.controller.open_port()
        while self.controller.is_connected:
            if not self.queue.empty():
                self._query(self.queue.get())
            next_command = self.get_next_command()
            if next_command:
                result = self._query(next_command)
                self.query_update.emit((next_command, result))
            self.msleep(5)

    def _query(self, command):
        try:
            if len(command) == 3:
                return self.controller.command(command)
            return getattr(self.controller, command)()
        except RuntimeError:
            return None

    def get_next_command(self):
        now = datetime.now().timestamp()
        for command in self.commands:
            next_time = self.commands[command]['next_update']
            if now > next_time:
                interval = self.commands[command]['interval']
                self.commands[command]['next_update'] = now + interval
                return command
