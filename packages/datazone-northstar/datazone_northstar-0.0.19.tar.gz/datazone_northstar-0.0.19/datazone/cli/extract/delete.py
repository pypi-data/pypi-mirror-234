from rich import print

from datazone.service_callers.crud import CrudServiceCaller


def delete(extract_id: str):
    CrudServiceCaller(service_name="job", entity_name="extract").delete_entity(entity_id=extract_id)

    print("Extract has deleted successfully :fire:")
