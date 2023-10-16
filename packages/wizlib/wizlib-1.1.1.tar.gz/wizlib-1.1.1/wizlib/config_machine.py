from argparse import Namespace
from pathlib import Path
import os
from dataclasses import dataclass
from unittest.mock import patch

from yaml import load
from yaml import Loader


@dataclass
class ConfigMachine:
    """
    Anything with a config - meant to be subclassed. Can be used with multiple
    inheritance. Assumes that its subclass is a dataclass defining the required
    attributes.

    Attributes:

    appname - The name of the config file, environment variable, etc. - meant
    to be populated as a class attribute (though can also be passed to init)

    config - Path to a config file. Meant to be populated in the init method.
    """

    appname = ''
    config: str = None

    @property
    def config_yaml(self):
        if hasattr(self, '_config_yaml'):
            return self._config_yaml
        if hasattr(self, 'config') and (val := self.config):
            path = Path(val)
        elif (envvar := self.env(self.appname + '-config')):
            path = Path(envvar)
        elif ((localpath := Path.cwd() / f".{self.appname}.yml").is_file()):
            path = localpath
        elif ((homepath := Path.home() / f".{self.appname}.yml").is_file()):
            path = homepath
        else:
            path = None
        if path:
            with open(path) as file:
                self._config_yaml = load(file, Loader=Loader)
                return self._config_yaml

    @staticmethod
    def env(name):
        if (envvar := name.upper().replace('-', '_')) in os.environ:
            return os.environ[envvar]

    def config_get(self, key: str):
        attr = key.replace('-', '_')
        if hasattr(self, attr) and (result := getattr(self, attr)):
            return result
        if (result := self.env(key)):
            return result
        if (yaml := self.config_yaml):
            split = key.split('-')
            while (val := split.pop(0)) and (val in yaml):
                yaml = yaml[val] if val in yaml else None
                if not split:
                    return yaml

    @classmethod
    def add_app_args(self, parser):
        """Allows a Command class to also inherit from ConfigMachine. List
        ConfigMachine first."""
        parser.add_argument('--config', action='store')


def nohome_test():  # pragma: nocover
    """Fake out a ConfigMachine so that it thinks test/files is the home
    directory. This way it's not tempted to pull real configuration."""
    return patch('pathlib.Path.home', lambda: Path('test/files'))


def patchconfig_test(**kwargs):  # pragma: nocover
    """Hand testable config data to a test method."""
    methodpath = 'wizlib.config_machine.ConfigMachine.config_get'

    def configpatch(self, key):
        key = key.replace('-', '_')
        return kwargs[key] if (key in kwargs) else None
    return patch(methodpath, configpatch)
