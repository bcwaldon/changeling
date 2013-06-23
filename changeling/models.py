import uuid

import jsonschema

import changeling.exception


class Change(object):

    schema = {
        'name': 'change',
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
        'additionalProperties': False,
    }

    def __init__(self, id=None, name=None, description=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description

    @classmethod
    def from_dict(self, data):
        self.validate(data)
        return Change(**data)

    def to_dict(self):
        def _generate_set_attributes():
            for k in Change.schema['properties'].keys():
                val = getattr(self, k)
                if val is not None:
                    yield (k, val)

        return dict(_generate_set_attributes())

    def __str__(self):
        return "<Change id=%s name=%s>" % (self.id, self.name)

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
