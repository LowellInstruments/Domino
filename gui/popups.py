from PyQt5.QtWidgets import QFileDialog, QMessageBox


def major_interval_warning(parent):
    message = 'The current logging parameters exceed the logger ' \
              'buffer size. This can usually be corrected by ' \
              'reducing the temperature recording interval. The ' \
              'configuration file was not generated. See the user ' \
              'guide for more details.'
    QMessageBox.information(parent, 'Invalid settings', message)


def end_time_in_past(parent):
    message = 'The specified end time is in the past. Please select ' \
              'a time in the future.'
    QMessageBox.warning(parent, 'End time in past', message)


def file_conversion_error(parent):
    message = 'One or more files could not be converted.'
    QMessageBox.warning(parent, 'Conversion Error', message)


def temp_compensated_sensor_warning(parent):
    text = 'The magnetometer is a temperature compensated sensor and ' \
           'it may not perform well if temperature logging is disabled. ' \
           'It is recommended that you enable temperature logging. Would ' \
           'you like to continue anyway?'
    answer = QMessageBox.warning(
        parent,
        'Temperature compensated sensor',
        text,
        QMessageBox.Yes | QMessageBox.No)
    if answer == QMessageBox.Yes:
        return True
    return False
