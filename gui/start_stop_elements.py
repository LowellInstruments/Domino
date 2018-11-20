from yaml import load
from gui.sensor_formats import hundredths_format, thousands_format, int_format


def build_commands(path, gui):
    commands = {}
    with open(path) as fid:
        command_params = load(fid)
    for command, params in command_params.items():
        commands[command] = {}
        commands[command]['interval'] = params['interval']
        commands[command]['next_update'] = 0
        klass = _class_from_string(params['update_fcn'])
        widget = getattr(gui, params['init'][0])
        params = params['init'][1:]
        commands[command]['update'] = klass(widget, *params)
    return commands


def _class_from_string(klass):
    return globals()[klass]


class SimpleTextElement:
    def __init__(self, widget, format_str):
        self.widget = widget
        self.format_str = format_str

    def update(self, data):
        self.widget.setText(self.format_str.format(data))


class FileSize(SimpleTextElement):
    def update(self, data):
        numeric_data = float(data) / 1024**2
        self.widget.setText(self.format_str.format(numeric_data))
