
import changeling.exception


class FakeStorage(object):
    def __init__(self, changes):
        self.changes = [(c['id'], c.to_dict()) for c in changes]

    def list_changes(self):
        return [c[1] for c in self.changes]

    def get_change(self, change_id):
        try:
            return dict(self.changes)[change_id]
        except KeyError:
            raise changeling.exception.ChangeNotFound(change_id)

    def get_change_history(self, change):
        return []
