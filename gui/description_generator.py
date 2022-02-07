from setup_file.setup_file import (
    DEFAULT_SETUP,
    INTERVALS,
    INTERVAL_STRING,
    ORIENTATION_BURST_COUNT,
    ORIENTATION_BURST_RATE,
    TEMPERATURE_INTERVAL,
    ORIENTATION_INTERVAL,
    ACCELEROMETER_ENABLED,
    MAGNETOMETER_ENABLED,
    TEMPERATURE_ENABLED,
    START_TIME,
    END_TIME,
    INTERVAL_START,
    PRESSURE_BURST_COUNT,
    PRESSURE_ENABLED,
    PRESSURE_BURST_RATE
)
from setup_file.setup_file import SetupFile
from mat.utils import epoch_from_timestamp


"""
Sample temperature every 60 seconds. Sample Accelerometer and Magnetometer at 
16 Hz for 10 seconds every 60 seconds.
Logger will begin recording when started and will cease recording when 
manually stopped.
File size: 125.5 MB / month
"""


SECONDS_PER_MONTH = 60*60*24*30


class DescriptionGenerator:
    def __init__(self, model):
        self.model = model  # type: SetupFile

    def description(self):
        output = self.sample_description() + '\n'
        output += self.start_stop_description() + '\n'
        output += self.file_size_description()
        return output

    def sample_description(self):
        return self.temperature_description() \
               + self.orient_description() \
               + self.pressure_description()

    def temperature_description(self):
        if self.model.value(TEMPERATURE_ENABLED):
            seconds = self._interval_to_string(
                self.model.value(TEMPERATURE_INTERVAL))
            return 'Sample temperature every {}. '.format(seconds)
        else:
            return 'Do not sample temperature. '

    def orient_description(self):
        if not self.model.orient_enabled():
            return 'Do not sample accelerometer and magnetometer. '
        return f'Sample {self._active_channels()} {self._orient_duration_rate()}. '

    def pressure_description(self):
        if self.model.value(PRESSURE_ENABLED):
            return f'Sample pressure {self._pressure_duration_rate()}.'
        else:
            return 'Do not sample pressure. '

    def _active_channels(self):
        output = ''
        is_accel = self.model.value(ACCELEROMETER_ENABLED)
        is_mag = self.model.value(MAGNETOMETER_ENABLED)
        if is_accel:
            output += 'accelerometer '
        if is_accel and is_mag:
            output += 'and '
        if is_mag:
            output += 'magnetometer '
        return output.strip()

    def _orient_duration_rate(self):
        interval = self._interval_to_string(
            self.model.value(ORIENTATION_INTERVAL))
        rate = str(self.model.value(ORIENTATION_BURST_RATE)) + ' Hz'
        if self.model.value(ORIENTATION_BURST_COUNT) == 1:
            output = 'a single time every {}'.format(interval)
        else:
            seconds = (self.model.value(ORIENTATION_BURST_COUNT)
                       // self.model.value(ORIENTATION_BURST_RATE))
            plural = 's' if seconds > 1 else ''
            output = 'at {} for {} second{} '.format(rate, seconds, plural)
            output += 'every {}'.format(interval)
        return output

    def _pressure_duration_rate(self):
        interval = self._interval_to_string(
            self.model.value(ORIENTATION_INTERVAL))
        rate = str(self.model.value(ORIENTATION_BURST_RATE)) + ' Hz'
        if self.model.value(PRESSURE_BURST_COUNT) == 1:
            output = 'a single time every {}'.format(interval)
        else:
            seconds = (self.model.value(PRESSURE_BURST_COUNT)
                       // self.model.value(ORIENTATION_BURST_RATE))
            plural = 's' if seconds > 1 else ''
            output = 'at {} for {} second{} '.format(rate, seconds, plural)
            output += 'every {}'.format(interval)
        return output

    def start_stop_description(self):
        interval_start = {
            'ON_INT_MIN': 'on the next minute. ',
            'ON_INT_QHR': 'on the next quarter hour. ',
            'ON_INT-1HR': 'on the next hour. '
        }
        output = ''
        mapping = [('Start recording ', 'started', START_TIME),
                   ('Stop recording ', 'stopped', END_TIME)]
        for preface, verb, tag in mapping:
            output += preface
            if self.model.value(tag) == DEFAULT_SETUP[tag]:
                output += 'when manually {}. '.format(verb)
            elif self.model.value(tag) in interval_start.keys():
                output += interval_start[self.model.value(tag)]
            else:
                output += '{}. '.format(self.model.value(tag))
        return output

    def file_size_description(self):
        chan_count = 0
        chan_count += 3 if self.model.value(ACCELEROMETER_ENABLED) else 0
        chan_count += 3 if self.model.value(MAGNETOMETER_ENABLED) else 0
        pressure = 1 if self.model.value(PRESSURE_ENABLED) else 0
        burst_count = self.model.value(ORIENTATION_BURST_COUNT)
        orient_interval = self.model.value(ORIENTATION_INTERVAL)
        # *_bytes are in bytes/second
        orient_bytes = (burst_count*chan_count*2)/orient_interval
        pressure_burst_count = self.model.value(PRESSURE_BURST_COUNT)
        pressure_bytes = (pressure_burst_count * pressure * 2) / orient_interval
        temp = 1 if self.model.value(TEMPERATURE_ENABLED) else 0
        temp_interval = self.model.value(TEMPERATURE_INTERVAL)
        temp_bytes = (temp*2)/temp_interval
        bytes_per_sec = orient_bytes + pressure_bytes + temp_bytes
        run_time, suffix = self._get_run_time()
        mb_per_month = (bytes_per_sec * run_time)/(1024**2)
        return 'File size: {:0.1f} MB{}'.format(mb_per_month, suffix)

    def _get_run_time(self):
        if (self.model.value(START_TIME) == DEFAULT_SETUP[START_TIME] or
                self.model.value(END_TIME) == DEFAULT_SETUP[END_TIME] or
                self.model.value(START_TIME) in INTERVAL_START):
            return SECONDS_PER_MONTH, ' per month.'
        else:
            start_seconds = epoch_from_timestamp(self.model.value(START_TIME))
            end_seconds = epoch_from_timestamp(self.model.value(END_TIME))
            return end_seconds - start_seconds, '.'

    def _interval_to_string(self, seconds):
        index = list(INTERVALS).index(seconds)
        return INTERVAL_STRING[index]
