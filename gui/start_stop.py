from gui.start_stop_ui import Ui_Frame
from PyQt5.QtCore import QThread, pyqtSignal
from mat.logger_controller import (
    LoggerController,
    TIME_CMD,
    STATUS_CMD,
    LOGGER_INFO_CMD,
    SD_CAPACITY_CMD,
    SD_FILE_SIZE_CMD,
    SD_FREE_SPACE_CMD,
    SENSOR_READINGS_CMD)
from datetime import datetime


class StartStopFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        commands = {TIME_CMD: [1, 0],
                    STATUS_CMD: [1, 0]}
        self.logger = LoggerQueryThread(commands)
        self.logger.query_update.connect(self.query_slot)

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.logger.start()

    def query_slot(self, query_results):
        pass
        #send to refresher


class Refresher:
    def __init__(self):
        pass


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
                result = self.controller.command(next_command)
                self.query_update.emit((next_command, result))
            self.msleep(5)

    def get_next_command(self):
        now = datetime.now().timestamp()
        for command in self.commands:
            interval, next_time = self.commands[command]
            if now > next_time:
                self.commands[command][1] = now + interval
                return command
