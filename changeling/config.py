import copy

import yaml


DEFAULTS = {
    'server.host': '127.0.0.1',
    'server.port': 8080,
    's3.bucket': '3ac5d7b9-c711-4307-bc06-7668b3c26efd-changeling',
}


def _open_config_file(path):
    return open(path, 'r')


def _parse_config_file(fap):
    return yaml.load(fap)


def load(config_path):
    fap = _open_config_file(config_path)
    config = copy.deepcopy(DEFAULTS)
    config.update(_parse_config_file(fap))
    return config
