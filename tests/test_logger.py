# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved

import logging
from converter.logger import log_to_stdout

class TestLogger(object):
    def test_log_to_stdout(self):
        handler_count = len(logging.getLogger().handlers)
        log_to_stdout()  # Action
        assert logging.getLogger().level == logging.DEBUG
        assert len(logging.getLogger().handlers) > handler_count
