

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
