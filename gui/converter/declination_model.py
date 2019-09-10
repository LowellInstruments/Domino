from gui.gui_utils import is_float


class Declination:
    def __init__(self, declination='0'):
        self._declination = declination
        self.error_state = False
        self.enabled = True
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    @property
    def declination(self):
        return self._declination

    @declination.setter
    def declination(self, value):
        if is_float(value) and -180 <= float(value) <= 180:
            self.error_state = False
        else:
            self.error_state = True
        self._declination = value
        self.notify_observers()

    def set_enabled(self, state):
        self.enabled = state
        self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer(self)
