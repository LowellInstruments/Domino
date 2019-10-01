import time
from gui.sensor_formats import hundredths_format, thousands_format, int_format
from re import search
from PyQt5 import QtGui, QtCore, QtWidgets
from numpy import ndarray
from collections import OrderedDict
from datetime import datetime
from gui.start_stop_clear import clear_gui
from enum import Enum


# [Command, repeat interval, class]
COMMANDS = [
    ['GTM', 1, 'TimeUpdate'],
    ['STS', 1, 'StatusUpdate'],
    ['get_logger_settings', 10, 'SensorUpdate'],
    ['get_sensor_readings', 1, 'SensorUpdate'],
    ['logger_info', 10, 'DeploymentUpdate'],
    ['FSZ', 5, 'FileSizeUpdate'],
    ['CTS', 10, 'FileSizeUpdate'],
    ['CFS', 10, 'FileSizeUpdate'],
    ['GSN', 10, 'SerialNumberUpdate'],
    ['GFV', 10, 'SimpleUpdate']
]

FILE_SIZE = {
    'FSZ': ('File size {:0.2f} MB', 'label_file_size'),
    'CTS': (' of {:0.2f} GB available', 'label_sd_total_space'),
    'CFS': ('SD card free space: {:0.2f}','label_sd_free_space')
}

SIMPLE_FIELD = {
    'GTM': ('Logger Time: {}', 'label_logger_time'),
    'GFV': ('Firmware Version: {}', 'label_firmware')
}

SENSORS = OrderedDict(
    [('ax', thousands_format),
     ('ay', thousands_format),
     ('az', thousands_format),
     ('mx', int_format),
     ('my', int_format),
     ('mz', int_format),
     ('temp', thousands_format),
     ('batt', hundredths_format)]
)

LOGGER_INFO = {
    'DP': ('Deployment Number: {}', 'label_deployment'),
    'MN': ('Model Number: {}', 'label_model')
}

ERROR_CODES = [
    (2, 'Delayed start'),
    (4, 'SD card error'),
    (8, 'MAT.cfg error'),
    (16, 'Safe shutdown'),
    (32, 'SD retry error'),
    (64, 'ADXL data error'),
    (128, 'Stack Overflow')
]


class Commands:
    def __init__(self, gui):
        self.gui = gui
        self.command_schedule = []
        self.command_handlers = {}
        self.make_commands()

    def make_commands(self):
        self.command_handlers = {}
        for command, _, klass in COMMANDS:

            existing_handler = self.get_existing(globals()[klass])
            if existing_handler:
                self.command_handlers[command] = existing_handler
            else:
                handler_type = globals()[klass]
                self.command_handlers[command] = handler_type(self.gui)

    def get_existing(self, klass):
        for handler in self.command_handlers.values():
            #import pdb; pdb.set_trace()
            if type(handler) == klass:
                return handler

    def get_schedule(self):
        command_schedule = []
        for command, repeat, _ in COMMANDS:
            command_schedule.append([command, repeat, 0])
        return list(command_schedule)

    def command_handler(self, query_results):
        query_command, data = query_results
        handler = self.command_handlers.get(query_command)
        if handler:
            handler.update(query_results)


class Update:
    def __init__(self, gui):
        self.gui = gui

    def update(self, query_results):
        raise NotImplementedError


class SimpleUpdate(Update):
    def __init__(self, gui):
        super().__init__(gui)
        self.widget = None

    def update(self, query_results):
        command, data = query_results
        format_, widget_name = SIMPLE_FIELD[command]
        self.widget = getattr(self.gui, widget_name)
        self.widget.setText(format_.format(data))


class SensorUpdate(Update):
    ASSOCIATED_CHANNELS = {
        'ACL': ['ax', 'ay', 'az'],
        'MGN': ['mx', 'my', 'mz'],
        'TMP': ['temp']}

    def __init__(self, gui):
        super().__init__(gui)
        self.logger_settings = None
        self.last_readings = None

    def update(self, query_results):
        if query_results[0] == 'get_logger_settings':
            self.logger_settings = query_results[1]
            self.supports_gls = True
            self.gls_status_determined = True
        elif query_results[0] == 'get_sensor_readings':
            self.redraw_table(query_results[1])

    def redraw_table(self, data):
        for index, sensor in enumerate(SENSORS.keys()):
            self._set_item_text(index, 1, self.enabled_str(sensor))
            self._set_item_text(index, 2, self.value_string(sensor, data))

    def _set_item_text(self, row, col, value):
        item = QtWidgets.QTableWidgetItem(value)
        self.gui.tableWidget.setItem(row, col, item)

    def enabled_str(self, channel):
        if channel == 'batt':
            status = 'n/a'
        elif self.logger_settings:
            status = 'Yes' if self._sensor_enabled(channel) else 'No'
        else:
            status = '--'
        return status

    def _sensor_enabled(self, channel):
        for sensor, channels in self.ASSOCIATED_CHANNELS.items():
            if channel in channels:
                return self.logger_settings[sensor]

    def value_string(self, sensor, readings):
        if not readings:
            return ''
        reading = readings.get(sensor, '')
        if isinstance(reading, ndarray):
            return self._format_sensor_value(sensor, reading[0])
        return self._format_sensor_value(sensor, reading)

    def _format_sensor_value(self, sensor, value):
        return SENSORS[sensor](value)


