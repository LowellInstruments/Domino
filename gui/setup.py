from gui.setup_ui import Ui_Frame
from setup_file.setup_file import SetupFile
from setup_file.setup_file import (
    DEFAULT_SETUP,
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
import logging
from gui.description_generator import DescriptionGenerator
from mat import appdata
from gui.gui_utils import error_message, set_enabled
import os


sensor_map = namedtuple('sensor_map', ['widget', 'tag'])


class SetupFrame(Ui_Frame):
    def __init__(self):
        application_data = appdata.get_userdata('domino.dat')
        setup_dict = application_data.get('setup_file', None)
        self.setup_file = SetupFile(setup_dict)
        self.interval_mapping = None
        self.sensor_mapping = None
        self.date_mapping = None
        self.description = DescriptionGenerator(self.setup_file)
        logging.basicConfig(level=logging.DEBUG)

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.lineEdit_file_name.setMaxLength(11)
        self.populate_combo_boxes()
        self.setup_mapping()
        self.set_retain_size([self.dateTimeEdit_start_time,
                              self.dateTimeEdit_end_time])
        self.redraw()
        self.connect_signals()

    def set_retain_size(self, widgets):
        for widget in widgets:
            date_time_size_policy = widget.sizePolicy()
            date_time_size_policy.setRetainSizeWhenHidden(True)
            widget.setSizePolicy(date_time_size_policy)

    def connect_signals(self):
        # user only signals (not triggered by programatic changes)
        # qlineedit -- textEdited
        # qcombobox -- activated
        self.lineEdit_file_name.editingFinished.connect(
            self.filename_changed)
        self.comboBox_orient_interval.activated.connect(
            lambda: self.interval_changed('orientation'))
        self.comboBox_temp_interval.activated.connect(
            lambda: self.interval_changed('temperature'))
        self.checkBox_temperature.stateChanged.connect(
            lambda: self.sensor_enabled_slot('temperature'))
        self.checkBox_magnetometer.stateChanged.connect(
            lambda: self.sensor_enabled_slot('magnetometer'))
        self.checkBox_accelerometer.stateChanged.connect(
            lambda: self.sensor_enabled_slot('accelerometer'))
        self.checkBox_led.stateChanged.connect(
            lambda: self.sensor_enabled_slot('led'))
        self.lineEdit_burst_duration.editingFinished.connect(
            self.duration_changed)
        self.checkBox_continuous.stateChanged.connect(
            self.continuous_changed)
        self.comboBox_orient_burst_rate.activated.connect(
            self.burst_rate_changed)
        self.comboBox_start_time.activated.connect(
            lambda: self.date_time_combobox_changed('start_time'))
        self.comboBox_end_time.activated.connect(
            lambda: self.date_time_combobox_changed('end_time'))
        self.dateTimeEdit_start_time.dateTimeChanged.connect(
            lambda: self.date_time_changed('start_time'))
        self.dateTimeEdit_end_time.dateTimeChanged.connect(
            lambda: self.date_time_changed('end_time'))
        self.pushButton_save.clicked.connect(
            self.save_file)

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

    def redraw(self, *args):
        logging.debug(args)
        file_name = self.setup_file.value(FILE_NAME)[:-4]
        self.lineEdit_file_name.setText(file_name)
        self.redraw_temperature()
        self.redraw_orient_group()
        self.redraw_interval_combo_boxes()
        self.redraw_check_boxes()
        self.redraw_date_boxes()
        self.redraw_burst()
        description = self.description.description()
        self.label_description.setText(description)

    def redraw_temperature(self):
        state = True if self.setup_file.value(TEMPERATURE_ENABLED) else False
        self.comboBox_temp_interval.setEnabled(state)

    def redraw_orient_group(self):
        orient_group = [self.comboBox_orient_interval,
                        self.comboBox_orient_burst_rate,
                        self.lineEdit_burst_duration,
                        self.checkBox_continuous]
        state = True if self.setup_file.orient_enabled() else False
        set_enabled(orient_group, state)

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
            if self.setup_file.value(occasion) != DEFAULT_SETUP[occasion]:
                combo_box.setCurrentIndex(1)
                date_time.setVisible(True)
                time = self.setup_file.value(occasion)
                time = QDateTime.fromString(time, 'yyyy-MM-dd HH:mm:ss')
                date_time.setDateTime(time)
            else:
                combo_box.setCurrentIndex(0)
                date_time.setVisible(False)

    def redraw_burst(self):
        if not self.setup_file.orient_enabled():
            return
        if self.setup_file.value(ORIENTATION_BURST_COUNT) == 1:
            self.lineEdit_burst_duration.setEnabled(False)
            self.checkBox_continuous.setEnabled(False)
            #self.lineEdit_burst_duration.setText('0')
        elif self.setup_file.is_continuous:
            self.lineEdit_burst_duration.setEnabled(False)
            self.comboBox_orient_interval.setEnabled(False)
            self.lineEdit_burst_duration.setText('1')
        else:
            self.lineEdit_burst_duration.setEnabled(True)
            self.comboBox_orient_interval.setEnabled(True)
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
        if combo_box.currentIndex() == 1:
            time_str = self._time_value(occasion)
            try:
                self.setup_file.set_time(tag, time_str)
            except ValueError:
                pass
            finally:
                self.redraw()
        else:
            self.setup_file.set_time(tag, DEFAULT_SETUP[tag])
        self.redraw()

    def _time_value(self, occasion):
        current_time = QDateTime.currentDateTime().toTime_t()
        next_hour = QDateTime.fromTime_t((current_time // 3600) * 3600 + 3600)
        if occasion == 'start_time':
            return next_hour.toString('yyyy-MM-dd HH:mm:ss')
        else:
            start_time = self.setup_file.value(START_TIME)
            if start_time == DEFAULT_SETUP[START_TIME]:
                end_time = next_hour.addYears(1)
            else:
                time_obj = QDateTime.fromString(start_time,
                                                'yyyy-MM-dd HH:mm:ss')
                end_time = time_obj.addYears(1)
            return end_time.toString('yyyy-MM-dd HH:mm:ss')

    def filename_changed(self):
        string = self.lineEdit_file_name.text()
        try:
            self.setup_file.set_filename(string + '.lid')
            # show_error(self.lineEdit_file_name, False)
        except ValueError:
            message = 'There were invalid characters in the file name. ' \
                      'Reverting value.'
            error_message(self.frame, 'File name error', message)
        finally:
            self.redraw()
            # show_error(self.lineEdit_file_name, True)

    def burst_rate_changed(self):
        index = self.comboBox_orient_burst_rate.currentIndex()
        if index == 0:
            self.setup_file.set_orient_burst_count(1)
            self.setup_file.set_orient_burst_rate(2)
            self.redraw()
        else:
            burst_rate = BURST_FREQUENCY[index-1]
            seconds = self.lineEdit_burst_duration.text()
            self.setup_file.set_orient_burst_rate(burst_rate)
            try:
                self.setup_file.set_orient_burst_count(burst_rate*int(seconds))
            except ValueError:
                self.setup_file.set_orient_burst_count(burst_rate)
            finally:
                self.redraw()

    def date_time_changed(self, occasion):
        widget, value = self.date_mapping[occasion]
        date_time = widget.dateTime()
        date_time_string = date_time.toString('yyyy-MM-dd HH:mm:ss')
        try:
            self.setup_file.set_time(value, date_time_string)
        except ValueError:
            message = 'Start time must be before end time. Reverting value.'
            error_message(self.frame, 'Start/Stop Time Error', message)
        finally:
            self.redraw()

    def interval_changed(self, sensor):
        index = self.interval_mapping[sensor].widget.currentIndex()
        tag = self.interval_mapping[sensor].tag
        self.setup_file.set_interval(tag, INTERVALS[index])
        self.redraw()

    def sensor_enabled_slot(self, sensor):
        state = self.sensor_mapping[sensor].widget.isChecked()
        tag = self.sensor_mapping[sensor].tag
        self.setup_file.set_channel_enabled(tag, state)
        self.redraw()

    def duration_changed(self):
        seconds = self.lineEdit_burst_duration.text()
        rate = self.setup_file.value(ORIENTATION_BURST_RATE)
        count = self.setup_file.value(ORIENTATION_BURST_COUNT)
        try:
            self.setup_file.set_orient_burst_count(int(seconds)*rate)
        except ValueError:
            message = 'The burst duration must be less than or equal to ' \
                      'the orientation interval. Reverting value.'
            error_message(self.frame, 'Invalid duration', message)
        finally:
            self.redraw()

    def continuous_changed(self):
        state = self.checkBox_continuous.isChecked()
        self.setup_file.set_continuous(state)
        self.redraw()

    def save_file(self):
        self.redraw()
        if self.setup_file.major_interval_bytes() > 32000:
            message = 'The current logging parameters exceed the logger ' \
                      'buffer size. This can usually be corrected by ' \
                      'reducing the temperature recording interval. The ' \
                      'configuration file was not generated. See the user ' \
                      'guide for more details.'
            QMessageBox.information(self.frame, 'Invalid settings', message)
            return
        application_data = appdata.get_userdata('domino.dat')
        directory = application_data.get('setup_file_directory', '')
        file_name = os.path.join(directory, 'MAT.cfg')
        path = QFileDialog.getSaveFileName(self.frame, 'Save File', file_name)
        if not path[0]:
            return
        if not path[0].endswith('MAT.cfg'):
            message = 'Filename must be MAT.cfg. File not saved. ' \
                      'Please save again.'
            error_message(self.frame, 'File name error', message)
            self.save_file()
            return
        directory = os.path.dirname(path[0])
        appdata.set_userdata('domino.dat', 'setup_file_directory', directory)
        appdata.set_userdata('domino.dat', 'setup_file',
                             self.setup_file._setup_dict)
        self.setup_file.write_file(path[0])
        QMessageBox.information(self.frame,
                                'File Saved',
                                'File saved successfully')
