from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAbstractButton
import gui


# TODO Move all the text, dialog types, etc into a yaml file


def major_interval_warning():
    message = 'The current logging parameters exceed the logger ' \
              'buffer size. This can usually be corrected by ' \
              'reducing the temperature recording interval. The ' \
              'configuration file was not generated. See the user ' \
              'guide for more details.'
    QMessageBox.information(gui.mw, 'Invalid settings', message)


def end_time_in_past():
    message = 'The specified end time is in the past. Please select ' \
              'a time in the future.'
    QMessageBox.warning(gui.mw, 'End time in past', message)


def temp_compensated_sensor_warning():
    text = 'The magnetometer is a temperature compensated sensor and ' \
           'it may not perform well if temperature logging is disabled. ' \
           'It is recommended that you enable temperature logging. Would ' \
           'you like to continue anyway?'
    answer = QMessageBox.warning(
        gui.mw,
        'Temperature compensated sensor',
        text,
        QMessageBox.Yes | QMessageBox.No)
    if answer == QMessageBox.Yes:
        return True
    return False


def no_channels_warning():
    text = 'At lease one channel must be enabled.'
    QMessageBox.warning(gui.mw, 'Invalid settings', text)


# Converter window dialogs

def open_lid_file(directory):
    file_paths = QFileDialog.getOpenFileNames(
        gui.mw,
        'Open Lowell Instruments Data File',
        directory,
        'Data Files (*.lid *.lis)')
    return file_paths


def about_declination():
    text = 'Magnetic declination is the angle between magnetic north and ' \
           'true north. This angle varies depending on position on the ' \
           'Earth\'s surface.' \
           '<br><br>In order for current and compass data to ' \
           'be converted to geographic coordinates, you must enter the ' \
           'declination at your deployment site, otherwise the heading and ' \
           'velocity components will be relative to magnetic north.' \
           '<br><br>Declination can be found using a calculator such as ' \
           '<a href="http://ngdc.noaa.gov/geomag-web">NOAA\'s Declination ' \
           'Calculator</a><br /><br />' \
           'Values must be in the range [-180, 180]<br /> East is positive.'

    message = QMessageBox(gui.mw)
    message.setTextFormat(1)
    message.setIcon(QMessageBox.Information)
    message.setWindowTitle('About Declination')
    message.setText(text)
    message.exec_()


def ask_overwrite(filename):
    buttons_actions = [
        (QMessageBox.Yes, 'once'),
        (QMessageBox.YesToAll, 'yes_to_all'),
        (QMessageBox.No, 'no'),
        (QMessageBox.NoToAll, 'no_to_all')
    ]
    button_val = 0
    for button, _ in buttons_actions:
        button_val = button_val | button
    message = 'Converting {} will overwrite files in the output ' \
              'directory. Would you like to continue?'.format(filename)
    answer = QMessageBox.question(gui.mw, 'Overwrite file?',
                                  message, button_val)
    for button, action in buttons_actions:
        if answer == button:
            return action


def prompt_mark_unconverted():
    text = 'All items in the queue have previously been converted. ' \
           'Would you like to mark them unconverted?'
    answer = QMessageBox.warning(
                gui.mw,
                'All items converted',
                text,
                QMessageBox.Yes | QMessageBox.Cancel)
    if answer == QMessageBox.Yes:
        return True


def confirm_custom_cal():
    text = 'You currently have a custom calibration file selected. ' \
           'This calibration will be applied to all the files in the ' \
           'conversion queue. Are you sure you want to apply it?'
    answer = QMessageBox.warning(
                gui.mw,
                'Confirm Custom Calibration',
                text,
                QMessageBox.Yes | QMessageBox.Cancel)
    return answer == QMessageBox.Yes


def confirm_quit():
    reply = QMessageBox.question(
            gui.mw,
            'Confirm Quit',
            'There are unconverted files in the queue. '
            'Are you sure you want to quit?')
    return reply == QMessageBox.Yes

def conversion_error(model):
    error_map = {
        'error_failed':
            'File structure error',
        'error_sensor_missing':
            'The output type selected depends on sensors that were disabled'
    }
    UNKNOWN = 'An unknown error occurred'
    message = 'There were errors during the file conversion'
    detailed_text = ''
    for file in model:
        if file.status.startswith('error'):
            error = error_map.get(file.status, UNKNOWN)
            error_str = '{}: {}\n'.format(file.filename, error)
            detailed_text += error_str
    msg_box = QMessageBox(gui.mw)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle('Conversion Error')
    msg_box.setText(message)
    msg_box.setDetailedText(detailed_text)
    msg_box.exec_()


def ask_remove_error_files():
    dialog = RemoveDiscardDialog(gui.mw)
    dialog.exec_()
    return dialog.clickedButton().text()


def header_error(filename, header_error):
    good, ideal = header_error
    percent = good / ideal * 100
    message = 'The file "{}" encountered corruption at {:.0f}%. ' \
              'The good portion of the file will be ' \
              'converted.'.format(filename, percent)
    QMessageBox.warning(gui.mw, 'File Corruption', message)


class RemoveDiscardDialog(QMessageBox):
    def __init__(self, *args):
        super().__init__(*args)
        text = 'Some files in the queue previously failed to convert. ' \
               'Would you like to remove them from the queue or ' \
               'retry conversion?'
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle('Error Files')
        self.setText(text)
        self.addButton('Remove', QMessageBox.AcceptRole)
        self.addButton('Retry', QMessageBox.AcceptRole)


def error_message(title, message):
    QMessageBox.warning(gui.mw, title, message, QMessageBox.Ok)
