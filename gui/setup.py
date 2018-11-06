from gui.setup_ui import Ui_Frame
from setup_file.setup_file import SetupFile
from setup_file.setup_file import (
    INTERVALS,
    INTERVAL_STRING,
    BURST_FREQUENCY,
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
from re import search
from collections import namedtuple


sensor_map = namedtuple('sensor_map', ['widget', 'value', 'change_fcn'])


class SetupFrame(Ui_Frame):
    def __init__(self):
        self.setup_file = SetupFile()
        self.interval_mapping = None
        self.sensor_mapping = None

    def setupUi(self, frame):
        super().setupUi(frame)
        self.populate_combo_boxes()
        self.lineEdit_file_name.textChanged.connect(
                    self.filename_changed)
        self.comboBox_orient_interval.currentIndexChanged.connect(
                    lambda: self.interval_changed('orientation'))
        self.comboBox_temp_interval.currentIndexChanged.connect(
                    lambda: self.interval_changed('temperature'))
        self.checkBox_temperature.stateChanged.connect(
                    lambda: self.sensor_enabled_slot('temperature'))
        self.checkBox_magnetometer.stateChanged.connect(
                    lambda: self.sensor_enabled_slot('magnetometer'))
        self.checkBox_accelerometer.stateChanged.connect(
                    lambda: self.sensor_enabled_slot('accelerometer'))
        self.checkBox_led.stateChanged.connect(
                    lambda: self.sensor_enabled_slot('led'))
        self.lineEdit_burst_duration.textChanged.connect(self.duration_changed)
        self.checkBox_continuous.stateChanged.connect(self.continuous_changed)
        self.comboBox_orient_burst_rate.currentIndexChanged.connect(
                    self.burst_rate_slot)
        self.comboBox_start_time.currentIndexChanged.connect(
                    self.redraw_date_boxes)
        self.comboBox_end_time.currentIndexChanged.connect(
                    self.redraw_date_boxes)
        self.lineEdit_file_name.setMaxLength(11)
        self.setup_mapping()

        self.redraw()

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
        self.comboBox_orient_burst_rate.addItems(burst_list)

    def redraw(self):
        file_name = self.setup_file.value(FILE_NAME)[:-4]
        self.lineEdit_file_name.setText(file_name)
        self.redraw_combo_boxes()
        self.redraw_check_boxes()
        self.redraw_date_boxes()
        orient_group = [self.comboBox_orient_interval,
                        self.comboBox_orient_burst_rate,
                        self.lineEdit_burst_duration,
                        self.checkBox_continuous]
        if self.setup_file.orient_enabled():
            self._set_enabled(orient_group, True)
            self.continuous_changed()
        else:
            self._set_enabled(orient_group, False)

    def redraw_date_boxes(self):
        mapping = [(self.comboBox_start_time, self.dateTimeEdit_start_time),
                   (self.comboBox_end_time, self.dateTimeEdit_end_time)]
        for combo_box, date_time in mapping:
            state = True if combo_box.currentIndex() == 1 else False
            date_time.setEnabled(state)

    def redraw_check_boxes(self):
        for sensor in self.sensor_mapping.values():
            state = sensor.value()
            sensor.widget.setChecked(state)
        state = self.setup_file.value(TEMPERATURE_ENABLED)
        self.comboBox_temp_interval.setEnabled(state)

    def filename_changed(self):
        string = self.lineEdit_file_name.text()
        try:
            self.setup_file.set_filename(string + '.lid')
            self.show_error(self.lineEdit_file_name, False)
        except ValueError:
            self.show_error(self.lineEdit_file_name, True)

    def redraw_combo_boxes(self):
        for sensor in ['temperature', 'orientation']:
            intervals = self.setup_file.available_intervals(sensor)
            for i, val in enumerate(intervals):
                widget = self.interval_mapping[sensor].widget
                widget.model().item(i).setEnabled(val)
            interval = self.interval_mapping[sensor].value()
            index = list(INTERVALS).index(interval)
            self.interval_mapping[sensor].widget.setCurrentIndex(index)

    def burst_rate_slot(self):
        index = self.comboBox_orient_burst_rate.currentIndex()
        burst_rate = BURST_FREQUENCY[index]
        self.setup_file.set_orient_burst_rate(burst_rate)

    def interval_changed(self, sensor):
        index = self.interval_mapping[sensor].widget.currentIndex()
        self.interval_mapping[sensor].change_fcn(INTERVALS[index])
        self.redraw_combo_boxes()

    def sensor_enabled_slot(self, sensor):
        state = self.sensor_mapping[sensor].widget.isChecked()
        self.sensor_mapping[sensor].change_fcn(state)
        self.redraw()

    def duration_changed(self):
        seconds = self.lineEdit_burst_duration.text()
        rate = BURST_FREQUENCY[self.comboBox_orient_burst_rate.currentIndex()]
        try:
            self.setup_file.set_orient_burst_count(int(seconds)*rate)
            self.show_error(self.lineEdit_burst_duration, False)
        except ValueError:
            self.show_error(self.lineEdit_burst_duration, True)

    def show_error(self, widget, error):
        if error:
            widget.setStyleSheet('background-color: rgb(255, 255, 0);')
        else:
            widget.setStyleSheet('')

    def continuous_changed(self):
        widgets = [self.comboBox_orient_interval,
                   self.lineEdit_burst_duration]
        if self.checkBox_continuous.isChecked():
            self.comboBox_orient_interval.setCurrentIndex(0)
            self.lineEdit_burst_duration.setText('1')
            self._set_enabled(widgets, False)
        else:
            self._set_enabled(widgets, True)

    def _set_enabled(self, widget, state):
        if type(widget) is not list:
            widget = [widget]
        for w in widget:
            w.setEnabled(state)
