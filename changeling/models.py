import uuid

import jsonschema

import changeling.exception


class Change(object):

    schema = {
        'name': 'change',
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
        },
        'additionalProperties': False,
    }

    def __init__(self, id=None, name=None):
        self.id = id or str(uuid.uuid4())
        self.name = name

    @classmethod
    def from_dict(self, data):
        self.validate(data)
        return Change(data.get('id'), data.get('name'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    def __str__(self):
        return "<Change name='%s'>" % self.name

    @classmethod
    def validate(cls, data):
        try:
            jsonschema.validate(data, cls.schema)
        except jsonschema.ValidationError as exc:
            raise changeling.exception.ValidationError(exc)

    def is_valid(self):
        try:
            self.validate(self.to_dict())
        except changeling.exception.ValidationError:
            return False
        else:
            return True
