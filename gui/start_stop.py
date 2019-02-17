# GPLv3 License
# Copyright (c) 2019 Lowell Instruments, LLC, some rights reserved
import logging
logging.basicConfig(level=logging.DEBUG, filename='query.log', filemode='w')
from gui.start_stop_ui import Ui_Frame
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QStatusBar, QLabel
from mat.logger_controller_usb import LoggerControllerUSB
from datetime import datetime
from gui.start_stop_updater import Commands, ConnectionStatus
from queue import Queue
from PyQt5.QtWidgets import QHeaderView, QMessageBox
from PyQt5.QtWidgets import QApplication


TIME_FIELD = 2


class StartStopFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.commands = None
        self.logger = None
        self.status_bar = None
        self.statusbar_serial_number = QLabel()
        self.statusbar_logging_status = QLabel()
        self.connection_status = ConnectionStatus(self)

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.commands = Commands(self)
        self.logger = LoggerQueryThread(self.commands.get_schedule())
        self.logger.query_update.connect(self.query_slot)
        self.logger.connected.connect(self.connected_slot)
        logging.debug('Starting logger thread')
        self.logger.start()
        self.time_updater = TimeUpdater()
        self.time_updater.time_signal.connect(self.update_time_slot)
        self.time_updater.start()
        self.pushButton_sync_clock.clicked.connect(
            lambda: self.logger.command('sync_time'))
        self.pushButton_start.clicked.connect(self.run)
        self.pushButton_stop.clicked.connect(self.stop)
        self.pushButton_connected.clicked.connect(self.reset)
        self.status_bar = self.get_status_bar()
        self.status_bar.addPermanentWidget(self.statusbar_serial_number)
        self.status_bar.addPermanentWidget(self.statusbar_logging_status)

    def get_status_bar(self):
        window_children = self.frame.window().children()
        for child in window_children:
            if isinstance(child, QStatusBar):
                return child

    def reset(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier | Qt.ControlModifier:
            self.logger.command('RST')
        elif modifiers == Qt.ControlModifier:
            self.logger.toggle_active()

    def query_slot(self, query_results):
        logging.debug(query_results)
        command, data = query_results
        if data:
            self.commands.command_handler(query_results)

    def connected_slot(self, state):
        self.connection_status.update(state)

    def run(self):
        style_sheet = self.label_logger_time.styleSheet()
        if style_sheet == 'background-color: rgb(255, 255, 0);':
            if not self.confirm_run_with_different_time():
                return

        self.pushButton_sync_clock.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.logger.command('RUN')

    def confirm_run_with_different_time(self):
        message = 'Device time differs from computer time by more than 1 ' \
                  'minute. Do you still want to start the device?'
        answer = QMessageBox.warning(self.frame, 'Check Time',
                                     message,
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        return answer == QMessageBox.Yes

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
    connected = pyqtSignal(bool)

    def __init__(self, commands):
        super().__init__()
        logging.debug('thread init')
        self.commands = commands
        self.controller = LoggerControllerUSB()
        logging.debug(self.controller)
        self.queue = Queue()
        self.is_active = False

    def command(self, command):
        self.queue.put(command)

    def run(self):
        self.is_active = True
        while True:
            if self.is_active and self.try_connecting():
                self.connected.emit(True)
                self.start_query_loop()
            else:
                self.connected.emit(False)
                self.sleep(1)

    def toggle_active(self):
        self.is_active = not self.is_active

    def start_query_loop(self):
        while self.is_active and self.controller.is_connected:
            next_command = self.get_next_command()
            if next_command:
                result = self._send_command(next_command)
                self.query_update.emit((next_command, result))
            self.msleep(10)

    def try_connecting(self):
        try:
            return True if self.controller.open_port() else False
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
