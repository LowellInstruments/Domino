import time
from gui.sensor_formats import hundredths_format, thousands_format, int_format
from re import search
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from numpy import ndarray
from collections import OrderedDict
from datetime import datetime
from gui.start_stop_clear import clear_gui
from gui.description_generator import DescriptionGenerator
from setup_file.setup_file import SetupFile


FILE_SIZE = {
    'FSZ': ('File size {:0.2f} MB', 'label_file_size'),
    'CTS': (' of {:0.2f} GB available', 'label_sd_total_space'),
    'CFS': ('SD card free space: {:0.2f}', 'label_sd_free_space')
}

SIMPLE_FIELD = {
    'GTM': ('Device Time: {}', 'label_logger_time'),
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
    (4, 'SD card problem'),
    (8, 'Configuration file (MAT.cfg) missing or invalid'),
    (16, 'Battery critically low'),
    (32, 'SD Card Problem'),
    (64, 'Data error'),
    (128, 'Stack Overflow')
]


class Commands:
    def __init__(self, gui):
        self.gui = gui
        self.command_schedule = []
        self.command_handlers = []
        self.gls_set = False
        self.HANDLER_CLASSES = [
            TimeUpdate,
            StatusUpdate,
            SensorUpdate,
            DeploymentUpdate,
            FileSizeUpdate,
            SerialNumberUpdate,
            SimpleUpdate,
            StuckSensor
        ]
        # (Command, repeat interval)
        self.COMMANDS = [
            ('GFV', 10),
            ('GTM', 1),
            ('STS', 1),
            ('get_sensor_readings', 1),
            ('logger_info', 10),
            ('FSZ', 5),
            ('CTS', 10),
            ('CFS', 10),
            ('GSN', 10)
        ]
        self.reset()

    def reset(self):
        self.make_schedule()
        self.command_handlers = []
        for klass in self.HANDLER_CLASSES:
            self.command_handlers.append(klass(self.gui))
        self.gls_set = False

    def make_schedule(self):
        self.command_schedule = []
        for command, repeat in self.COMMANDS:
            self.command_schedule.append([command, repeat, 0])

    def next_command(self):
        for i, (command, repeat, next_time) in enumerate(self.command_schedule):
            if time.monotonic() > next_time:
                self.command_schedule[i][2] = time.monotonic() + repeat
                return command

    def supports_gls(self, state):
        if not self.gls_set and state is True:
            self.gls_set = True
            self.command_schedule.insert(1, ['get_logger_settings', 5, 0])

    def notify_handlers(self, query_results):
        for handler in self.command_handlers:
            handler.notify(query_results)


class Update:
    def __init__(self, gui):
        """
        When subclassing, the applicable_commands method must return a list
        of commands that should be accepted by update
        """
        self.gui = gui

    def applicable_commands(self):
        raise NotImplementedError

    def update(self, query_results):
        raise NotImplementedError

    def notify(self, query_results):
        command, data = query_results
        if command in self.applicable_commands():
            self.update(query_results)


class SimpleUpdate(Update):
    def __init__(self, gui):
        super().__init__(gui)
        self.widget = None

    def applicable_commands(self):
        return ['GTM', 'GFV']

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

    def applicable_commands(self):
        return ['get_logger_settings', 'get_sensor_readings']

    def update(self, query_results):
        command, data = query_results
        if command == 'get_logger_settings':
            self.logger_settings = query_results[1]
            self.update_settings_description()
        elif command == 'get_sensor_readings':
            self.redraw_table(query_results[1])

    def update_settings_description(self):
        if self.logger_settings:
            setup_file = SetupFile(self.logger_settings)
            description = DescriptionGenerator(setup_file).sample_description()
        else:
            description = 'No MAT.cfg settings file found on device memory card.'
        self.gui.labelLoggerSettings.setText(description)

    def redraw_table(self, data):
        for index, sensor in enumerate(SENSORS.keys()):
            self._set_item_text(index, 1, self.enabled_str(sensor))
            self._set_item_text(index, 2, self.value_string(sensor, data))

    def _set_item_text(self, row, col, value):
        item = QtWidgets.QTableWidgetItem(value)
        if col == 1:
            alignment = Qt.AlignCenter
        else:
            alignment = Qt.AlignRight
        item.setTextAlignment(alignment)
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
    def applicable_commands(self):
        return ['GTM']

    def update(self, query_results):
        super().update(query_results)
        command, data = query_results
        try:
            logger_time = datetime.strptime(data, '%Y/%m/%d %H:%M:%S')
        except ValueError:
            return
        computer_time = datetime.now()
        diff = abs(logger_time - computer_time).total_seconds()
        if diff > 60:
            style = 'background-color: rgb(255, 255, 0);'
        else:
            style = ''
        self.widget.setStyleSheet(style)


class SerialNumberUpdate(Update):
    def applicable_commands(self):
        return ['GSN']

    def update(self, query_results):
        command, data = query_results
        self.gui.label_serial.setText('Serial Number: {}'.format(data))
        self.gui.statusbar_serial_number.setText(
            '  Connected to {}  '.format(data))


class FileSizeUpdate(Update):
    def applicable_commands(self):
        return ['FSZ', 'CTS', 'CFS']

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

    def applicable_commands(self):
        return ['STS']

    def update(self, query_results):
        command, data = query_results
        status_code = int(data, 16)
        self._show_running(self._running(status_code))
        self.gui.label_status.setText(self.description(status_code))

    def _running(self, status_code):
        return False if status_code & 1 else True

    def description(self, status_code):
        running = 'running' if self._running(status_code) else 'stopped'
        status_str = 'Device {}'.format(running)
        if status_code & 2:
            status_str += ' - {}'.format('Delayed start')
        # for value, string in ERROR_CODES:
        #     if status_code & value:
        #         status_str += ' - {}'.format(string)
        return status_str

    def _show_running(self, state):
        self.gui.pushButton_start.setEnabled(not state)
        self.gui.pushButton_stop.setEnabled(state)
        self.gui.pushButton_sync_clock.setEnabled(not state)
        icon = self.rabbit_icon if state is True else self.stopped_icon
        self.gui.pushButton_status.setIcon(icon)
        self.gui.pushButton_status.setIconSize(QtCore.QSize(36, 36))
        status = '  Device Running  ' if state else '  Stopped  '
        self.gui.statusbar_logging_status.setText(status)
        status = {False: 'Real-Time Data', True: 'Most-Recent Data'}
        self.gui.label_table.setText(status[state])


class DeploymentUpdate(Update):
    def applicable_commands(self):
        return ['logger_info']

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


class StuckSensor(Update):
    def __init__(self, gui):
        super().__init__(gui)
        self.warned = False
        self.last_data = None

    def applicable_commands(self):
        return ['get_sensor_readings']

    def check_zeros(self, data):
        if not self.last_data or self.warned:
            return

        mag_keys = ['mx_raw', 'my_raw', 'mz_raw']
        if all([data[x] == 0 for x in mag_keys]) \
                and all([self.last_data[x] == 0 for x in mag_keys]):
            self.warned = True
            reply = QtWidgets.QMessageBox.question(
                self.gui.frame,
                'Magnetometer error',
                'The magnetometer on your device is not responding. '
                'Would you like to reset your device.')
            if reply == QtWidgets.QMessageBox.Yes:
                self.gui.queue.put('RST')

    def update(self, query_results):
        command, data = query_results
        self.check_zeros(data)
        self.last_data = data
