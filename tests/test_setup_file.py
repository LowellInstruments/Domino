from pathlib import Path
from setup_file.setup_file import (
    SetupFile,
    DEFAULT_SETUP
)


def reference_file(file_name):
    file_path = Path(__file__)
    return file_path.parent / 'files' / file_name


class TestSetupFile:
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
        setup = SetupFile.load_from_file(reference_file('MAT.cfg'))
        assert setup._setup_dict == expected
