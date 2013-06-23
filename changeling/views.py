import json

import flask
from flask import request

import changeling.exception
import changeling.models


def build_response(status, data=None):
    resp = flask.Response(status=status)
    resp.mimetype = 'application/vnd.changeling.v0+json'
    if data is not None:
        resp.data = json.dumps(data)
    return resp


def register(app, api):

    @app.route('/changes', methods=['GET'])
    def list_changes():
        data = [change.to_dict() for change in api.list()]
        return build_response(200, data)

    @app.route('/changes', methods=['POST'])
    def create_change():
        request_data = json.loads(request.data)
        change = changeling.models.Change.from_dict(request_data)
        api.save(change)
        return build_response(201, change.to_dict())

    @app.route('/changes/<change_id>', methods=['GET'])
    def show_change(change_id):
        try:
            change = api.get(change_id)
        except changeling.exception.ChangeNotFound:
            return build_response(404)
        else:
            return build_response(200, change.to_dict())

    @app.route('/changes/<change_id>', methods=['DELETE'])
    def delete_change(change_id):
        try:
            change = api.get(change_id)
            api.delete(change)
        except changeling.exception.ChangeNotFound:
            return build_response(404)
        else:
            return build_response(204)
