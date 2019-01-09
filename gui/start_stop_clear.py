from PyQt5.QtWidgets import QTableWidgetItem


DEFAULTS = [
    ('label_status', 'Not connected'),
    ('label_connection', 'Not connected'),
    ('label_file_size', 'File size: --'),
    ('label_sd_free_space', 'SD card free space: --'),
    ('label_sd_total_space', ''),
    ('label_logger_time', 'Logger Time: --'),
    ('label_serial', 'Serial Number: --'),
    ('label_firmware', 'Firmware Version: --'),
    ('label_model', 'Model Number: --'),
    ('label_firmware', 'Firmware Version: --'),
    ('label_deployment', 'Deployment Number: --')
]


def clear_gui(gui):
    _clear_table(gui)
    for widget_name, string in DEFAULTS:
        widget = getattr(gui, widget_name)
        widget.setText(string)
        widget.setStyleSheet('')


def _clear_table(gui):
    for row in range(8):
        for col in range(1, 3):
            item = QTableWidgetItem('--')
            gui.tableWidget.setItem(row, col, item)
