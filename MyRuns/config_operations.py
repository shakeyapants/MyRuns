import yaml
import os
import sys
import platform
from pathlib import Path

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
PROJECT_NAME = 'MyRuns'

if platform.uname().system == 'Windows':
    home = str(Path("%s/%s" % (os.getenv('LOCALAPPDATA'), PROJECT_NAME)))
elif platform.uname().system == 'Linux' or 'Darwin':
    home = str(Path("%s/%s" % (os.getenv('HOME'), PROJECT_NAME)))


class ConfigFile(object):
    def __init__(self, path_to_config, config_name):
        self._path_config = path_to_config
        self.config_name = config_name

    def read_parameter(self, parameter, default=None):
        try:
            with open(os.path.join(self._path_config, self.config_name), 'r') as config:
                try:
                    config = yaml.load(config)
                    return config.get(parameter, default)
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError:
            with open(os.path.join(home, self.config_name), 'w') as config:
                yaml.dump({'MY_STRAVA_CLIENT_ID': '11111', 'MY_STRAVA_SECRET': 'strava_secret',
                           'REDIRECT_URI': 'uri', 'SECRET_KEY': 'secret_key'}, config)
            with open(os.path.join(home, 'config.yaml'), 'r') as config:
                yaml.load(config)
            return 'template config created'

    def write_parameter(self, parameter, value):
        try:
            with open(os.path.join(self._path_config, self.config_name), 'r') as stream:
                config = yaml.load(stream)
                config[parameter] = value
        except FileNotFoundError:
            pass
        with open(os.path.join(self._path_config, self.config_name), 'w') as stream:
            yaml.dump(config, stream, default_flow_style=False)
        return 'parameter updated'

