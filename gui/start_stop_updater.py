from gui.sensor_formats import hundredths_format, thousands_format, int_format
from re import search
from PyQt5 import QtGui, QtCore, QtWidgets
from numpy import ndarray
from collections import OrderedDict


# [Command, repeat interval, class]
COMMANDS = [
    ['GTM', 1, 'SimpleUpdate'],
    ['STS', 1, 'StatusUpdate'],
    ['get_sensor_readings', 1, 'SensorUpdate'],
    ['logger_info', 99999999, 'DeploymentUpdate'],
    ['FSZ', 5, 'FileSizeUpdate'],
    ['CTS', 10, 'FileSizeUpdate'],
    ['CFS', 10, 'FileSizeUpdate'],
    ['GSN', 10, 'SimpleUpdate'],
    ['GFV', 10, 'SimpleUpdate']
]

FILE_SIZE = {
    'FSZ': ('File size {:0.2f} MB', 'label_file_size'),
    'CTS': (' of {:0.2f} GB available', 'label_sd_total_space'),
    'CFS': ('SD card free space: {:0.2f}','label_sd_free_space')
}

SIMPLE_FIELD = {
    'GTM': ('Logger time: {}', 'label_logger_time'),
    'GSN': ('Serial Number: {}', 'label_serial'),
    'GFV': ('Firmware version: {}', 'label_firmware'),
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


class Commands:
    def __init__(self, gui):
        self.gui = gui
        self.command_schedule = []
        self.command_handlers = {}
        self.make_commands()

    def make_commands(self):
        self.command_handlers = {}
        for command, _, klass in COMMANDS:
            handler_obj = globals()[klass]
            self.command_handlers[command] = handler_obj(self.gui)

    def get_schedule(self):
        command_schedule = []
        for command, repeat, _ in COMMANDS:
            command_schedule.append([command, repeat, 0])
        return command_schedule

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
    def update(self, query_results):
        command, data = query_results
        format_, widget_name = SIMPLE_FIELD[command]
        widget = getattr(self.gui, widget_name)
        widget.setText(format_.format(data))


class FileSizeUpdate(Update):
    def update(self, query_results):
        command, data = query_results
        format_, widget_name = FILE_SIZE[command]
        widget = getattr(self.gui, widget_name)
        numeric_data = search('[0-9]+', data).group()
        numeric_data = float(numeric_data) / 1024**2
        widget.setText(format_.format(numeric_data))


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
        status_code = int(data)
        self._show_running(False if status_code & 1 else True)

    def _show_running(self, state):
        status_str = 'running' if state is True else 'not running'
        self.gui.label_status.setText('Device is {}'.format(status_str))
        self.gui.pushButton_start.setEnabled(not state)
        self.gui.pushButton_stop.setEnabled(state)
        self.gui.pushButton_sync_clock.setEnabled(not state)
        icon = self.rabbit_icon if state is True else self.stopped_icon
        self.gui.pushButton_icon.setIcon(icon)
        self.gui.pushButton_icon.setIconSize(QtCore.QSize(36, 36))


class SensorUpdate(Update):
    def update(self, query_results):
        command, data = query_results
        for index, sensor in enumerate(SENSORS.keys()):
            self._set_item_text(index, 1, self.enabled_string(sensor, data))
            self._set_item_text(index, 2, self.value_string(sensor, data))

    def _set_item_text(self, row, col, value):
        item = QtWidgets.QTableWidgetItem(value)
        self.gui.tableWidget.setItem(row, col, item)

    def enabled_string(self, sensor, readings):
        if readings and sensor in readings:
            return 'Yes'
        return 'No'

    def value_string(self, sensor, readings):
        if not readings:
            return ''
        reading = readings.get(sensor, '')
        if isinstance(reading, ndarray):
            return self._format_sensor_value(sensor, reading[0])
        return self._format_sensor_value(sensor, reading)

    def _format_sensor_value(self, sensor, value):
        return SENSORS[sensor](value)


class DeploymentUpdate(Update):
    def update(self, query_results):
        command, data = query_results
        if 'DP' in data:
            deployment_str = 'Deployment Number: {}'.format(data['DP'])
            self.gui.label_deployment.setText(deployment_str)
        if 'MA' in data:
            model_str = 'Model Number: {}'.format(data['MA'])
            self.gui.label_model.setText(model_str)
