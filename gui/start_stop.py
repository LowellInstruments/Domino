import logging
logging.basicConfig(level=logging.DEBUG, filename='query.log', filemode='w')
from gui.start_stop_ui import Ui_Frame
from PyQt5.QtCore import QThread, pyqtSignal
from mat.logger_controller import LoggerController
from datetime import datetime
from gui.start_stop_updater import Commands
from queue import Queue
from PyQt5.QtWidgets import QHeaderView


TIME_FIELD = 2


class StartStopFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.commands = None
        self.logger = None

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.commands = Commands(self)
        self.logger = LoggerQueryThread(self.commands.get_schedule())
        self.logger.query_update.connect(self.query_slot)
        logging.debug('Starting logger thread')
        self.logger.start()
        self.time_updater = TimeUpdater()
        self.time_updater.time_signal.connect(self.update_time_slot)
        self.time_updater.start()
        self.pushButton_sync_clock.clicked.connect(
            lambda: self.logger.command('sync_time'))
        self.pushButton_start.clicked.connect(self.run)
        self.pushButton_stop.clicked.connect(self.stop)

    def query_slot(self, query_results):
        logging.debug(query_results)
        command, data = query_results
        if data:
            self.commands.command_handler(query_results)

    def run(self):
        self.pushButton_sync_clock.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.logger.command('RUN')

    def stop(self):
        self.pushButton_stop.setEnabled(False)
        self.logger.command('STP')

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
        logging.debug('thread init')
        self.commands = commands
        self.controller = LoggerController()
        logging.debug(self.controller)
        self.queue = Queue()
        self.queue.put('load_logger_info')

    def command(self, command):
        self.queue.put(command)

    def run(self):
        logging.debug('Entered thread')
        while True:
            if not self.try_connecting():
                self.sleep(1)
            while self.controller.is_connected:
                next_command = self.get_next_command()
                if next_command:
                    result = self._send_command(next_command)
                    self.query_update.emit((next_command, result))
                self.msleep(10)

    def try_connecting(self):
        try:
            self.controller.open_port()
            return True
        except RuntimeError:
            return False

    def get_next_command(self):
        if not self.queue.empty():
            return self.queue.get()
        now = datetime.now().timestamp()
        for i, (command, repeat, next_time) in enumerate(self.commands):
            if now > next_time:
                self.commands[i][TIME_FIELD] = now + repeat
                return command

    def check_user_command(self):
        if not self.queue.empty():
            self._send_command(self.queue.get())

    def _send_command(self, command):
        try:
            if len(command) == 3:
                return self.controller.command(command)
            return getattr(self.controller, command)()
        except RuntimeError:
            return None