

class Change(object):
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(self, data):
        return Change(data['name'])

    def to_dict(self):
        return {'name': self.name}

    def __str__(self):
        return "<Change name='%s'>" % self.name
