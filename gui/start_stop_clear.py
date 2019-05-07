from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui


DEFAULTS = [
    ('label_connected', 'Not connected'),
    ('label_status', 'Connect for Status'),
    ('label_file_size', 'File size: --'),
    ('label_sd_free_space', 'SD card free space: --'),
    ('label_sd_total_space', ''),
    ('label_logger_time', 'Logger Time: --'),
    ('label_serial', 'Serial Number: --'),
    ('label_firmware', 'Firmware Version: --'),
    ('label_model', 'Model Number: --'),
    ('label_firmware', 'Firmware Version: --'),
    ('label_deployment', 'Deployment Number: --'),
    ('statusbar_logging_status', '  --  '),
    ('statusbar_serial_number','  Not Connected  ')
]


def clear_gui(gui):
    _clear_table(gui)
    unknown_icon = QtGui.QIcon()
    unknown_icon.addPixmap(
        QtGui.QPixmap(':/icons/icons/unknown-status.png'),
        QtGui.QIcon.Normal, QtGui.QIcon.Off)
    gui.pushButton_status.setIcon(unknown_icon)
    for widget_name, string in DEFAULTS:
        widget = getattr(gui, widget_name)
        widget.setText(string)
        widget.setStyleSheet('')


def _clear_table(gui):
    for row in range(8):
        for col in range(1, 3):
            item = QTableWidgetItem('--')
            gui.tableWidget.setItem(row, col, item)
