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
from setup_file.setup_file import SetupFile

"""
Sample temperature every 60 seconds. Sample Accelerometer and Magnetomer at 16 Hz for 10 seconds every 60 seconds.
Logger will begin recording when started and will cease recording when manually stopped.
File size: 125.5 MB / month
"""


class DescriptionGenerator:
    def __init__(self, model):
        self.model = model  # type: SetupFile

    def description(self):
        output = self.sample_description() + '\n'
        output += self.start_stop_description() + '\n'
        output += self.file_size_description()
        return output

    def sample_description(self):
        return self.temperature_description() + self.orient_description()

    def temperature_description(self):
        if self.model.value(TEMPERATURE_ENABLED):
            seconds = self._interval_to_string(
                self.model.value(TEMPERATURE_INTERVAL))
            return 'Sample temperature every {}. '.format(seconds)
        else:
            return 'Do not sample temperature. '

    def orient_description(self):
        interval = self._interval_to_string(
            self.model.value(ORIENTATION_INTERVAL))
        rate = str(self.model.value(ORIENTATION_BURST_RATE)) + ' Hz'
        output = self._active_channels()
        if self.model.value(ORIENTATION_BURST_COUNT) == 1:
            output += 'a single time every {}'.format(interval)
        elif self.model.is_continuous:
            output += 'continuously at {}.'.format(rate)
        else:
            seconds = (self.model.value(ORIENTATION_BURST_COUNT)
                       // self.model.value(ORIENTATION_BURST_RATE))
            plural = 's' if seconds > 1 else ''
            output += 'at {} for {} second{} '.format(rate, seconds, plural)
            output += 'every {}.'.format(interval)
        return output

    def _active_channels(self):
        if not self.model.orient_enabled():
            return 'Do not sample accelerometer and magnetometer.'
        output = 'Sample '
        is_accel = self.model.value(ACCELEROMETER_ENABLED)
        is_mag = self.model.value(MAGNETOMETER_ENABLED)
        if is_accel:
            output += 'accelerometer '
        if is_accel and is_mag:
            output += 'and '
        if is_mag:
            output += 'magnetometer '
        return output

    def start_stop_description(self):
        output = ''
        mapping = [('Begin recording ', 'started', START_TIME),
                   ('Stop recording ', 'stopped', END_TIME)]
        for preface, verb, tag in mapping:
            output += preface
            if self.model.value(tag) == DEFAULT_SETUP[tag]:
                output += 'when manually {}. '.format(verb)
            else:
                output += '{}. '.format(self.model.value(tag))
        return output

    def file_size_description(self):
        return 'File size TBD'

    def _interval_to_string(self, seconds):
        index = list(INTERVALS).index(seconds)
        return INTERVAL_STRING[index]
