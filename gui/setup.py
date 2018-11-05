from gui.setup_ui import Ui_Frame
from setup_file.setup_file import SetupFile
from setup_file.setup_file import (
    INTERVALS,
    INTERVAL_STRING,
    BURST_FREQUENCY,
    TEMPERATURE_INTERVAL,
    ORIENTATION_INTERVAL
)
from re import search


class SetupFrame(Ui_Frame):
    def __init__(self):
        self.setup_file = SetupFile()
        self.orient_map = None
        self.temp_map = None
        self.interval_widget = None
        self.interval_change_fcn = None
        self.interval_value = None

    def setupUi(self, frame):
        super().setupUi(frame)
        self.populate_combo_boxes()
        self.comboBox_orient_interval.currentIndexChanged.connect(
                            lambda: self.interval_changed('orientation'))
        self.comboBox_temp_interval.currentIndexChanged.connect(
                            lambda: self.interval_changed('temperature'))
        self.lineEdit_burst_duration.textChanged.connect(self.duration_changed)
        self.checkBox_continuous.stateChanged.connect(self.continuous_changed)
        self.comboBox_orient_burst_rate.currentIndexChanged.connect(
                                                self.burst_rate_slot)
        self.lineEdit_file_name.setMaxLength(11)
        self.interval_widget = \
            {'temperature': self.comboBox_temp_interval,
             'orientation': self.comboBox_orient_interval}
        self.interval_change_fcn = \
            {'temperature': self.setup_file.set_temperature_interval,
             'orientation': self.setup_file.set_orient_interval}
        self.interval_value = \
            {'temperature': TEMPERATURE_INTERVAL,
             'orientation': ORIENTATION_INTERVAL}

        self.redraw()

    def populate_combo_boxes(self):
        self.comboBox_temp_interval.addItems(INTERVAL_STRING)
        self.comboBox_orient_interval.addItems(INTERVAL_STRING)
        burst_list = [str(x) + ' Hz' for x in BURST_FREQUENCY]
        self.comboBox_orient_burst_rate.addItems(burst_list)

    def redraw(self):
        self.redraw_combo_boxes()

    def redraw_combo_boxes(self):
        for sensor in ['temperature', 'orientation']:
            intervals = self.setup_file.available_intervals(sensor)
            for i, val in enumerate(intervals):
                self.interval_widget[sensor].model().item(i).setEnabled(val)
            interval = self.setup_file.value(self.interval_value[sensor])
            index = list(INTERVALS).index(interval)
            self.interval_widget[sensor].setCurrentIndex(index)

    def burst_rate_slot(self):
        index = self.comboBox_orient_burst_rate.currentIndex()
        burst_rate = BURST_FREQUENCY[index]
        self.setup_file.set_orient_burst_rate(burst_rate)

    def interval_changed(self, sensor):
        index = self.interval_widget[sensor].currentIndex()
        self.interval_change_fcn[sensor](INTERVALS[index])
        self.redraw_combo_boxes()

    def sensor_enabled_slot(self, sensor):
        pass

    def duration_changed(self):
        seconds = self.lineEdit_burst_duration.text()
        rate = BURST_FREQUENCY[self.comboBox_orient_burst_rate.currentIndex()]
        if not self._verify_integer(seconds):
            self._error_color(self.lineEdit_burst_duration, True)
        try:
            self.setup_file.set_orient_burst_count(int(seconds)*rate)
            self._error_color(self.lineEdit_burst_duration, False)
        except ValueError:
            self._error_color(self.lineEdit_burst_duration, True)

    def _verify_integer(self, string):
        if search('^[1-9]+[0-9]*$', string):
            return True
        return False

    def _error_color(self, widget, error):
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

    def update_description(self):
        pass
