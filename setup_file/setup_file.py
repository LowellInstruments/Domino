from datetime import datetime
from mat.utils import parse_tags
from mat.header import Header
from numpy import array, logical_or, logical_and
from pathlib import Path
from re import compile, search
import mat.sensor


TYPE_INT = ('BMN', 'BMR', 'ORI', 'TRI', 'PRR', 'PRN')
TYPE_BOOL = ('ACL', 'LED', 'MGN', 'TMP', 'PRS', 'PHD')
WRITE_ORDER = ['DFN', 'TMP', 'ACL', 'MGN', 'TRI', 'ORI', 'BMR', 'BMN',
               'STM', 'ETM', 'LED']
INTERVALS = array([1, 2, 5, 10, 15, 20, 30, 60,
                   120, 300, 600, 900, 1800, 3600])
INTERVAL_STRING = array(['1 second', '2 seconds', '5 seconds', '10 seconds',
                         '15 seconds', '20 seconds', '30 seconds',
                         '1 minute', '2 minutes', '5 minutes', '10 minutes',
                         '15 minutes', '30 minutes', '1 hour'],
                        dtype=object)
BURST_FREQUENCY = array([2, 4, 8, 16, 32, 64])
DEFAULT_SETUP = {'DFN': 'Test.lid', 'TMP': True, 'ACL': True,
                 'MGN': True, 'TRI': 60, 'ORI': 60, 'BMR': 8, 'BMN': 160,
                 'STM': '1970-01-01 00:00:00',
                 'ETM': '2096-01-01 00:00:00',
                 'LED': True}
INTERVAL_START = ['ON_INT_MIN', 'ON_INT_QHR', 'ON_INT-1HR']
FILE_NAME = 'DFN'
TEMPERATURE_ENABLED = 'TMP'
ACCELEROMETER_ENABLED = 'ACL'
MAGNETOMETER_ENABLED = 'MGN'
PRESSURE_ENABLED = 'PRS'
PHOTO_DIODE_ENABLED = 'PHD'
TEMPERATURE_INTERVAL = 'TRI'
ORIENTATION_INTERVAL = 'ORI'
ORIENTATION_BURST_RATE = 'BMR'
ORIENTATION_BURST_COUNT = 'BMN'
START_TIME = 'STM'
END_TIME = 'ETM'
LED_ENABLED = 'LED'
PRESSURE_BURST_RATE = 'PRR'
PRESSURE_BURST_COUNT = 'PRN'


def load_setup_file(path):
    """
    Return a SetupFile object from a MAT.cfg setup file
    """
    with open(path, 'rb') as fid:
        setup_file_string = fid.read().decode('IBM437')
    setup_file_string = _remove_comments(setup_file_string)
    setup_dict = parse_tags(setup_file_string)
    setup_dict = _convert_to_type(setup_dict)
    return SetupFile(setup_dict)


def _remove_comments(setup_file_string):
    while setup_file_string.startswith('//'):
        eol = setup_file_string.find('\r\n')
        setup_file_string = setup_file_string[eol + 2:]
    return setup_file_string


def _convert_to_type(setup_dict):
    for tag, value in setup_dict.items():
        if tag in TYPE_INT:
            setup_dict[tag] = int(value)
        if tag in TYPE_BOOL:
            setup_dict[tag] = value == '1'
    return setup_dict


