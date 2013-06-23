import argparse

import flask

import changeling.api
import changeling.config
import changeling.storage
import changeling.views


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config-file', default='changeling.yaml')
parser.add_argument('--debug', action='store_true', default=False)
parser.add_argument('--host', default=None)
parser.add_argument('--port', default=None, type=int)


def run_gunicorn(config_file):
    app = flask.Flask('changeling')

    config = changeling.config.load(config_file)
    storage = changeling.storage.StorageFactory(config)
    api = changeling.api.ChangeAPI(storage)

    changeling.views.register(app, api)

    return app


def run():
    args = parser.parse_args()

    config = changeling.config.load(args.config_file)
    storage = changeling.storage.StorageFactory(config)
    api = changeling.api.ChangeAPI(storage)

    app = flask.Flask('changeling')
    app.debug = args.debug

    changeling.views.register(app, api)
    app.run(host=args.host or config['server.host'],
            port=args.port or config['server.port'])
