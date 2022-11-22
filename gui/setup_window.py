from gui.setup_ui import Ui_Frame
from setup_file.setup_file import SetupFile
from setup_file.setup_file import (
    DEFAULT_SETUP,
    INTERVALS,
    INTERVAL_STRING,
    BURST_FREQUENCY,
    ORIENTATION_BURST_COUNT,
    ORIENTATION_BURST_RATE,
    PRESSURE_BURST_COUNT,
    TEMPERATURE_INTERVAL,
    ORIENTATION_INTERVAL,
    ACCELEROMETER_ENABLED,
    MAGNETOMETER_ENABLED,
    TEMPERATURE_ENABLED,
    PRESSURE_ENABLED,
    LED_ENABLED,
    FILE_NAME,
    START_TIME,
    END_TIME,
    INTERVAL_START
)
from collections import namedtuple
from PyQt5.QtCore import QDateTime, QSettings
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from gui.description_generator import DescriptionGenerator
from gui import dialogs
from gui.gui_utils import set_enabled
import os
from datetime import datetime
import json
from pathlib import Path
import numpy as np


sensor_map = namedtuple('sensor_map', ['widget', 'tag'])


def appdata_directory():
    path = os.path.join(os.getenv('APPDATA'),
                        'LowellInstruments',
                        'Domino')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def load_presets():
    with open('factory_presets.json') as f:
        presets = json.load(f)
    try:
        with open(Path(appdata_directory(), 'user_presets_pressure.json')) as f:
            user_presets = json.load(f)
    except FileNotFoundError:
        user_presets = []
    presets.extend(user_presets)
    new_preset = {
        'name': 'New Preset',
        'description': 'Enter your description',
        'factory': False,
        'settings': DEFAULT_SETUP
    }
    presets.append(new_preset)
    return presets


def fix_data_types(presets):
    fcn_map = {
        np.int32: int,
        np.float64: float
    }
    for p in presets:
        for tag, value in p['settings'].items():
            if type(value) in fcn_map:
                p['settings'][tag] = fcn_map[type(value)](value)
    return presets


def save_presets(presets):
    # saves user presets, removes factory presets
    to_save = [x for x in presets if not x['factory']]
    to_save = [x for x in to_save if x['name'] != 'New Preset']
    to_save = fix_data_types(to_save)
    with open(Path(appdata_directory(), 'user_presets_pressure.json'), 'w') as f:
        json.dump(to_save, f, indent=4)


