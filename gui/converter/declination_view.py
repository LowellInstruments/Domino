from gui.gui_utils import show_error


class DeclinationView:
    def __init__(self, line_edit):
        self.line_edit = line_edit

    def refresh(self, model):
        self.line_edit.setText(str(model.declination))
        show_error(self.line_edit, model.error_state)
        self.line_edit.setEnabled(model.enabled)

    def connect(self, slot):
        self.line_edit.textEdited.connect(slot)
