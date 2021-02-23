from PyQt5.QtWidgets import QMessageBox
from pathlib import Path
import sys


def application_directory():
    try:
        directory = Path(sys._MEIPASS)
    except AttributeError:
        directory = Path(__file__).parent
    return directory


def show_error(widgets, state):
    widgets = make_list(widgets)
    style = 'background-color: rgb(255, 255, 0);' if state else ''
    for widget in widgets:
        widget.setStyleSheet(style)


def set_enabled(widgets, state):
    widgets = make_list(widgets)
    for w in widgets:
        w.setEnabled(state)


def make_list(widget):
    if type(widget) is not list:
        widget = [widget]
    return widget


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def sec_to_string(seconds):
    if seconds == 1:
        return '1 second'
    elif seconds == 60:
        return '1 minute'
    elif seconds < 60:
        return f'{seconds:0.0f} seconds'
    elif seconds < 3600:
        return f'{seconds/60:0.0f} minutes'
    elif seconds == 3600:
        return '1 hour'
    else:
        return f'{seconds/3600:0.0f} hours'


class SharedValue:
    """
    A class to allow multiple objects to share a value. Registered observers
    will be updated when the value changes.
    """
    def __init__(self, value):
        self._value = value
        self._observers = {}

    def register(self, name, widget, mode, fcn):
        self._observers[name] = {'widget': widget, 'mode': mode, 'fcn': fcn}

    def unregister(self, name):
        del self._observers[name]

    def n_observers(self):
        return len(self.active_observers())

    def active_observers(self):
        # return the dictionary for "active" observers
        return {x: self._observers[x] for x in self._observers
                if self._observers[x]['mode'] == 'active'}

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for observer in self._observers:
            self._observers[observer]['fcn']()
