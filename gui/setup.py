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


sensor_map = namedtuple('sensor_map', ['widget', 'tag'])


class SetupFrame(Ui_Frame):
    def __init__(self):
        self.setup_file = SetupFile()
        self.setup_file.set_observer(self.test)
        self.interval_mapping = None
        self.sensor_mapping = None
        self.date_mapping = None

    def test(self, key, value):
        self.redraw()

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.lineEdit_file_name.setMaxLength(11)
        self.populate_combo_boxes()
        self.setup_mapping()
        self.set_retain_size([self.dateTimeEdit_start_time,
                              self.dateTimeEdit_end_time])
        self.connect_signals(True)
        self.redraw()

    def set_retain_size(self, widgets):
        for widget in widgets:
            date_time_size_policy = widget.sizePolicy()
            date_time_size_policy.setRetainSizeWhenHidden(True)
            widget.setSizePolicy(date_time_size_policy)

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
                    lambda: self.date_time_combobox_changed('start_time')),
                   (self.comboBox_end_time.currentIndexChanged,
                    lambda: self.date_time_combobox_changed('end_time')),
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
                sensor_map(self.comboBox_temp_interval, TEMPERATURE_INTERVAL),
            'orientation':
                sensor_map(self.comboBox_orient_interval, ORIENTATION_INTERVAL)
        }

        self.sensor_mapping = {
            'temperature':
                sensor_map(self.checkBox_temperature, TEMPERATURE_ENABLED),
            'accelerometer':
                sensor_map(self.checkBox_accelerometer, ACCELEROMETER_ENABLED),
            'magnetometer':
                sensor_map(self.checkBox_magnetometer, MAGNETOMETER_ENABLED),
            'led':
                sensor_map(self.checkBox_led, LED_ENABLED)}

        self.date_mapping = {
            'start_time':
                sensor_map(self.dateTimeEdit_start_time, START_TIME),
            'end_time':
                sensor_map(self.dateTimeEdit_end_time, END_TIME)}

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
        self.redraw_interval_combo_boxes()
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

    def redraw_interval_combo_boxes(self):
        for sensor in ['temperature', 'orientation']:
            tag = self.interval_mapping[sensor].tag
            intervals = self.setup_file.available_intervals(tag)
            for i, val in enumerate(intervals):
                widget = self.interval_mapping[sensor].widget
                widget.model().item(i).setEnabled(val)
            interval = self.setup_file.value(tag)
            index = list(INTERVALS).index(interval)
            self.interval_mapping[sensor].widget.setCurrentIndex(index)

    def redraw_check_boxes(self):
        for sensor in self.sensor_mapping.values():
            state = self.setup_file.value(sensor.tag)
            sensor.widget.setChecked(state)

    def redraw_date_boxes(self):
        mapping = [(self.comboBox_start_time,
                    self.dateTimeEdit_start_time,
                    START_TIME),
                   (self.comboBox_end_time,
                    self.dateTimeEdit_end_time,
                    END_TIME)]
        for combo_box, date_time, occasion in mapping:
            if combo_box.currentIndex() == 1:
                date_time.setVisible(True)
                time = self.setup_file.value(occasion)
                time = QDateTime.fromString(time, 'yyyy-MM-dd HH:mm:ss')
                date_time.setDateTime(time)
            else:
                date_time.setVisible(False)

    def redraw_burst(self):
        if not self.setup_file.orient_enabled():
            return

        if self.comboBox_orient_burst_rate.currentIndex() == 0:
            self.lineEdit_burst_duration.setEnabled(False)
            self.checkBox_continuous.setEnabled(False)
            self.lineEdit_burst_duration.setText('0')
        elif self.checkBox_continuous.isChecked():
            self.lineEdit_burst_duration.setEnabled(False)
            self.comboBox_orient_burst_rate.setEnabled(False)
        else:
            self.lineEdit_burst_duration.setEnabled(True)
            self.checkBox_continuous.setEnabled(True)
            self.comboBox_orient_burst_rate.setEnabled(True)
            count = self.setup_file.value(ORIENTATION_BURST_COUNT)
            rate = self.setup_file.value(ORIENTATION_BURST_RATE)
            seconds = count // rate
            index = list(BURST_FREQUENCY).index(rate)
            self.comboBox_orient_burst_rate.setCurrentIndex(index + 1)
            self.lineEdit_burst_duration.setText(str(seconds))

    def date_time_combobox_changed(self, occasion):
        mapping = {'start_time':
                   (self.comboBox_start_time,
                    self.dateTimeEdit_start_time,
                    START_TIME),
                   'end_time':
                   (self.comboBox_end_time,
                    self.dateTimeEdit_end_time,
                    END_TIME)}
        combo_box, datetime_edit, tag = mapping[occasion]
        if combo_box.currentIndex() == 0:
            current_time = QDateTime.currentDateTime().toTime_t()
            # next_hour = (current_time//3600)+3600
            # self.setup_file.set_time(tag, next_hour)
        else:
            self.date_time_changed(occasion)

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
            self.setup_file.set_orient_burst_count(1)
            self.setup_file.set_orient_burst_rate(2)
        else:
            burst_rate = BURST_FREQUENCY[index-1]
            seconds = self.lineEdit_burst_duration.text()
            self.setup_file.set_orient_burst_rate(burst_rate)
            try:
                self.setup_file.set_orient_burst_count(burst_rate*int(seconds))
            except ValueError:
                self.setup_file.set_orient_burst_count(burst_rate)
                self.show_error(self.lineEdit_burst_duration, False)

    def date_time_changed(self, occasion):
        widget, value = self.date_mapping[occasion]
        date_time = widget.dateTime()
        date_time_string = date_time.toString('yyyy-MM-dd HH:mm:ss')
        try:
            self.setup_file.set_time(value, date_time_string)
            # TODO Show error dialog
        except ValueError:
            pass

    def interval_changed(self, sensor):
        index = self.interval_mapping[sensor].widget.currentIndex()
        tag = self.interval_mapping[sensor].tag
        self.setup_file.set_interval(tag, INTERVALS[index])

    def sensor_enabled_slot(self, sensor):
        state = self.sensor_mapping[sensor].widget.isChecked()
        tag = self.interval_mapping[sensor].tag
        self.setup_file.set_channel_enabled(tag, state)

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
        if self.checkBox_continuous.isChecked():
            self.comboBox_orient_interval.setCurrentIndex(0)
            self.lineEdit_burst_duration.setText('1')
        self.redraw()

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
