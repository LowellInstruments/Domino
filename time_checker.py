import ntplib
from PyQt5.QtCore import QThread, pyqtSignal


class TimeChecker(QThread):
    time_diff = pyqtSignal(float)
    time_check_error = pyqtSignal(str)

    def run(self):
        try:
            server = ntplib.NTPClient()
            response = server.request('time.google.com', version=3)
            self.time_diff.emit(response.offset)
        except Exception as e:
            print(str(e))
            self.time_check_error.emit(str(e))
