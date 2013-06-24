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



def _get_app(config):
    storage = changeling.storage.StorageFactory(config)
    change_api_factory = changeling.api.change_api_factory
    auth_api_factory = changeling.api.auth_api_factory

    app = flask.Flask('changeling')
    changeling.views.register(
        app, storage, change_api_factory, auth_api_factory)

    app.debug = config['logging.level'].lower() == 'debug'

    return app


def build_app_from_config_file(config_file):
    config = changeling.config.load(config_file)
    return _get_app(config)


def run():
    args = parser.parse_args()
    config = changeling.config.load(args.config_file)
    config['logging.level'] = 'debug' if args.debug else 'info'

    app = _get_app(config)
    app.run(host=args.host or config['server.host'],
            port=args.port or config['server.port'])
