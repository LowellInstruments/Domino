# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved

import os
from mat.data_converter import DataConverter


class TestConversionManager(object):
    def test_creation(self):
        assert DataConverter("no file")

    def test_conversion(self):
        full_file_path = reference_file("test.lid")
        manager = DataConverter(full_file_path, average=False)
        manager.convert()
        assert_compare_expected_file("test_accelmag.csv")
        assert_compare_expected_file("test_temperature.csv")


def reference_file(file_name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "files",
        file_name)


def assert_compare_expected_file(file_name):
    new_path = reference_file(file_name)
    expected_path = reference_file(file_name + ".expect")
    with open(new_path) as new_file, open(expected_path) as expected_file:
        new_lines = [line.strip() for line in new_file.readlines()]
        expected_lines = [line.strip() for line in expected_file.readlines()]
    os.remove(new_path)
    assert new_lines == expected_lines
