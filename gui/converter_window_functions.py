


def disable_scroll_wheel(window):
    widgets = [
        window.comboBox_temp_interval,
        window.comboBox_orient_interval,
        window.comboBox_pressure_interval,
        window.comboBox_pressure_burst_rate,
        window.comboBox_start_time,
        window.dateTimeEdit_start_time,
        window.comboBox_end_time,
        window.dateTimeEdit_end_time
    ]
    for widget in widgets:
        widget.wheelEvent = lambda event: event.ignore()
