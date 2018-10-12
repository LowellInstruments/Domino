import numpy as np
from datetime import datetime
import os
from mat.utils import parse_tags


TYPE_INT = ('BMN', 'BMR', 'ORI', 'TRI', 'PRR', 'PRN')
TYPE_BOOL = ('ACL', 'LED', 'MGN', 'TMP', 'PRS', 'PHD')
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
PRINT_ORDER = ['DFN', 'TMP', 'ACL', 'MGN', 'TRI', 'ORI', 'BMR', 'BMN',
               'STM', 'ETM', 'LED', 'PRS', 'PHD', 'PRR', 'PRN']
INTERVALS = np.array([1, 2, 5, 10, 15, 20, 30, 60,
                      120, 300, 600, 900, 1800, 3600])
INTERVAL_STRING = np.array(['1 second', '2 seconds', '5 seconds', '10 seconds',
                            '15 seconds', '20 seconds', '30 seconds',
                            '1 minute', '2 minutes', '5 minutes', '10 minutes',
                            '15 minutes', '30 minutes', '1 hour'],
                           dtype=object)
BURST_FREQUENCY = np.array([2, 4, 8, 16, 32, 64])
DEFAULT_SETUP = {'DFN': 'untitled.lid', 'TMP': True, 'ACL': True,
                 'MGN': True, 'TRI': 1, 'ORI': 1, 'BMR': 2, 'BMN': 1,
                 'STM': '1970-01-01 00:00:00',
                 'ETM': '4096-01-01 00:00:00',
                 'LED': False, 'PRS': False,
                 'PHD': False, 'PRR': 0, 'PRN': 0}


class SetupFile:
    def __init__(self, setup_dict=None):
        self._setup_dict = setup_dict if setup_dict else DEFAULT_SETUP

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'rb') as fid:
            setup_file_string = fid.read().decode('IBM437')
        setup_file_string = cls._remove_comments(setup_file_string)
        setup_dict = parse_tags(setup_file_string)
        cls._convert_to_type(setup_dict)
        return cls(setup_dict)

    @staticmethod
    def _remove_comments(setup_file_string):
        while setup_file_string.startswith('//'):
            eol = setup_file_string.find('\r\n')
            setup_file_string = setup_file_string[eol+2:]
        return setup_file_string

    @staticmethod
    def _convert_to_type(setup_dict):
        for tag, value in setup_dict.items():
            if tag in TYPE_INT:
                setup_dict[tag] = int(value)
            if tag in TYPE_BOOL:
                setup_dict[tag] = value == '1'

    def available_tri(self):
        """
        Logical array (mask) for self.intervals of available tri intervals
        """
        if self.orient_interval == 0:
            return INTERVALS > 0  # all values are available because orient is disabled

        is_available = np.logical_or(INTERVALS % self._setup_dict['ORI'] == 0,
                                     self._setup_dict['ORI'] % INTERVALS == 0)
        return is_available

    def available_ori(self):
        """
        Logical array (mask) for self.intervals of available ori intervals
        """
        if self.orient_interval == 0:
            return INTERVALS > 0  # all values are available because orient is disabled

        is_available = np.logical_or(INTERVALS % self._setup_dict['TRI'] == 0,
                                     self._setup_dict['TRI'] % INTERVALS == 0)
        return is_available

    @property
    def filename(self):
        return self._setup_dict['DFN']

    @filename.setter
    def filename(self, filename):
        if len(filename) > 15:
            raise ValueError('filename must be 15 characters or less')
        if not filename.endswith('.lid'):
            raise ValueError('filename must end with .lid')
        self._setup_dict['DFN'] = filename

    @property
    def temperature_enabled(self):
        return self._setup_dict['TMP']

    @temperature_enabled.setter
    def temperature_enabled(self, state):
        if type(state) is not bool:
            raise ValueError('Temperature state must be True or False')
        self._setup_dict['TMP'] = state
        # if temperature logging is disabled, set the temperature recording
        # interval to 1 second
        if state is False:
            self._setup_dict['TRI'] = 1

    @property
    def accelerometer_enabled(self):
        return self._setup_dict['ACL']

    @accelerometer_enabled.setter
    def accelerometer_enabled(self, state):
        if type(state) is not bool:
            raise ValueError('Accelerometer state must be True or False')
        self._setup_dict['ACL'] = state
        if not self.orient_enabled:
            self.orient_interval = 1
            self.orient_burst_rate = 2
            self.orient_burst_count = 1

    @property
    def magnetometer_enabled(self):
        return self._setup_dict['MGN']

    @magnetometer_enabled.setter
    def magnetometer_enabled(self, state):
        if type(state) is not bool:
            raise ValueError('Magnetometer state must be True or False')
        self._setup_dict['MGN'] = state
        if not self.orient_enabled:
            self.orient_interval = 1
            self.orient_burst_rate = 2
            self.orient_burst_count = 1

    @property
    def orient_enabled(self):
        return self._setup_dict['ACL'] or self._setup_dict['MGN']

    @property
    def orient_interval(self):
        return self._setup_dict['ORI']

    @orient_interval.setter
    def orient_interval(self, value):
        if value not in INTERVALS[self.available_ori()]:
            raise ValueError('Invalid ORI value')
        # if self._setup_dict['BMN'] > (value * self._setup_dict['BMR']):
        #     raise ValueError('orientation burst count may not exceed orientation interval multiplied by orientation'
        #                      'burst rate')
        self._setup_dict['ORI'] = value

    @property
    def temperature_interval(self):
        return self._setup_dict['TRI']

    @temperature_interval.setter
    def temperature_interval(self, value):
        if value not in INTERVALS[self.available_tri()]:
            raise ValueError('Invalid TRI value')
        self._setup_dict['TRI'] = value

    @property
    def orient_burst_rate(self):
        return self._setup_dict['BMR']

    @orient_burst_rate.setter
    def orient_burst_rate(self, value):
        if value not in [2, 4, 8, 16, 32, 64]:
            raise ValueError('Orient burst rate not supported')
        self._setup_dict['BMR'] = value

    @property
    def orient_burst_count(self):
        return self._setup_dict['BMN']

    @orient_burst_count.setter
    def orient_burst_count(self, value):
        if value > (self._setup_dict['ORI'] * self._setup_dict['BMR']):
            raise ValueError('Burst count must be less than orient interval '
                             'multiplied by orient burst rate.')
        self._setup_dict['BMN'] = value

    @property
    def led_enabled(self):
        return self._setup_dict['LED']

    @led_enabled.setter
    def led_enabled(self, state):
        if type(state) is not bool:
            raise ValueError('Magnetometer state must be True or False')
        self._setup_dict['LED'] = state

    def validate(self):
        pass

    def generate_config_file(self, path=None):
        path = '' if path is None else path
        with open(os.path.join(path, 'MAT.cfg'), 'w', newline='') as out_file:
            out_file.write('// Lowell Instruments LLC - MAT Data Logger - Configuration File\r\n')
            out_file.write('// This file was generated on {}\r\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            for tag in self.PRINT_ORDER:
                if tag in self._setup_dict:
                    value = self._setup_dict[tag]
                    if tag in self.TYPE_BOOL:  # Boolean type needs to be 1 or 0
                        value = 1 if self._setup_dict[tag] is True else 0
                    out_file.write('{} {}\r\n'.format(tag, value))

    def reset(self):
        self.__init__()
