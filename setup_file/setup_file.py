from datetime import datetime
from mat.utils import parse_tags
from numpy import array, logical_or, logical_and
from pathlib import Path
from re import compile, search
from setup_file.utils import date_string_to_datetime


TYPE_INT = ('BMN', 'BMR', 'ORI', 'TRI', 'PRR', 'PRN')
TYPE_BOOL = ('ACL', 'LED', 'MGN', 'TMP', 'PRS', 'PHD')
WRITE_ORDER = ['DFN', 'TMP', 'ACL', 'MGN', 'TRI', 'ORI', 'BMR', 'BMN',
               'STM', 'ETM', 'LED', 'PRS', 'PHD', 'PRR', 'PRN']
INTERVALS = array([1, 2, 5, 10, 15, 20, 30, 60,
                   120, 300, 600, 900, 1800, 3600])
INTERVAL_STRING = array(['1 second', '2 seconds', '5 seconds', '10 seconds',
                         '15 seconds', '20 seconds', '30 seconds',
                         '1 minute', '2 minutes', '5 minutes', '10 minutes',
                         '15 minutes', '30 minutes', '1 hour'],
                        dtype=object)
BURST_FREQUENCY = array([2, 4, 8, 16, 32, 64])
DEFAULT_SETUP = {'DFN': 'untitled.lid', 'TMP': True, 'ACL': True,
                 'MGN': True, 'TRI': 1, 'ORI': 1, 'BMR': 16, 'BMN': 16,
                 'STM': '1970-01-01 00:00:00',
                 'ETM': '2096-01-01 00:00:00',
                 'LED': False, 'PRS': False,
                 'PHD': False, 'PRR': 0, 'PRN': 0}
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


class ObservableDict(dict):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.observers = []

    def set_observer(self, observer_fnc):
        self.observers.append(observer_fnc)

    def update_observers(self, key, value):
        for observer in self.observers:
            observer(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.update_observers(key, value)


class SetupFile:
    def __init__(self, setup_dict=None):
        setup_dict = setup_dict or dict(DEFAULT_SETUP)
        self._setup_dict = ObservableDict(setup_dict)
        self.time_re = compile('^[0-9$]{4}-[0-1][0-9]-[0-3][0-9] '
                               '[0-1][0-9]:[0-6][0-9]:[0-6][0-9]$')
        self.is_continuous = True
        self.is_start_time = False
        self.is_end_time = False

    def set_observer(self, observer_fcn):
        self._setup_dict.set_observer(observer_fcn)

    def value(self, tag):
        return self._setup_dict[tag]

    def available_intervals(self, sensor):
        """
        Available orientation and temperature intervals must be calculated
        in coordination with each other.
        Logical array (mask) of available orientation or temperature intervals
        """
        if sensor not in ['temperature', 'orientation']:
            raise ValueError('Unknown sensor {}'.format(sensor))
        opposite_interval = self._opposite_interval(sensor)
        if sensor is 'temperature':
            return logical_and(self._factors_and_multiples(opposite_interval),
                               INTERVALS >= opposite_interval)
        return self._factors_and_multiples(opposite_interval)

    def _opposite_interval(self, sensor):
        if sensor is 'orientation':
            return self.value(TEMPERATURE_INTERVAL)
        return self.value(ORIENTATION_INTERVAL)

    def _factors_and_multiples(self, interval):
        return logical_or(INTERVALS % interval == 0,
                          interval % INTERVALS == 0)

    def set_filename(self, filename):
        if not search(r'^[a-zA-Z0-9_\-]{1,11}\.lid$', filename):
            raise ValueError('Filename error')
        self._setup_dict[FILE_NAME] = filename

    def set_channel_enabled(self, sensor, state):
        self._confirm_bool(state)
        self._setup_dict[sensor] = state

    def _set_accelmag_enabled(self, sensor, state):
        self._confirm_bool(state)
        self._setup_dict[sensor] = state

    def orient_enabled(self):
        return (self.value(ACCELEROMETER_ENABLED) or
                self.value(MAGNETOMETER_ENABLED))

    def set_orient_interval(self, value):
        if value not in INTERVALS[self.available_intervals('orientation')]:
            raise ValueError('Invalid orientation interval value')
        max_burst_count = value * self.value(ORIENTATION_BURST_RATE)
        if self.value(ORIENTATION_BURST_COUNT) > max_burst_count:
            self.set_orient_burst_count(max_burst_count)
        self._setup_dict[ORIENTATION_INTERVAL] = value
        if value > self.value(TEMPERATURE_INTERVAL):
            self.set_temperature_interval(value)

    def set_temperature_interval(self, value):
        if value not in INTERVALS[self.available_intervals('temperature')]:
            raise ValueError('Invalid temperature interval value')
        self._setup_dict[TEMPERATURE_INTERVAL] = value

    def set_orient_burst_rate(self, value):
        if value not in BURST_FREQUENCY:
            raise ValueError('Invalid burst rate')
        self._setup_dict[ORIENTATION_BURST_RATE] = value

    def set_orient_burst_count(self, value):
        max_burst_count = (self.value(ORIENTATION_INTERVAL) *
                           self.value(ORIENTATION_BURST_RATE))
        if value > max_burst_count:
            raise ValueError('Burst count must be <= orient interval '
                             'multiplied by orient burst rate.')
        self._setup_dict[ORIENTATION_BURST_COUNT] = value

    def set_time(self, occasion, time):
        if occasion not in [START_TIME, END_TIME]:
            raise ValueError('position must be STM or ETM')
        if not self.time_re.search(time):
            raise ValueError('Incorrectly formatted time string')
        old_value = self.value(occasion)
        self._setup_dict[occasion] = time
        if not self._check_time():
            self._setup_dict[occasion] = old_value
            raise ValueError('start time and end time must be in '
                             'correct order')

    def _check_time(self):
        start_time = date_string_to_datetime(self.value(START_TIME))
        end_time = date_string_to_datetime(self.value(END_TIME))
        if end_time <= start_time:
            return False
        return True

    def _confirm_bool(self, state):
        if type(state) is not bool:
            raise ValueError('State must be True or False')

    def write_file(self, directory):
        file_writer = ConfigFileWriter(directory, self._setup_dict)
        file_writer.write_file()


class ConfigFileWriter:
    def __init__(self, directory, setup_dict):
        self.directory = directory
        self.setup_dict = setup_dict

    def write_file(self):
        directory = Path(self.directory or '')
        with open(directory / 'MAT.cfg', 'w', newline='\r\n') as fid:
            self._write_header(fid)
            for line in self._formatted_tag_and_value():
                fid.write(line)

    def _write_header(self, fid):
        fid.write('// Lowell Instruments LLC - MAT Data Logger - '
                  'Configuration File\n')
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fid.write('// This file was generated on {}\n'.format(time_str))

    def _formatted_tag_and_value(self):
        for tag in WRITE_ORDER:
            value = self.setup_dict[tag]
            value = self._bool_to_string(tag, value)
            yield '{} {}\n'.format(tag, value)

    def _bool_to_string(self, tag, value):
        if tag in TYPE_BOOL:
            return 1 if value is True else 0
        return value
