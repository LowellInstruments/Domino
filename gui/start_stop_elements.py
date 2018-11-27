from yaml import load
from gui.sensor_formats import hundredths_format, thousands_format, int_format
from re import search
from PyQt5 import QtGui, QtCore


def build_commands(path, gui):
    commands = {}
    with open(path) as fid:
        command_params = load(fid)
    for command, params in command_params.items():
        this_command = {}
        this_command['interval'] = params['interval']
        this_command['next_update'] = 0
        klass = _class_from_string(params['update_fcn'])
        this_command['update'] = klass(gui, *params['init'])
        commands[command] = this_command
    return commands


def _class_from_string(klass):
    return globals()[klass]


class SimpleTextElement:
    def __init__(self, gui, widget, format_str):
        self.widget = getattr(gui, widget)
        self.format_str = format_str

    def update(self, data):
        self.widget.setText(self.format_str.format(data))


class FileSize(SimpleTextElement):
    def update(self, data):
        numeric_data = search('[0-9]+', data).group()
        numeric_data = float(numeric_data) / 1024**2
        self.widget.setText(self.format_str.format(numeric_data))


class Status:
    def __init__(self, gui):
        self.gui = gui
        self.rabbit_icon = QtGui.QIcon()
        self.rabbit_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/icons8-running-rabbit-48.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopped_icon = QtGui.QIcon()
        self.stopped_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/icons8-private-48.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def update(self, data):
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
