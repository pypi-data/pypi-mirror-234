from rich import print

from datazone.service_callers.crud import CrudServiceCaller


def delete(source_id: str):
    CrudServiceCaller(service_name="dataset", entity_name="source").delete_entity(entity_id=source_id)

    print("Source has deleted successfully :fire:")
