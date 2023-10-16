from typing import Dict, Optional

from datazone.service_callers.base import BaseCrudServiceCaller


class CrudServiceCaller(BaseCrudServiceCaller):
    def __init__(self, service_name: str, entity_name: str):
        self.service_name = service_name
        self.entity_name = entity_name

    def get_entity_with_id(self, entity_id: str) -> Dict:
        response = self.get_session().get(
            f"{self.get_service_url()}/{self.entity_name}/get-by-id/{entity_id}",
        )
        return response.json()

    def get_entity_list(self, params: Optional[Dict] = None):
        session = self.get_session()
        response = session.get(f"{self.get_service_url()}/{self.entity_name}/list", params=params)
        return response.json()

    def create_entity(self, payload: Dict):
        session = self.get_session()
        response = session.post(
            f"{self.get_service_url()}/{self.entity_name}/create",
            json=payload,
        )
        return response.json()

    def delete_entity(self, entity_id: str):
        session = self.get_session()
        session.delete(f"{self.get_service_url()}/{self.entity_name}/delete/{entity_id}")

    def update_entity(self, entity_id: str, payload: Dict):
        session = self.get_session()
        session.put(f"{self.get_service_url()}/{self.entity_name}/update/{entity_id}", json=payload)
