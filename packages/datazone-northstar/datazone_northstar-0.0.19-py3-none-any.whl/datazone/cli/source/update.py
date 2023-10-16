from typing import Optional, Dict, Any

from rich import print

from datazone.core.common.types import SourceType
from datazone.service_callers.crud import CrudServiceCaller


def update(
    source_id: str,
    name: Optional[str] = None,
    database_type: Optional[SourceType] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database_name: Optional[str] = None,
    schema_name: Optional[str] = None,
):
    connection_parameters = {
        "source_type": "database",
        "database_type": database_type,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database_name": database_name,
        "schema_name": schema_name,
    }
    keys = list(connection_parameters.keys())
    for key in keys:
        value = connection_parameters.get(key)
        if not value:
            connection_parameters.pop(key)

    payload: Dict[str, Any] = {"connection_parameters": connection_parameters}

    if name:
        payload.update({"name": name})

    CrudServiceCaller(service_name="dataset", entity_name="source").update_entity(entity_id=source_id, payload=payload)

    # TODO add test connection mechanism
    print("Source has updated successfully :pencil:")
