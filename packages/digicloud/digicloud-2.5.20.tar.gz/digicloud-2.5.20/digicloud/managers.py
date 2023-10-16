"""
    Managers definition.
"""
import os
import pickle
import sys
from pathlib import Path
from collections import ChainMap

from requests import Session as Sess
from sentry_sdk import capture_message


class ConfigManager():
    """Configuration manager for all configs."""
    FILE_NAME = 'config'
    DEFAULTS = {
        'BASE_URL': os.environ.get('API_BASE_URL', "https://api.digicloud.ir"),
    }

    def __init__(self, app_logger):
        self._log = app_logger
        self._path = self._get_config_path()
        self._states = dict()
        self._load()

    def __getitem__(self, item):
        try:
            return ChainMap(self.DEFAULTS, self._states)[item]
        except KeyError:
            raise KeyError('No "{}" in configuration.'.format(item))

    def __setitem__(self, item, value):
        self._states[item] = value

    def __delitem__(self, item):
        if item in self._states:
            del self._states[item]

    def __contains__(self, item):
        return item in self._states

    def __call__(self):
        return self._states

    def _get_config_path(self):
        """Create config file directory.

        Handles platform dependent path creation for ``FILE_NAME ``,
        and return full path to config file.
        """
        path = {
            'darwin': '$HOME/Library/Application Support/digicloud',
            'win': '%LOCALAPPDATA%/digicloud',
            'linux': '$HOME/.config/digicloud',
        }[sys.platform]

        path = os.path.expandvars(path)

        if not os.path.isdir(path):
            os.makedirs(path, mode=0o755, exist_ok=True)

        full_path = os.path.join(path, self.FILE_NAME)
        Path(full_path).touch()

        return full_path

    def _load(self):
        with open(self._path, 'rb') as file_:
            if os.path.getsize(self._path) > 0:
                self._states = pickle.load(file_)

    def _dump(self):
        with open(self._path, 'wb') as file_:
            pickle.dump(self._states, file_, pickle.HIGHEST_PROTOCOL)

    def get(self, item, default=None):
        """return item from config or default."""
        return self._states.get(item, default)

    def save(self):
        """write configurations to file."""
        self._dump()


class Session(Sess):
    """Custom ``requests.Session`` object model."""

    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url
        super(Session, self).__init__(*args, **kwargs)

    @property
    def user_agent(self):
        return self.headers.get("User-Agent")

    @user_agent.setter
    def user_agent(self, value):
        self.headers["User-Agent"] = value

    def resource(self, uri, method='GET', payload=None, params=None,
                 endpoint_version='/v1'):
        """Resource access helper."""
        url = f'{self.base_url}{endpoint_version}{uri}'
        response = self.request(method, url, params=params, json=payload)
        self.log_to_sentry(response)
        response.raise_for_status()
        if len(response.content):
            return response.json()
        return None

    def get(self, uri, params=None):
        return self.resource(uri, params=params)

    def post(self, uri, payload):
        return self.resource(uri, 'POST', payload)

    def put(self, uri, payload):
        return self.resource(uri, 'PUT', payload)

    def patch(self, uri, payload):
        return self.resource(uri, 'PATCH', payload)

    def delete(self, uri, payload=None):
        return self.resource(uri, 'DELETE', payload)

    def setup(self, config):
        self.base_url = config['BASE_URL']
        if config.get('AUTH_HEADERS'):
            auth_headers = config['AUTH_HEADERS']
            self.headers.update(auth_headers)
        else:
            config['AUTH_HEADERS'] = dict()

    def log_to_sentry(self, response):
        response_time = round(response.elapsed.total_seconds(), 1)
        if response_time > 25:
            capture_message('slow-response: url: {} time: {} seconds'.format(
                response.request.url, response_time
            ))
