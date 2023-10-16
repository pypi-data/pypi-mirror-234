from os import environ as env
from abc import ABC

from datazone.core.connections.config import ConnectionConfig
from datazone.core.connections.session import get_session


class BaseServiceCaller(ABC):
    service_name: str

    @classmethod
    def get_root_url(cls):
        config = ConnectionConfig()
        return config.host

    @classmethod
    def get_service_url(cls):
        service_url = env.get(f"{cls.service_name.upper()}_STATIC_URL")
        if service_url is None:
            service_url = f"{cls.get_root_url()}/{cls.service_name}"

        return service_url

    @classmethod
    def get_session(cls):
        return get_session()


class BaseCrudServiceCaller(ABC):
    service_name: str

    def get_service_url(self):
        service_url = env.get(f"{self.service_name.upper()}_STATIC_URL")
        if service_url is None:
            config = ConnectionConfig()
            service_url = f"{config.host}/{self.service_name}"

        return service_url

    def get_session(self):
        return get_session()
