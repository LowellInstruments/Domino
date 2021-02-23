


def disable_scroll_wheel(window):
    widgets = [
        window.comboBox_temp_interval,
        window.comboBox_orient_interval,
        window.comboBox_orient_burst_rate,
        window.comboBox_pressure_interval,
        window.comboBox_pressure_burst_rate,
        window.comboBox_start_time,
        window.dateTimeEdit_start_time,
        window.comboBox_end_time,
        window.dateTimeEdit_end_time
    ]
    for widget in widgets:
        widget.wheelEvent = lambda event: event.ignore()


def lock_setup_controls(window, state):
    widgets = [
        window.frame_temperature,
        window.frame_orient,
        window.frame_pressure
    ]
    for widget in widgets:
        widget.setEnabled(not state)


def connect_signals(window):
    # user only signals (not triggered by programatic changes)
    # qlineedit -- textEdited
    # qcombobox -- activated
    window.lineEdit_file_name.editingFinished.connect(
        window.filename_changed)
    window.comboBox_orient_interval.activated.connect(
        lambda: window.interval_changed('orientation'))
    window.comboBox_temp_interval.activated.connect(
        lambda: window.interval_changed('temperature'))
    window.checkBox_temperature.stateChanged.connect(
        lambda: window.sensor_enabled_slot('temperature'))
    window.checkBox_magnetometer.stateChanged.connect(
        lambda: window.sensor_enabled_slot('magnetometer'))
    window.checkBox_accelerometer.stateChanged.connect(
        lambda: window.sensor_enabled_slot('accelerometer'))
    window.checkBox_led.stateChanged.connect(
        lambda: window.sensor_enabled_slot('led'))
    window.lineEdit_burst_duration.editingFinished.connect(
        window.duration_changed)
    window.checkBox_continuous.stateChanged.connect(
        window.continuous_changed)
    window.comboBox_orient_burst_rate.activated.connect(
        window.burst_rate_changed)
    window.comboBox_start_time.activated.connect(
        lambda: window.date_time_combobox_changed('start_time'))
    window.comboBox_end_time.activated.connect(
        lambda: window.date_time_combobox_changed('end_time'))
    window.dateTimeEdit_start_time.dateTimeChanged.connect(
        lambda: window.date_time_changed('start_time'))
    window.dateTimeEdit_end_time.dateTimeChanged.connect(
        lambda: window.date_time_changed('end_time'))
    window.pushButton_save.clicked.connect(
        window.save_file)
    window.treeWidget.itemClicked.connect(window.tree_click)
