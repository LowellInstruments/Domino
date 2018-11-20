from gui.start_stop_ui import Ui_Frame
from PyQt5.QtCore import QThread, pyqtSignal
from mat.logger_controller import LoggerController
from datetime import datetime
from gui.start_stop_elements import build_commands


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

    def query_slot(self, query_results):
        tag, data = query_results
        self.commands[tag]['update'].update(data)


class LoggerQueryThread(QThread):
    query_update = pyqtSignal(tuple)

    def __init__(self, commands):
        super().__init__()
        self.commands = commands
        self.controller = LoggerController()

    def run(self):
        self.controller.open_port()
        while self.controller.is_connected:
            next_command = self.get_next_command()
            if next_command:
                result = self._query(next_command)
                self.query_update.emit((next_command, result))
            self.msleep(5)

    def _query(self, command):
        if len(command) == 3:
            return self.controller.command(command)
        return getattr(self.controller, command)()

    def get_next_command(self):
        now = datetime.now().timestamp()
        for command in self.commands:
            next_time = self.commands[command]['next_update']
            if now > next_time:
                interval = self.commands[command]['interval']
                self.commands[command]['next_update'] = now + interval
                return command
