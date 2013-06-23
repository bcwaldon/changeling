

class FakeStorage(object):
    def __init__(self, changes):
        self.changes = changes

    def list_changes(self):
        return self.changes
