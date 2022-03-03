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
import pytest
import os


def file(file_name):
    return Path(__file__).parent / 'files' / file_name


@pytest.fixture
def setup():
    return SetupFile()


def test_creation():
    assert SetupFile()


def test_default_dict():
    setup = SetupFile()
    assert setup._setup_dict == DEFAULT_SETUP


def test_load_setup_file():
    expected = {'DFN': 'Calibrate.lid', 'TMP': True, 'ACL': True,
                'MGN': True, 'TRI': 1, 'ORI': 1, 'BMR': 64, 'BMN': 64,
                'STM': '1970-01-01 00:00:00',
                'ETM': '4096-01-01 00:00:00',
                'LED': True}
    setup = load_setup_file(file('example_MAT.cfg'))
    assert setup._setup_dict == expected


def test_available_temperature_intervals(setup):
    expected = array([15, 30, 60, 120, 300, 600, 900, 1800, 3600])
    setup.set_interval(ORIENTATION_INTERVAL, 15)
    temp_intervals = INTERVALS[
        setup.available_intervals(TEMPERATURE_INTERVAL)]
    assert array_equal(temp_intervals, expected)


def test_available_orientation_intervals(setup):
    expected = array([1, 5, 15, 30, 60, 120, 300, 600, 900, 1800, 3600])
    setup.set_interval(ORIENTATION_INTERVAL, 15)
    setup.set_interval(TEMPERATURE_INTERVAL, 15)
    orient_intervals = INTERVALS[
        setup.available_intervals(ORIENTATION_INTERVAL)]
    assert array_equal(orient_intervals, expected)


def test_unknown_sensor(setup):
    with pytest.raises(ValueError):
        setup.available_intervals('Kryptonite')


def test_set_filename(setup):
    setup.set_filename('test.lid')
    assert setup.value(FILE_NAME) == 'test.lid'


def test_file_name_too_long(setup):
    with pytest.raises(ValueError):
        setup.set_filename('a_very_long_file_name.lid')


def test_disable_temperature(setup):
    setup.set_channel_enabled(TEMPERATURE_ENABLED, False)
    assert setup.value(TEMPERATURE_ENABLED) is False


def test_bad_bool_value(setup):
    with pytest.raises(ValueError):
        setup.set_channel_enabled(MAGNETOMETER_ENABLED, 1)


def test_set_invalid_orient_interval(setup):
    setup.set_interval(ORIENTATION_INTERVAL, 1)
    setup.set_interval(TEMPERATURE_INTERVAL, 10)
    with pytest.raises(ValueError):
        setup.set_interval(ORIENTATION_INTERVAL, 15)


def test_set_invalid_temperature_interval(setup):
    setup.set_interval(ORIENTATION_INTERVAL, 15)
    with pytest.raises(ValueError):
        setup.set_interval(TEMPERATURE_INTERVAL, 10)


def test_invalid_burst_rate(setup):
    with pytest.raises(ValueError):
        setup.set_orient_burst_rate(15)


def test_enable_led(setup):
    setup.set_channel_enabled(LED_ENABLED, False)
    assert setup.value(LED_ENABLED) is False


def test_change_start_time(setup):
    assert setup.value(START_TIME) == '1970-01-01 00:00:00'
    start_time = '2018-10-15 14:20:00'
    setup.set_time(START_TIME, start_time)
    assert setup.value(START_TIME) == start_time


def test_end_time_before_start_time(setup):
    start_time = '2018-10-15 14:20:00'
    setup.set_time(START_TIME, start_time)
    end_time = '2018-10-15 00:00:00'
    with pytest.raises(ValueError):
        setup.set_time(END_TIME, end_time)


def test_wrong_date_format(setup):
    with pytest.raises(ValueError):
        setup.set_time(START_TIME, '2018/10/15 14:20:00')


def test_major_interval_bytes(setup):
    bytes = setup.major_interval_bytes()
    assert bytes == 1924


def test_major_interval_bytes_no_mag(setup):
    setup.set_channel_enabled(MAGNETOMETER_ENABLED, False)
    bytes = setup.major_interval_bytes()
    assert bytes == 964


def test_orient_enabled(setup):
    assert setup.orient_enabled() is True
    setup.set_channel_enabled(MAGNETOMETER_ENABLED, False)
    assert setup.orient_enabled() is True
    setup.set_channel_enabled(ACCELEROMETER_ENABLED, False)
    assert setup.orient_enabled() is False


def test_temperature_interval_override(setup):
    # TRI shouldn't ever be > ORI. If ORI is set > TRI, increase TRI to match
    assert setup.value(TEMPERATURE_INTERVAL) == 60
    assert setup.value(ORIENTATION_INTERVAL) == 60
    # now increase ORI to be > TRI
    setup.set_interval(ORIENTATION_INTERVAL, 120)
    assert setup.value(TEMPERATURE_INTERVAL) == 120
    assert setup.value(ORIENTATION_INTERVAL) == 120


def test_save_and_load_round_trip(setup, tmp_path):
    path = tmp_path / 'MAT.cfg'
    # change from default
    setup.set_interval(ORIENTATION_INTERVAL, 1)
    setup.set_orient_burst_rate(4)
    setup.write_file(path)
    new_file = load_setup_file(path)
    assert setup._setup_dict == new_file._setup_dict


def test_disabled_temperature_adjustments_on_save(setup, tmp_path):
    """
    If TMP is 0, set TRI to 0
    """
    path = tmp_path / 'MAT.cfg'
    setup.set_channel_enabled(TEMPERATURE_ENABLED, False)
    setup.write_file(path)
    new_file = load_setup_file(path)
    assert new_file._setup_dict[TEMPERATURE_INTERVAL] == 0


def test_disabled_orient_adjustments_on_save(setup, tmp_path):
    """
    If ACL and MGN are 0, set ORI to 0, BMR to 2, and BMN to 0
    """
    path = tmp_path / 'MAT.cfg'
    # change from default
    setup.set_channel_enabled(ACCELEROMETER_ENABLED, False)
    setup.set_channel_enabled(MAGNETOMETER_ENABLED, False)
    setup.write_file(path)
    new_file = load_setup_file(path)
    assert new_file._setup_dict[ORIENTATION_INTERVAL] == 0
    assert new_file._setup_dict[ORIENTATION_BURST_RATE] == 2
    assert new_file._setup_dict[ORIENTATION_BURST_COUNT] == 0