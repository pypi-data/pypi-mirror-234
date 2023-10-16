from typing import Dict, Optional


from datazone.constants import Constants
from datazone.service_callers.base import BaseServiceCaller


class RepositoryServiceCaller(BaseServiceCaller):
    service_name = "repo"

    @classmethod
    def get_repository_with_id(cls, id: str) -> Dict:
        session = cls.get_session()
        response = session.get(
            f"{cls.get_service_url()}/repository/get-by-id/{id}",
        )
        return response.json()

    @classmethod
    def create_repository(cls, name: str, description: Optional[str] = None) -> Dict:
        session = cls.get_session()
        response = session.post(
            f"{cls.get_service_url()}/repository/create",
            json={"name": name, "description": description},
        )
        return response.json()

    @classmethod
    def get_default_server(cls) -> Dict:
        session = cls.get_session()
        response = session.get(
            f"{cls.get_service_url()}/server/get-default-server",
        )
        return response.json()

    @classmethod
    def create_session(
        cls,
        server_id: str,
        organisation_name: str,
        repository_name: str,
    ) -> Dict:
        session = cls.get_session()
        response = session.post(
            f"{cls.get_service_url()}/session/create",
            json={
                "server": server_id,
                "organisation": organisation_name,
                "repository": repository_name,
                "expire_duration": Constants.DEFAULT_SESSION_DURATION,
            },
        )
        return response.json()
