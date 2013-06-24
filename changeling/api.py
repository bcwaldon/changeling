import changeling.models


class UnauthenticatedChangeAPI(object):
    def __init__(self, storage):
        self.storage = storage

    def list(self):
        for change_data in self.storage.list_changes():
            try:
                yield changeling.models.Change.from_dict(change_data)
            except changeling.exception.ValidationError:
                #TODO(bcwaldon): Log the offending object so it can
                # be removed from the datastore
                continue

    def get(self, change_id):
        change_data = self.storage.get_change(change_id)
        return changeling.models.Change.from_dict(change_data)

    def new(self, data):
        change = changeling.models.Change.from_dict(data)
        self.save(change)
        return change

    def save(self, change):
        data = change.to_dict()
        self.storage.save_change(data['id'], data)

    def delete(self, change):
        self.storage.delete_change(change['id'])

    @staticmethod
    def schema():
        return changeling.models.Change.schema


class AuthenticatedChangeAPI(UnauthenticatedChangeAPI):
    def __init__(self, storage, user):
        super(AuthenticatedChangeAPI, self).__init__(storage)
        self.user = user

    def new(self, data):
        data['owner'] = self.user
        change = changeling.models.Change.from_dict(data)
        self.save(change)
        return change


def change_api_factory(storage, user=None):
    if user is None:
        return UnauthenticatedChangeAPI(storage)
    else:
        return AuthenticatedChangeAPI(storage, user)


class AuthAPI(object):
    def __init__(self):
        pass

    def get_user_by_key(self, key):
        #NOTE(bcwaldon): We don't have *real* authentication yet, so we assume
        # the key is an identifying token for now
        user = key

        return user


def auth_api_factory():
    return AuthAPI()
