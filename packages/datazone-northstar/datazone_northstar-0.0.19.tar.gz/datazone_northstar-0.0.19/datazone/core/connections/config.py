import json
from typing import Dict

import keyring

from datazone.constants import Constants
from datazone.errors.auth import MissingConfigurationError


class ConnectionConfig:
    _confs: Dict

    def __init__(self):
        conf = keyring.get_password(Constants.DEFAULT_KEYRING_APP_NAME, "conf")
        if conf is None:
            raise MissingConfigurationError
        self._confs = json.loads(conf)

    @property
    def host(self):
        return self._confs.get("host")

    @property
    def username(self):
        return self._confs.get("username")

    @property
    def password(self):
        return self._confs.get("password")

    @property
    def token_url(self):
        return f"{self.host}/token"
