import changeling.models


class ChangeAPI(object):
    def __init__(self, config, storage):
        self.config = config
        self.storage = storage

    def list(self):
        for change_data in self.storage.list_changes():
            yield changeling.models.Change.from_dict(change_data)

    def save(self, change):
        data = change.to_dict()
        self.storage.save_change(data)
