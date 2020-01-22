# GPLv3 License
# Copyright (c) 2019 Lowell Instruments, LLC, some rights reserved
import logging
import time
logging.basicConfig(level=logging.DEBUG, filename='query.log', filemode='w')
from gui.start_stop_ui import Ui_Frame
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSysInfo
from PyQt5.QtWidgets import QStatusBar, QLabel
from mat.logger_controller_usb import LoggerControllerUSB
from mat.logger_controller import CommunicationError
from mat.calibration_factories import DEFAULT_COEFFICIENTS
from datetime import datetime
from gui.start_stop_updater import Commands, ConnectionStatus, ERROR_CODES
from gui import start_stop_updater
from PyQt5.QtWidgets import QHeaderView, QMessageBox
from PyQt5.QtWidgets import QApplication
from queue import Queue
from gui import dialogs


TIME_FIELD = 2


class StartStopFrame(Ui_Frame):
    def __init__(self):
        self.frame = None
        self.commands = None
        self.logger = None
        self.status_bar = None
        self.statusbar_serial_number = QLabel()
        self.statusbar_logging_status = QLabel()
        self.statusbar_connect_status = QLabel()
        self.connection_status = ConnectionStatus(self)
        self.queue = Queue()
        self.try_connecting = True

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        self.tableWidget.horizontalHeader().setFixedHeight(30)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_width = self.tableWidget.horizontalHeader().length()
        self.tableWidget.setFixedSize(
            table_width,
            self.tableWidget.verticalHeader().length()
            + self.tableWidget.horizontalHeader().height()
        )
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.tableWidget.setColumnWidth(0, table_width / 2)
        self.tableWidget.setColumnWidth(1, table_width / 4)
        self.tableWidget.setColumnWidth(2, table_width / 4)
        if QSysInfo.productType() == 'windows' and QSysInfo.productVersion() == '10':
            self.tableWidget.horizontalHeader().setStyleSheet(
                'border-top: 0px; '
                'border-left: 0px; '
                'border-right: 0px; '
                'border-bottom: 1px solid gray;')
        self.commands = Commands(self)
        self.logger = LoggerQueryThread(self.commands,
                                        self.queue)
        self.logger.query_update.connect(self.query_slot)
        self.logger.connected.connect(self.connected_slot)
        self.logger.error_code.connect(self.show_run_error)
        self.logger.error_message.connect(self.show_warning)
        self.logger.start()
        self.time_updater = TimeUpdater()
        self.time_updater.time_signal.connect(self.update_time_slot)
        self.time_updater.start()
        self.pushButton_sync_clock.clicked.connect(
            lambda: self.queue.put('sync_time'))
        self.pushButton_start.clicked.connect(self.run)
        self.pushButton_stop.clicked.connect(self.stop)
        self.pushButton_connected.clicked.connect(self.reset)
        self.status_bar = self.get_status_bar()
        self.status_bar.addPermanentWidget(self.statusbar_connect_status)
        self.statusbar_connect_status.setText('  Auto Connect  ')
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
            self.queue.put('RST')
        elif modifiers == Qt.ControlModifier:
            if self.try_connecting == True:
                self.queue.put('disconnect')
                self.statusbar_connect_status.setText(
                    '  Manually Disconnected  ')
            else:
                self.logger.start()
                self.statusbar_connect_status.setText('  Auto Connect  ')
            self.try_connecting = not(self.try_connecting)

    def query_slot(self, query_results):
        logging.debug(query_results)
        command, data = query_results
        if data is not None:
            self.commands.notify_handlers(query_results)

    def connected_slot(self, state):
        self.connection_status.update(state)

    def run(self):
        style_sheet = self.label_logger_time.styleSheet()
        if style_sheet == 'background-color: rgb(255, 255, 0);':
            if not self.confirm_run_with_different_time():
                return

        self.pushButton_sync_clock.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.queue.put('RUN')
        self.queue.put('POST_RUN_STATUS')

    def confirm_run_with_different_time(self):
        message = 'Device time differs from computer time by more than 1 ' \
                  'minute. Do you still want to start the device?'
        answer = QMessageBox.warning(self.frame, 'Check Time',
                                     message,
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        return answer == QMessageBox.Yes

    def show_run_error(self, code):
        status_str = 'Device failed to start'
        for value, string in ERROR_CODES:
            if code & value:
                status_str += ' - {}'.format(string)
        status_str += ' (error code 0x{})'.format(code)
        dialogs.error_message('Error', status_str)

    def stop(self):
        self.pushButton_stop.setEnabled(False)
        self.queue.put('STP')

    def update_time_slot(self, time_str):
        if self.logger.is_connected:
            text = 'Computer Time: {}'.format(time_str)
        else:
            text = 'Computer Time: --'
        self.label_computer_time.setText(text)

    def show_warning(self, title, message):
        dialogs.error_message(title, message)


class TimeUpdater(QThread):
    time_signal = pyqtSignal(str)

    def run(self):
        while True:
            time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            self.time_signal.emit(time)
            self.msleep(250)


class LoggerQueryThread(QThread):
    query_update = pyqtSignal(tuple)
    connected = pyqtSignal(bool)
    error_code = pyqtSignal(int)
    error_message = pyqtSignal(str, str)

    def __init__(self, commands, queue):
        super().__init__()
        self.commands = commands
        self.queue = queue
        self.is_active = False
        self.is_connected = False
        self.time = time.monotonic()

    def run(self):
        self.is_active = True
        while self.is_active:
            if self.read_queue() == 'disconnect':
                self.is_active = False
            with LoggerControllerUSB() as controller:
                if controller is not None:
                    self.commands.reset()
                    self._update_connection_status(True)
                    self.queue.put('load_calibration')
                    self.start_query_loop(controller)
                else:
                    self._update_connection_status(False)
            self.msleep(250)
        self._update_connection_status(False)

    def _update_connection_status(self, status):
        self.is_connected = status
        self.connected.emit(status)

    def start_query_loop(self, controller):
        while controller.is_connected and self.is_active:
            next_command = self.get_next_command()
            if next_command == 'disconnect':
                self.is_active = False
                break

            elif next_command == 'POST_RUN_STATUS':
                result = self._send_command(controller, 'STS')
                if int(result) & 252:
                    self.error_code.emit(int(result) & 252)

            elif next_command == 'load_calibration':
                if controller.calibration.coefficients == DEFAULT_COEFFICIENTS:
                    self.error_message.emit(
                        'Warning',
                        'Calibration values on your device are missing, invalid, or outdated.')

            elif next_command is not None:
                result = self._send_command(controller, next_command)
                if next_command == 'GFV':
                    if result != '1.0.124':
                        self.commands.supports_gls(True)
                self.query_update.emit((next_command, result))

            self.msleep(50)

    def get_next_command(self):
        queue = self.read_queue()
        if queue:
            return queue
        return self.commands.next_command()

    def read_queue(self):
        if not self.queue.empty():
            return self.queue.get()

    def _send_command(self, controller, command):
        try:
            if len(command) == 3:
                return controller.command(command)
            return getattr(controller, command)()
        except (RuntimeError, CommunicationError):
            return None

    def _clear_queue(self):
        # Note sure if this is needed anymore
        with self.queue.mutex:
            self.queue.queue.clear()