class SetupFrame(Ui_Frame):
    def __init__(self):
        self.setup_file = SetupFile()
        self.presets = load_presets()
        self.interval_mapping = None
        self.sensor_mapping = None
        self.date_mapping = None
        self.description = DescriptionGenerator(self.setup_file)

    def load_last_preset(self, name):
        try:
            ind = [x['name'] for x in self.presets].index(name)
            self.setup_file.reset()
            self.setup_file.update_dict(self.presets[ind]['settings'])
            return ind
        except ValueError:
            return

    def setupUi(self, frame):
        self.frame = frame
        super().setupUi(frame)
        self.lineEdit_file_name.setMaxLength(15)
        self.populate_combo_boxes()
        self.setup_mapping()
        self.set_retain_size([self.dateTimeEdit_start_time,
                              self.dateTimeEdit_end_time])
        self.redraw()
        self.connect_signals()

        ind = self.load_last_preset(QSettings().value('preset', None))
        ind = ind if ind else 0
        self.comboBox_preset.setCurrentIndex(ind)
        self.preset_changed(ind)

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
        self.checkBox_pressure.stateChanged.connect(
            lambda: self.sensor_enabled_slot('pressure'))
        self.checkBox_led.stateChanged.connect(
            lambda: self.sensor_enabled_slot('led'))
        self.lineEdit_burst_duration.editingFinished.connect(
            lambda: self.duration_changed('orientation'))
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
        self.comboBox_preset.activated.connect(self.preset_changed)
        self.pushButton_delete.clicked.connect(self.delete_preset)
        self.pushButton_save_preset.clicked.connect(self.save_preset)
        self.pushButton_copy_preset.clicked.connect(self.copy_preset)

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
            'pressure':
                sensor_map(self.checkBox_pressure, PRESSURE_ENABLED),
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
        self.comboBox_orient_burst_rate.addItems(burst_list)
        self.populate_presets()

    def populate_presets(self):
        self.comboBox_preset.clear()
        self.comboBox_preset.addItems([x['name'] for x in self.presets])
        # unfortunately the separator counts as an item which throws off
        # the index relationship between self.presets and the combobox
        # n_factory = sum([1 for x in self.presets if x['factory']])
        # self.comboBox_preset.insertSeparator(n_factory)

    def redraw(self, *args):
        file_name = self.setup_file.value(FILE_NAME)[:-4]
        self.lineEdit_file_name.setText(file_name)
        self.redraw_temperature()
        self.redraw_orient_group()
        self.redraw_burst_duration()
        self.redraw_interval_combo_boxes()
        self.redraw_check_boxes()
        self.redraw_date_boxes()
        description = self.description.description()
        self.label_description.setText(description)
        if self.comboBox_preset.currentText() == 'New Preset':
            self.presets[-1]['settings'] = self.setup_file._setup_dict

    def redraw_temperature(self):
        state = True if self.setup_file.value(TEMPERATURE_ENABLED) else False
        self.comboBox_temp_interval.setEnabled(state)

    def redraw_orient_group(self):
        burst_widgets = [
            self.comboBox_orient_interval,
            self.comboBox_orient_burst_rate,
            self.lineEdit_burst_duration]
        burst_widget_state = (
                self.setup_file.value(ACCELEROMETER_ENABLED) or
                self.setup_file.value(MAGNETOMETER_ENABLED) or
                self.setup_file.value(PRESSURE_ENABLED))
        set_enabled(burst_widgets, burst_widget_state)

        rate = self.setup_file.value(ORIENTATION_BURST_RATE)
        index = list(BURST_FREQUENCY).index(rate)
        self.comboBox_orient_burst_rate.setCurrentIndex(index)

    def redraw_burst_duration(self):
        rate = self.setup_file.value(ORIENTATION_BURST_RATE)
        mapping = [
            (self.lineEdit_burst_duration, ORIENTATION_BURST_COUNT)
        ]
        for line_edit, value_field in mapping:
            count = self.setup_file.value(value_field)
            seconds = count // rate

            current_state = line_edit.isEnabled()
            line_edit.setText(str(seconds))
            line_edit.setEnabled(current_state)

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
            value = self.setup_file.value(occasion)
            if value == DEFAULT_SETUP[occasion]:
                combo_box.setCurrentIndex(0)
                date_time.setVisible(False)
            elif value in INTERVAL_START:
                combo_box.setCurrentIndex(INTERVAL_START.index(value)+1)
                date_time.setVisible(False)
            else:
                combo_box.setCurrentIndex(combo_box.count() - 1)
                date_time.setVisible(True)
                time = self.setup_file.value(occasion)
                time = QDateTime.fromString(time, 'yyyy-MM-dd HH:mm:ss')
                date_time.setDateTime(time)

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
            self.setup_file.set_time(tag, DEFAULT_SETUP[tag])

        elif combo_box.currentIndex() == combo_box.count()-1:
            time_str = self._time_value(occasion)
            try:
                self.setup_file.set_time(tag, time_str)
            except ValueError:
                pass
            finally:
                self.redraw()
        else:
            start_time = INTERVAL_START[combo_box.currentIndex()-1]
            self.setup_file.set_time(tag, start_time)

        self.redraw()

    def _time_value(self, occasion):
        current_time = QDateTime.currentDateTime().toTime_t()
        next_hour = QDateTime.fromTime_t((current_time // 3600) * 3600 + 3600)
        if occasion == 'start_time':
            return next_hour.toString('yyyy-MM-dd HH:mm:ss')
        else:
            start_time = self.setup_file.value(START_TIME)
            if (start_time == DEFAULT_SETUP[START_TIME] or
                    start_time in INTERVAL_START):
                end_time = next_hour.addMonths(1)
            else:
                time_obj = QDateTime.fromString(start_time,
                                                'yyyy-MM-dd HH:mm:ss')
                end_time = time_obj.addMonths(1)
            return end_time.toString('yyyy-MM-dd HH:mm:ss')

    def filename_changed(self):
        string = self.lineEdit_file_name.text()
        try:
            self.setup_file.set_filename(string + '.lid')
        except ValueError:
            message = 'There were invalid characters in the file name. ' \
                      'Reverting to prior value. Use only alphanumeric ' \
                      'values and/or underscores and dashes. 15 characters maximum.'
            dialogs.error_message('Description Error', message)
        finally:
            self.redraw()

    def burst_rate_changed(self):
        index = self.comboBox_orient_burst_rate.currentIndex()
        burst_rate = BURST_FREQUENCY[index]
        seconds = self.lineEdit_burst_duration.text()
        self.setup_file.set_orient_burst_rate(burst_rate)
        try:
            self.setup_file.set_burst_count(
                ORIENTATION_BURST_COUNT,
                burst_rate*int(seconds))
        except ValueError:
            self.setup_file.set_burst_count(
                ORIENTATION_BURST_COUNT,
                burst_rate)
        finally:
            self.redraw()

    def burst_mode_changed(self, sensor):
        mapping = {
            'accel_mag': (
                self.lineEdit_burst_duration,
                ORIENTATION_BURST_COUNT)
        }
        line_edit, value_field = mapping.get(sensor)

        line_edit.setEnabled(True)
        burst = self.setup_file.value(ORIENTATION_BURST_RATE)
        self.setup_file.set_burst_count(value_field, burst)
        self.redraw()

    def preset_changed(self, index):
        preset = self.presets[index]
        is_factory = preset['factory']
        is_new_preset = self.comboBox_preset.currentText() == 'New Preset'
        self.pushButton_delete.setDisabled(is_factory | is_new_preset)
        self.pushButton_save_preset.setDisabled(is_factory)
        self.groupBox_temperature.setDisabled(is_factory)
        self.groupBox_orient.setDisabled(is_factory)
        self.groupBox_start.setDisabled(is_factory)
        self.groupBox_stop.setDisabled(is_factory)
        self.lineEdit_preset.setDisabled(is_factory)
        self.lineEdit_preset.setText(preset['description'])

        self.pushButton_copy_preset.setDisabled(is_new_preset)

        self.setup_file.reset()
        self.setup_file.preset = preset['name']
        self.setup_file.update_dict(preset['settings'])
        self.redraw()

    def copy_preset(self):
        index = self.comboBox_preset.currentIndex()
        preset = dict(self.presets[index])
        preset['name'] = 'New Preset'
        preset['description'] = 'Enter your description here'
        preset['factory'] = False
        self.presets[-1] = preset
        self.comboBox_preset.setCurrentIndex(len(self.presets)-1)
        self.preset_changed(len(self.presets)-1)

    def delete_preset(self):
        index = self.comboBox_preset.currentIndex()
        preset = dict(self.presets[index])
        if dialogs.ask_delete_preset(preset['name']):
            self.presets.pop(index)
            self.populate_presets()
            self.comboBox_preset.setCurrentIndex(0)
            self.preset_changed(0)
        save_presets(self.presets)

    def save_preset(self):
        index = self.comboBox_preset.currentIndex()
        preset = self.presets[index]

        if preset['name'] == 'New Preset':
            new_name = dialogs.ask_new_preset_name()
            if new_name is None:
                return
            existing_names = [x['name'] for x in self.presets]
            if new_name == 'New Preset':
                dialogs.error_message(
                    'Invalid name',
                    '"New Preset" is an invalid preset name.'
                )
                return

            if new_name in existing_names:
                dialogs.error_message(
                    'Invalid name',
                    f'The name "{new_name}" is already in use.'
                )
                return

            if new_name == '':
                dialogs.error_message(
                    'Invalid name',
                    'Please enter a valid name.'
                )
                return
            preset['name'] = new_name

        preset['settings'] = self.setup_file._setup_dict
        preset['description'] = self.lineEdit_preset.text()
        save_presets(self.presets)
        self.presets = load_presets()
        self.populate_presets()
        self.preset_changed(index)
        self.comboBox_preset.setCurrentIndex(index)
        dialogs.inform('Preset saved',
                       f'"{preset["name"]}" saved successfully')

    def date_time_changed(self, occasion):
        widget, value = self.date_mapping[occasion]
        date_time = widget.dateTime()
        date_time_string = date_time.toString('yyyy-MM-dd HH:mm:ss')
        try:
            self.setup_file.set_time(value, date_time_string)
        except ValueError:
            message = 'Start time must be before end time. Reverting value.'
            dialogs.error_message('Start/Stop Time Error', message)
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

    def duration_changed(self, sensor):
        burst_count = {'orientation': ORIENTATION_BURST_COUNT}.get(sensor)
        line_edit = {'orientation': self.lineEdit_burst_duration}.get(sensor)
        seconds = line_edit.text()
        rate = self.setup_file.value(ORIENTATION_BURST_RATE)
        try:
            self.setup_file.set_burst_count(
                burst_count,
                int(seconds)*rate)
        except ValueError:
            message = 'The burst duration must be less than or equal to ' \
                      'the orientation interval. Reverting value.'
            line_edit.blockSignals(True)
            dialogs.error_message('Invalid duration', message)
            line_edit.blockSignals(False)
        finally:
            self.redraw()

    def save_file(self):
        self.redraw()
        if not self.pre_save_check():
            return

        directory = QSettings().value('setup_file_directory', '', type=str)
        file_name = os.path.join(directory, 'MAT.cfg')
        path = QFileDialog.getSaveFileName(self.frame, 'Save File', file_name)
        if not path[0]:
            return
        if not path[0].endswith('MAT.cfg'):
            message = 'Filename must be MAT.cfg. File not saved. ' \
                      'Please save again.'
            dialogs.error_message('File name error', message)
            self.save_file()
            return
        directory = os.path.dirname(path[0])
        QSettings().setValue('setup_file_directory', directory)
        QSettings().setValue('setup_file', self.setup_file._setup_dict)
        QSettings().setValue('preset', self.comboBox_preset.currentText())
        self.setup_file.write_file(path[0])
        message = 'Setup file saved but your device is NOT RECORDING ' \
                  'yet.  To start recording, switch to the ' \
                  '"Device" tab and click the "Start Running" button.'
        dialogs.inform('File Saved', message)

    def pre_save_check(self):
        passed = True
        channels = self.setup_file.value(ACCELEROMETER_ENABLED) \
                   or self.setup_file.value(MAGNETOMETER_ENABLED) \
                   or self.setup_file.value(TEMPERATURE_ENABLED)
        if not channels:
            dialogs.no_channels_warning()
            passed = False

        if self.setup_file.value('STM') not in INTERVAL_START and \
                self.setup_file.value('STM') != DEFAULT_SETUP['STM'] and \
                self.dateTimeEdit_start_time.dateTime() < QDateTime.currentDateTime():
            message = 'Start time must be in the future.'
            dialogs.error_message('Start/Stop Time Error', message)
            passed = False

        if self.setup_file.major_interval_bytes() > 32000:
            dialogs.major_interval_warning()
            passed = False
        if not self.temp_compensated_okay_to_save():
            passed = False
        end_time = self.setup_file.value(END_TIME)
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        if self.setup_file.value(START_TIME) in INTERVAL_START:
            # this is a workaround to make the start on interval values
            # work with existing code. Basically the logger will start
            # immediately (within an hour at most)
            start_time = datetime.now()
        else:
            start_time = self.setup_file.value(START_TIME)
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        current_time = QDateTime.currentDateTime().toPyDateTime()
        if current_time > end_time:
            dialogs.end_time_in_past()
            passed = False
        if (start_time-current_time).days > 365:
            proceed = dialogs.end_time_gt_year()
            if not proceed:
                passed = False
        return passed

    def temp_compensated_okay_to_save(self):
        save = True
        if self.setup_file.value(MAGNETOMETER_ENABLED):
            if not self.setup_file.value(TEMPERATURE_ENABLED):
                save = dialogs.temp_compensated_sensor_warning()
        return save
