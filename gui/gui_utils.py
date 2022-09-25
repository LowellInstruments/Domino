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


def hhmmss(seconds):
    hours = seconds // 3600
    seconds = round(seconds % 3600, 1)
    minutes = seconds // 60
    seconds = round(seconds % 60, 1)
    output = ''

    if hours > 1:
        output += f'{int(hours)} hours, '
    elif hours == 1:
        output += f'{int(hours)} hour, '

    if minutes > 1:
        output += f'{int(minutes)} minutes, '
    elif minutes == 1:
        output += f'{int(minutes)} minute'

    if seconds == 0 or seconds > 1:
        output += f'{seconds} seconds'
    elif seconds == 1:
        output += f'{seconds} second'

    return output