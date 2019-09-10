class DeclinationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self.view.refresh)
        self.view.connect(self.changed)

    def changed(self, new_value):
        self.model.declination = new_value

