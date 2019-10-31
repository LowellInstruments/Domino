from gui.gui_utils import is_float
from PyQt5.QtCore import QObject, pyqtSignal


class Declination(QObject):
    update_signal = pyqtSignal()

    def __init__(self, declination=0):
        super().__init__()
        self._declination = declination
        self.error_state = False
        self.enabled = True

    @property
    def declination(self):
        return self._declination

    @declination.setter
    def declination(self, value):
        self._declination = value
        if is_float(value) and -180 <= float(value) <= 180:
            self.error_state = False
        else:
            self.error_state = True
            print('error')
        self.update_signal.emit()

    def declination_value(self):
        """
        use this method to read declination as a float
        """
        try:
            declination = float(self._declination)
        except ValueError:
            declination = 0.0
        return declination

    def set_enabled(self, state):
        self.enabled = state
        self.update_signal.emit()
