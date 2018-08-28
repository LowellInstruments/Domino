# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved

from converter.conversion_manager import ConversionManager

class TestConversionManager(object):
    def test_creation(self):
        assert ConversionManager("no file")
