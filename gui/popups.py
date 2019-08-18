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
