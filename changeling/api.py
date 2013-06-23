import changeling.models


class ChangeAPI(object):
    def __init__(self, storage):
        self.storage = storage

    def list(self):
        for change_data in self.storage.list_changes():
            yield changeling.models.Change.from_dict(change_data)

    def get(self, change_id):
        change_data = self.storage.get_change(change_id)
        return changeling.models.Change.from_dict(change_data)

    def new(self, data):
        change = changeling.models.Change.from_dict(data)
        self.save(change)
        return change

    def save(self, change):
        self.storage.save_change(change.to_dict())

    def delete(self, change):
        self.storage.delete_change(change.id)

    @staticmethod
    def schema():
        return changeling.models.Change.schema
