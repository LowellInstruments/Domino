from numpy import array, array_equal
from pathlib import Path
from setup_file.setup_file import (
    SetupFile,
    load_setup_file,
    INTERVALS,
    DEFAULT_SETUP,
    FILE_NAME,
    TEMPERATURE_ENABLED,
    ORIENTATION_INTERVAL,
    ORIENTATION_BURST_RATE,
    ORIENTATION_BURST_COUNT,
    ACCELEROMETER_ENABLED,
    MAGNETOMETER_ENABLED,
    LED_ENABLED,
    TEMPERATURE_INTERVAL,
    START_TIME,
    END_TIME
)
from unittest import TestCase


def reference_file(file_name):
    return files_directory() / file_name


def files_directory():
    return Path(__file__).parent / 'files'


class TestSetupFile(TestCase):
    def test_creation(self):
        assert SetupFile()

    def test_default_dict(self):
        setup = SetupFile()
        assert setup._setup_dict == DEFAULT_SETUP

    def test_load_setup_file(self):
        expected = {'DFN': 'Calibrate.lid', 'TMP': True, 'ACL': True,
                    'MGN': True, 'TRI': 1, 'ORI': 1, 'BMR': 64, 'BMN': 64,
                    'STM': '1970-01-01 00:00:00',
                    'ETM': '4096-01-01 00:00:00',
                    'LED': True}
        setup = load_setup_file(reference_file('example_MAT.cfg'))
        assert setup._setup_dict == expected

    def test_available_temperature_intervals(self):
        expected = array([15, 30, 60, 120, 300, 600, 900, 1800, 3600])
        setup = SetupFile()
        setup.set_interval(ORIENTATION_INTERVAL, 15)
        temp_intervals = INTERVALS[
            setup.available_intervals(TEMPERATURE_INTERVAL)]
        assert array_equal(temp_intervals, expected)

    def test_available_orientation_intervals(self):
        expected = array([1, 5, 15, 30, 60, 120, 300, 600, 900, 1800, 3600])
        setup = SetupFile()
        setup.set_interval(ORIENTATION_INTERVAL, 15)
        orient_intervals = INTERVALS[
            setup.available_intervals(ORIENTATION_INTERVAL)]
        assert array_equal(orient_intervals, expected)

    def test_unknown_sensor(self):
        setup = SetupFile()
        with self.assertRaises(ValueError):
            setup.available_intervals('oxygen')

    def test_set_filename(self):
        setup = SetupFile()
        setup.set_filename('test.lid')
        assert setup.value(FILE_NAME) == 'test.lid'

    def test_file_name_too_long(self):
        setup = SetupFile()
        with self.assertRaises(ValueError):
            setup.set_filename('a_very_long_file_name.lid')

    def test_disable_temperature(self):
        setup = SetupFile()
        setup.set_channel_enabled(TEMPERATURE_ENABLED, False)
        assert setup.value(TEMPERATURE_ENABLED) is False

    def test_bad_bool_value(self):
        setup = SetupFile()
        with self.assertRaises(ValueError):
            setup.set_channel_enabled(MAGNETOMETER_ENABLED, 1)

    def test_set_invalid_orient_interval(self):
        setup = SetupFile()
        setup.set_interval(TEMPERATURE_INTERVAL, 10)
        with self.assertRaises(ValueError):
            setup.set_interval(ORIENTATION_INTERVAL, 15)

    def test_set_invalid_temperature_interval(self):
        setup = SetupFile()
        setup.set_interval(ORIENTATION_INTERVAL, 15)
        with self.assertRaises(ValueError):
            setup.set_interval(TEMPERATURE_INTERVAL, 10)

    def test_invalid_burst_rate(self):
        setup = SetupFile()
        with self.assertRaises(ValueError):
            setup.set_orient_burst_rate(15)

    def test_too_large_orient_burst_count(self):
        setup = SetupFile()
        setup.set_interval(ORIENTATION_INTERVAL, 1)
        setup.set_orient_burst_rate(16)
        with self.assertRaises(ValueError):
            setup.set_orient_burst_count(17)

    def test_enable_led(self):
        setup = SetupFile()
        setup.set_channel_enabled(LED_ENABLED, False)
        assert setup.value(LED_ENABLED) is False

    def test_save_default_setup(self):
        setup = SetupFile()
        setup.write_file(files_directory())
        setup = load_setup_file(reference_file('MAT.cfg'))
        assert setup._setup_dict == DEFAULT_SETUP
        reference_file('MAT.cfg').unlink()

    def test_change_start_time(self):
        setup = SetupFile()
        assert setup.value(START_TIME) == '1970-01-01 00:00:00'
        start_time = '2018-10-15 14:20:00'
        setup.set_time(START_TIME, start_time)
        assert setup.value(START_TIME) == start_time

    def test_end_time_before_start_time(self):
        setup = SetupFile()
        start_time = '2018-10-15 14:20:00'
        setup.set_time(START_TIME, start_time)
        end_time = '2018-10-15 00:00:00'
        with self.assertRaises(ValueError):
            setup.set_time(END_TIME, end_time)

    def test_unknown_time_position(self):
        setup = SetupFile()
        with self.assertRaises(ValueError):
            setup.set_time('middle', '2018-10-15 14:20:00')

    def test_wrong_date_format(self):
        setup = SetupFile()
        with self.assertRaises(ValueError):
            setup.set_time(START_TIME, '2018/10/15 14:20:00')
