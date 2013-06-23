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


def build_error_response(status, message=None):
    envelope = {'message': message}
    return build_response(status, envelope)


def parse_json_request():
    mimetypes = [
        'application/json',
        'application/vnd.changeling+json',
        'application/vnd.changeling.v0+json',
    ]
    if not request.headers.get('content-type') in mimetypes:
        joined = ', '.join(mimetypes)
        msg = 'Expected Content-Type header to be one of %s' % joined
        raise ValueError(msg)

    try:
        return json.loads(request.data)
    except (ValueError, TypeError) as exc:
        raise ValueError('Unable to parse JSON: %s' % exc)


def register(app, api):

    @app.route('/schemas/change', methods=['GET'])
    def schema():
        return build_response(200, api.schema())

    @app.route('/changes', methods=['GET'])
    def list_changes():
        data = [change.to_dict() for change in api.list()]
        return build_response(200, data)

    @app.route('/changes', methods=['POST'])
    def create_change():
        try:
            data = parse_json_request()
        except ValueError as exc:
            return build_error_response(400, str(exc))

        #NOTE(bcwaldon): id should be generated by the underlying API
        if 'id' in data:
            data.pop('id')

        try:
            change = api.new(data)
        except changeling.exception.ValidationError:
            return build_error_response(400, 'Invalid change entity')
        else:
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
