import argparse

import flask

import changeling.api
import changeling.config
import changeling.storage
import changeling.views


APP = flask.Flask('changeling')

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config-file', default='changeling.yaml')
parser.add_argument('--debug', action='store_true', default=False)


def run():
    args = parser.parse_args()

    config = changeling.config.load(args.config_file)
    storage = changeling.storage.Storage(config)
    api = changeling.api.ChangeAPI(storage)

    app = flask.Flask('changeling')
    app.debug = args.debug

    changeling.views.register(app, api)
    app.run()
