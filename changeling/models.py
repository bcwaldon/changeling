import uuid


class Change(object):
    def __init__(self, id=None, name=None):
        self.id = id or str(uuid.uuid4())
        self.name = name

    @classmethod
    def from_dict(self, data):
        return Change(data.get('id'), data.get('name'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    def __str__(self):
        return "<Change name='%s'>" % self.name
