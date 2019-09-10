class TableController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        model.add_observer(self.view.refresh)

    # slot
    def delete_selected_rows(self):
        row_objects = self.view.selectionModel().selectedRows()
        for row in row_objects:
            self.model.delete(row.row())

    # slot
    def clear(self):
        if len(self.model) == 0:
            return
        self.model.clear()

    def refresh(self):
        self.model.notify_observers()
