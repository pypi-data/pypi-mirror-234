from typing import Dict, Optional


from datazone.service_callers.base import BaseServiceCaller


class DatasetServiceCaller(BaseServiceCaller):
    service_name = "dataset"

    @classmethod
    def get_transaction_list_by_dataset(cls, dataset_id):
        session = cls.get_session()
        response = session.get(
            f"{cls.get_service_url()}/transaction/list",
            params={"dataset_id": dataset_id},
        )
        return response.json()

    @classmethod
    def get_view_list_by_dataset(cls, dataset_id):
        session = cls.get_session()
        response = session.get(f"{cls.get_service_url()}/view/list-by-dataset-id/{dataset_id}")
        return response.json()

    @classmethod
    def get_sample_data(cls, dataset_id: str, transaction_id: Optional[str] = None) -> Dict:
        params = {}
        if transaction_id:
            params.update({"transaction_id": transaction_id})
        session = cls.get_session()
        response = session.get(f"{cls.get_service_url()}/dataset/get-sample-data/{dataset_id}", params=params)
        return response.json()
