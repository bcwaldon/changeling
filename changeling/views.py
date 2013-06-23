import json

def register(app, api):

    @app.route('/changes')
    def list_changes():
        return json.dumps([change.to_dict() for change in api.list()])
