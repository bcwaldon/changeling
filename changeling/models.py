import uuid

import jsonschema

import changeling.exception


class Change(object):

    schema = {
        'name': 'change',
        'properties': {
            'id': {
                'type': 'string',
                'pattern': ('^([0-9a-fA-F]){8}-([0-9a-fA-F]){4}'
                            '-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}'
                            '-([0-9a-fA-F]){12}$'),
            },
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'tags': {'type': 'array'},
            'wip': {'type': 'boolean'},
            'approved': {'type': 'boolean'},
        },
        'additionalProperties': False,
    }

    def __init__(self, **kwargs):
        self.attributes = {
            'id': str(uuid.uuid4()),
            'tags': [],
            'wip': False,
            'approved': False,
        }
        self.attributes.update(kwargs)
        self._validate(self.attributes)

    def __getitem__(self, key):
        return self.attributes[key]

    @classmethod
    def from_dict(self, data):
        return Change(**data)

    def to_dict(self):
        def _generate_set_attributes():
            for k in Change.schema['properties'].keys():
                val = self[k]
                if val is not None:
                    yield (k, val)

        return dict(_generate_set_attributes())

    def __str__(self):
        return "<Change id=%s name=%s>" % (self['id'], self['name'])

    @classmethod
    def _validate(cls, data):
        try:
            jsonschema.validate(data, cls.schema)
        except jsonschema.ValidationError as exc:
            raise changeling.exception.ValidationError(exc)
