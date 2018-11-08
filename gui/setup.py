from gui.setup_ui import Ui_Frame
from setup_file.setup_file import SetupFile
from setup_file.setup_file import (
    INTERVALS,
    INTERVAL_STRING,
    BURST_FREQUENCY,
    ORIENTATION_BURST_COUNT,
    ORIENTATION_BURST_RATE,
    TEMPERATURE_INTERVAL,
    ORIENTATION_INTERVAL,
    ACCELEROMETER_ENABLED,
    MAGNETOMETER_ENABLED,
    TEMPERATURE_ENABLED,
    LED_ENABLED,
    FILE_NAME,
    START_TIME,
    END_TIME
)
from collections import namedtuple
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QFileDialog, QMessageBox


sensor_map = namedtuple('sensor_map', ['widget', 'value', 'change_fcn'])


class SetupFrame(Ui_Frame):
    def __init__(self):
        self.setup_file = SetupFile()
        self.setup_file.set_observer(self.test)
        self.interval_mapping = None
        self.sensor_mapping = None

    def test(self, key, value):
        self.redraw()

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.lineEdit_file_name.setMaxLength(11)
        self.populate_combo_boxes()
        self.setup_mapping()
        self.connect_signals(True)
        self.redraw()

    def connect_signals(self, state):
        signals = [(self.lineEdit_file_name.textChanged,
                    self.filename_changed),
                   (self.comboBox_orient_interval.currentIndexChanged,
                    lambda: self.interval_changed('orientation')),
                   (self.comboBox_temp_interval.currentIndexChanged,
                    lambda: self.interval_changed('temperature')),
                   (self.checkBox_temperature.stateChanged,
                    lambda: self.sensor_enabled_slot('temperature')),
                   (self.checkBox_magnetometer.stateChanged,
                    lambda: self.sensor_enabled_slot('magnetometer')),
                   (self.checkBox_accelerometer.stateChanged,
                    lambda: self.sensor_enabled_slot('accelerometer')),
                   (self.checkBox_led.stateChanged,
                    lambda: self.sensor_enabled_slot('led')),
                   (self.lineEdit_burst_duration.textChanged,
                    self.duration_changed),
                   (self.checkBox_continuous.stateChanged,
                    self.continuous_changed),
                   (self.comboBox_orient_burst_rate.currentIndexChanged,
                    self.burst_rate_changed),
                   (self.comboBox_start_time.currentIndexChanged,
                    self.redraw_date_boxes),
                   (self.comboBox_end_time.currentIndexChanged,
                    self.redraw_date_boxes),
                   (self.dateTimeEdit_start_time.dateTimeChanged,
                    lambda: self.date_time_changed('start_time')),
                   (self.dateTimeEdit_end_time.dateTimeChanged,
                    lambda: self.date_time_changed('end_time')),
                   (self.pushButton_save.clicked,
                    self.save_file)]

        for signal, fcn in signals:
            if state is True:
                signal.connect(fcn)
            else:
                signal.disconnect()

    def setup_mapping(self):
        self.interval_mapping = {
            'temperature':
                sensor_map(
                    self.comboBox_temp_interval,
                    lambda: self.setup_file.value(TEMPERATURE_INTERVAL),
                    self.setup_file.set_temperature_interval),
            'orientation':
                sensor_map(
                    self.comboBox_orient_interval,
                    lambda: self.setup_file.value(ORIENTATION_INTERVAL),
                    self.setup_file.set_orient_interval)
        }

        self.sensor_mapping = {
            'temperature':
                sensor_map(
                    self.checkBox_temperature,
                    lambda: self.setup_file.value(TEMPERATURE_ENABLED),
                    self.setup_file.set_temperature_enabled),
            'accelerometer':
                sensor_map(
                    self.checkBox_accelerometer,
                    lambda: self.setup_file.value(ACCELEROMETER_ENABLED),
                    self.setup_file.set_accelerometer_enabled),
            'magnetometer':
                sensor_map(
                    self.checkBox_magnetometer,
                    lambda: self.setup_file.value(MAGNETOMETER_ENABLED),
                    self.setup_file.set_magnetometer_enabled),
            'led':
                sensor_map(
                    self.checkBox_led,
                    lambda: self.setup_file.value(LED_ENABLED),
                    self.setup_file.set_led_enabled),
        }

    def populate_combo_boxes(self):
        self.comboBox_temp_interval.addItems(INTERVAL_STRING)
        self.comboBox_orient_interval.addItems(INTERVAL_STRING)
        burst_list = [str(x) + ' Hz' for x in BURST_FREQUENCY]
        burst_list = ['No Burst'] + burst_list
        self.comboBox_orient_burst_rate.addItems(burst_list)

    def redraw(self):
        self.connect_signals(False)
        file_name = self.setup_file.value(FILE_NAME)[:-4]
        self.lineEdit_file_name.setText(file_name)
        self.redraw_temperature()
        self.redraw_orient_group()
        self.redraw_combo_boxes()
        self.redraw_check_boxes()
        self.redraw_date_boxes()
        self.redraw_burst()
        self.connect_signals(True)

    def redraw_temperature(self):
        state = True if self.setup_file.value(TEMPERATURE_ENABLED) else False
        self.comboBox_temp_interval.setEnabled(state)

    def redraw_orient_group(self):
        orient_group = [self.comboBox_orient_interval,
                        self.comboBox_orient_burst_rate,
                        self.lineEdit_burst_duration,
                        self.checkBox_continuous]
        state = True if self.setup_file.orient_enabled() else False
        self._set_enabled(orient_group, state)

    def redraw_combo_boxes(self):
        for sensor in ['temperature', 'orientation']:
            intervals = self.setup_file.available_intervals(sensor)
            for i, val in enumerate(intervals):
                widget = self.interval_mapping[sensor].widget
                widget.model().item(i).setEnabled(val)
            interval = self.interval_mapping[sensor].value()
            index = list(INTERVALS).index(interval)
            self.interval_mapping[sensor].widget.setCurrentIndex(index)

    def redraw_check_boxes(self):
        for sensor in self.sensor_mapping.values():
            state = sensor.value()
            sensor.widget.setChecked(state)

    def redraw_date_boxes(self):
        mapping = [(self.comboBox_start_time,
                    self.dateTimeEdit_start_time,
                    START_TIME),
                   (self.comboBox_end_time,
                    self.dateTimeEdit_end_time,
                    END_TIME)]
        for combo_box, date_time, occasion in mapping:
            time = self.setup_file.value(occasion)
            time = QDateTime.fromString(time, 'yyyy-MM-dd HH:mm:ss')
            date_time.setDateTime(time)
            state = True if combo_box.currentIndex() == 1 else False
            date_time.setEnabled(state)

    def redraw_burst(self):
        is_orient = self.setup_file.orient_enabled()
        state = True if is_orient else False

        count = self.setup_file.value(ORIENTATION_BURST_COUNT)
        rate = self.setup_file.value(ORIENTATION_BURST_RATE)
        seconds = count // rate
        index = list(BURST_FREQUENCY).index(rate)
        self.comboBox_orient_burst_rate.setCurrentIndex(index + 1)
        self.lineEdit_burst_duration.setText(str(seconds))
        self.lineEdit_burst_duration.setEnabled(state)
        self.checkBox_continuous.setEnabled(state)

        if is_orient and self.setup_file.value(ORIENTATION_BURST_COUNT) == 1:
            self.comboBox_orient_burst_rate.setCurrentIndex(0)
            self.lineEdit_burst_duration.setEnabled(False)
            self.checkBox_continuous.setEnabled(False)

    def filename_changed(self):
        string = self.lineEdit_file_name.text()
        try:
            self.setup_file.set_filename(string + '.lid')
            self.show_error(self.lineEdit_file_name, False)
        except ValueError:
            self.show_error(self.lineEdit_file_name, True)

    def burst_rate_changed(self):
        index = self.comboBox_orient_burst_rate.currentIndex()
        if index == 0:
            self.checkBox_continuous.setChecked(False)
            self.setup_file.set_orient_burst_count(1)
            self.setup_file.set_orient_burst_rate(2)
        else:
            burst_rate = BURST_FREQUENCY[index-1]
            self.setup_file.set_orient_burst_rate(burst_rate)
            self.setup_file.set_orient_burst_count(burst_rate)
            self.duration_changed()

    def date_time_changed(self, occasion):
        mapping = {'start_time':
                   (self.dateTimeEdit_start_time, START_TIME),
                   'end_time':
                   (self.dateTimeEdit_end_time, END_TIME)}
        widget, value = mapping[occasion]
        date_time = widget.dateTime()
        date_time_string = date_time.toString('yyyy-MM-dd HH:mm:ss')
        try:
            self.setup_file.set_time(value, date_time_string)
            # TODO Show error dialog
        except ValueError:
            pass

    def interval_changed(self, sensor):
        index = self.interval_mapping[sensor].widget.currentIndex()
        self.interval_mapping[sensor].change_fcn(INTERVALS[index])
        self.duration_changed()

    def sensor_enabled_slot(self, sensor):
        state = self.sensor_mapping[sensor].widget.isChecked()
        self.sensor_mapping[sensor].change_fcn(state)

    def duration_changed(self):
        seconds = self.lineEdit_burst_duration.text()
        rate = self.setup_file.value(ORIENTATION_BURST_RATE)
        count = self.setup_file.value(ORIENTATION_BURST_COUNT)
        try:
            self.setup_file.set_orient_burst_count(int(seconds)*rate)
            self.show_error(self.lineEdit_burst_duration, False)
        except ValueError:
            self.show_error(self.lineEdit_burst_duration, True)

    def show_error(self, widgets, error):
        widgets = self._make_list(widgets)
        style = 'background-color: rgb(255, 255, 0);' if error else ''
        for widget in widgets:
            widget.setStyleSheet(style)

    def continuous_changed(self):
        widgets = [self.comboBox_orient_interval,
                   self.lineEdit_burst_duration]
        if self.checkBox_continuous.isChecked():
            self.comboBox_orient_interval.setCurrentIndex(0)
            self.lineEdit_burst_duration.setText('1')
            self._set_enabled(widgets, False)
        else:
            self._set_enabled(widgets, True)

    def _set_enabled(self, widgets, state):
        widgets = self._make_list(widgets)
        for w in widgets:
            w.setEnabled(state)

    def _make_list(self, widget):
        if type(widget) is not list:
            widget = [widget]
        return widget

    def save_file(self):
        path = QFileDialog.getExistingDirectory(self.frame, 'Save File')
        if not path:
            return
        self.setup_file.write_file(path)
        QMessageBox.information(self.frame,
                                'File Saved',
                                'File saved successfully')
