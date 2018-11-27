from yaml import load
from gui.sensor_formats import hundredths_format, thousands_format, int_format
from re import search


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
        self.label_status = gui.label_status
        self.button_start = gui.pushButton_start
        self.button_stop = gui.pushButton_stop
        self.button_sync = gui.pushButton_sync_clock
        self.format_str = 'Device is {}'

    def update(self, data):
        status_code = int(data)
        state = False if status_code & 1 else True
        self._show_running(state)

    def _show_running(self, state):
        status_str = 'running' if state is True else 'not running'
        self.label_status.setText(self.format_str.format(status_str))
        self.button_start.setEnabled(not state)
        self.button_stop.setEnabled(state)
        self.button_sync.setEnabled(not state)