class SetupFile:
    def __init__(self, setup_dict=None):
        self._setup_dict = setup_dict or dict(DEFAULT_SETUP)
        self.time_re = compile(r'^[0-9$]{4}-[0-1][0-9]-[0-3][0-9] '
                               '(0?[0-9]|1[0-9]|2[0-3]):'
                               '[0-5][0-9]:[0-6][0-9]$')
        self.is_continuous = self._check_continuous()
        self.is_start_time = False
        self.is_end_time = False
        self.preset = None

    def reset(self):
        self._setup_dict = dict(DEFAULT_SETUP)
        self.is_continuous = False
        self.is_start_time = False
        self.is_end_time = False
        self.preset = None

    def value(self, tag):
        return self._setup_dict[tag]

    def update(self, tag, value):
        self._setup_dict[tag] = value

    def update_dict(self, new_values):
        # merge dict new_values into _setup_dict
        self._setup_dict.update(new_values)
        self.is_continuous = self._check_continuous()

    def major_interval_bytes(self):
        header = Header('')
        header._header = self._setup_dict
        interval, n_bytes = mat.sensor.major_interval_info(header)
        return n_bytes

    def available_intervals(self, sensor):
        """
        Available orientation and temperature intervals must be calculated
        in coordination with each other.
        Returns a logical array (mask) of available orientation or temperature
        intervals
        """
        if sensor not in [TEMPERATURE_INTERVAL, ORIENTATION_INTERVAL]:
            raise ValueError('Unknown sensor {}'.format(sensor))
        opposite_interval = self._opposite_interval(sensor)
        if sensor is TEMPERATURE_INTERVAL:
            return logical_and(self._factors_and_multiples(opposite_interval),
                               INTERVALS >= opposite_interval)
        else:
            return self._factors_and_multiples(opposite_interval)

    def _opposite_interval(self, sensor):
        if sensor is ORIENTATION_INTERVAL:
            return self.value(TEMPERATURE_INTERVAL)
        return self.value(ORIENTATION_INTERVAL)

    def _factors_and_multiples(self, interval):
        return logical_or(INTERVALS % interval == 0,
                          interval % INTERVALS == 0)

    def set_filename(self, filename):
        if not search(r'^[a-zA-Z0-9_\-]{1,15}\.lid$', filename):
            raise ValueError('Filename error')
        self.update(FILE_NAME, filename)

    def set_channel_enabled(self, sensor, state):
        self._confirm_bool(state)
        self.update(sensor, state)

    def orient_enabled(self):
        return (self.value(ACCELEROMETER_ENABLED) or
                self.value(MAGNETOMETER_ENABLED))

    def set_interval(self, channel, value):
        if value not in INTERVALS[self.available_intervals(channel)]:
            raise ValueError('Invalid interval value')
        if channel == ORIENTATION_INTERVAL and self.is_continuous:
            raise ValueError('Cannot change orientation interval or burst '
                             'count when operating in continuous mode')
        self.update(channel, value)
        max_burst_count = value * self.value(ORIENTATION_BURST_RATE)
        if self.value(ORIENTATION_BURST_COUNT) > max_burst_count:
            self.set_orient_burst_count(max_burst_count)
        if self.value(ORIENTATION_INTERVAL) > self.value(TEMPERATURE_INTERVAL):
            self.set_interval(TEMPERATURE_INTERVAL, value)

    def set_orient_burst_rate(self, value):
        if value not in BURST_FREQUENCY:
            raise ValueError('Invalid burst rate')
        self.update(ORIENTATION_BURST_RATE, value)
        if self.is_continuous:
            self.update(ORIENTATION_BURST_COUNT, value)

    def set_orient_burst_count(self, value):
        max_burst_count = (self.value(ORIENTATION_INTERVAL) *
                           self.value(ORIENTATION_BURST_RATE))
        if 0 <= value > max_burst_count:
            raise ValueError('Burst count must be > 0 and <= orient interval '
                             'multiplied by orient burst rate.')
        if self.is_continuous and (value !=
                                   self.value(ORIENTATION_BURST_RATE)):
            raise ValueError('Invalid burst count while in continuous mode')
        self.update(ORIENTATION_BURST_COUNT, value)

    def set_time(self, occasion, time):
        time_dict = {START_TIME: self.value(START_TIME),
                     END_TIME: self.value(END_TIME)}
        time_dict[occasion] = time
        if self._validate_time(time_dict):
            self.update(occasion, time)

    def _validate_time(self, time_dict):
        for key in time_dict:
            if time_dict[key] in INTERVAL_START:
                time_dict[key] = datetime.now()
            else:
                time_dict[key] = datetime.strptime(time_dict[key],
                                                   '%Y-%m-%d %H:%M:%S')
        if time_dict[END_TIME] <= time_dict[START_TIME]:
            raise ValueError('start time and end time must be in '
                             'correct order')
        return True

    def _check_continuous(self):
        if self.value('ORI') * self.value('BMR') == self.value('BMN'):
            return True
        else:
            return False

    def _confirm_bool(self, state):
        if type(state) is not bool:
            raise ValueError('State must be True or False')

    def write_file(self, path):
        file_writer = ConfigFileWriter(path, self._setup_dict, self.preset)
        file_writer.write_file()

    def set_continuous(self, state):
        self._confirm_bool(state)
        self.is_continuous = state
        if state is True:
            self.update(ORIENTATION_INTERVAL, 1)
            burst_rate = self.value(ORIENTATION_BURST_RATE)
            self.update(ORIENTATION_BURST_COUNT, burst_rate)


class ConfigFileWriter:
    def __init__(self, path, setup_dict, preset=None):
        self.path = path
        # make a copy because we may change values in the fix function
        self.setup_dict = dict(setup_dict)
        self._fix_ori_tri()
        self.preset = preset

    def write_file(self):
        directory = Path(self.path)
        with open(directory, 'w', newline='\r\n') as fid:
            self._write_header(fid)
            for line in self._formatted_tag_and_value():
                fid.write(line)

    def _write_header(self, fid):
        fid.write('// Lowell Instruments LLC - MAT Data Logger - '
                  'Configuration File\n')
        if self.preset:
            fid.write(f'// Preset profile: {self.preset}\n')
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fid.write('// This file was generated on {}\n'.format(time_str))

    def _formatted_tag_and_value(self):
        for tag in WRITE_ORDER:
            value = self.setup_dict[tag]
            value = self._bool_to_string(tag, value)
            yield '{} {}\n'.format(tag, value)

    def _fix_ori_tri(self):
        """
        If TMP is 0, set TRI to 0
        If ACL and MGN are 0, set ORI to 0, BMR to 2, and BMN to 0
        """
        if not self.setup_dict[TEMPERATURE_ENABLED]:
            self.setup_dict[TEMPERATURE_INTERVAL] = 0
        if (not self.setup_dict[ACCELEROMETER_ENABLED]
                and not self.setup_dict[MAGNETOMETER_ENABLED]):
            self.setup_dict[ORIENTATION_INTERVAL] = 0
            self.setup_dict[ORIENTATION_BURST_RATE] = 2
            self.setup_dict[ORIENTATION_BURST_COUNT] = 0

    def _bool_to_string(self, tag, value):
        if tag in TYPE_BOOL:
            return 1 if value is True else 0
        return value