class TimeUpdate(SimpleUpdate):
    def update(self, query_results):
        super().update(query_results)
        _, data = query_results
        logger_time = datetime.strptime(data, '%Y/%m/%d %H:%M:%S')
        computer_time = datetime.now()
        diff = abs(logger_time - computer_time).total_seconds()
        if diff > 60:
            style = 'background-color: rgb(255, 255, 0);'
        else:
            style = ''
        self.widget.setStyleSheet(style)


class SerialNumberUpdate(Update):
    def update(self, query_results):
        command, data = query_results
        self.gui.label_serial.setText('Serial Number: {}'.format(data))
        self.gui.statusbar_serial_number.setText(
            '  Connected to {}  '.format(data))


class FileSizeUpdate(Update):
    def update(self, query_results):
        command, data = query_results
        format_, widget_name = FILE_SIZE[command]
        self.widget = getattr(self.gui, widget_name)
        numeric_data = search('[0-9]+', data).group()
        numeric_data = float(numeric_data) / 1024**2
        self.widget.setText(format_.format(numeric_data))


class StatusUpdate(Update):
    def __init__(self, gui):
        super().__init__(gui)
        self.gui = gui
        self.rabbit_icon = QtGui.QIcon()
        self.rabbit_icon.addPixmap(
            QtGui.QPixmap(':/icons/icons/icons8-running-rabbit-48.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopped_icon = QtGui.QIcon()
        self.stopped_icon.addPixmap(
            QtGui.QPixmap(':/icons/icons/icons8-private-48.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def update(self, query_results):
        command, data = query_results
        status_code = int(data, 16)
        self._show_running(self._running(status_code))
        self.gui.label_status.setText(self.description(status_code))

    def _running(self, status_code):
        return False if status_code & 1 else True

    def description(self, status_code):
        running = 'running' if self._running(status_code) else 'halted'
        status_str = 'Device is {}'.format(running)
        for value, string in ERROR_CODES:
            if status_code & value:
                status_str += ' - {}'.format(string)
        return status_str

    def _show_running(self, state):
        self.gui.pushButton_start.setEnabled(not state)
        self.gui.pushButton_stop.setEnabled(state)
        self.gui.pushButton_sync_clock.setEnabled(not state)
        icon = self.rabbit_icon if state is True else self.stopped_icon
        self.gui.pushButton_status.setIcon(icon)
        self.gui.pushButton_status.setIconSize(QtCore.QSize(36, 36))
        status = '  Device Running  ' if state else '  Halted  '
        self.gui.statusbar_logging_status.setText(status)


class DeploymentUpdate(Update):
    def update(self, query_results):
        command, data = query_results
        for tag in LOGGER_INFO:
            if tag in data:
                format_, widget_name = LOGGER_INFO[tag]
                widget = getattr(self.gui, widget_name)
                widget.setText(format_.format(data[tag]))


class ConnectionStatus:
    def __init__(self, gui):
        self.gui = gui
        self.last_state = None
        self.connected_icon = QtGui.QIcon()
        self.connected_icon.addPixmap(
            QtGui.QPixmap(':/icons/icons/icons8-usb-connected-48.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.not_connected_icon = QtGui.QIcon()
        self.not_connected_icon.addPixmap(
            QtGui.QPixmap(':/icons/icons/icons8-usb-disconnected-48.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def update(self, state):
        buttons = [self.gui.pushButton_sync_clock,
                   self.gui.pushButton_start,
                   self.gui.pushButton_stop]
        if state == self.last_state:
            return
        self.last_state = state
        for button in buttons:
            button.setEnabled(state)
        if state is False:
            clear_gui(self.gui)
            self.gui.pushButton_connected.setIcon(self.not_connected_icon)
        else:
            self.gui.pushButton_connected.setIcon(self.connected_icon)
            self.gui.label_connected.setText('Connected on USB')
