from typing import Optional

from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

history_columns = [
    "ID",
    "Entity Type",
    "Entity ID",
    "Created At",
    "Started At",
    "Finished At",
    "Created By",
    "Run ID",
    "Status",
]


def list_func(pipeline_id: Optional[str] = None, extract_id: Optional[str] = None) -> None:
    params = {}
    if pipeline_id is not None:
        params.update({"pipeline_id": pipeline_id})
    elif extract_id is not None:
        params.update({"extract_id": extract_id})

    response_data = CrudServiceCaller(service_name="job", entity_name="execution").get_entity_list(params=params)

    console = Console()

    table = Table(*history_columns)
    for datum in reversed(response_data):
        values = [
            datum.get("_id"),
            "Extract" if datum.get("extract") is not None else "Pipeline",
            datum.get("pipeline").get("id") if datum.get("pipeline") is not None else datum.get("extract").get("id"),
            datum.get("created_at"),
            datum.get("start_datetime"),
            datum.get("finish_datetime"),
            datum.get("created_by"),
            datum.get("run_id"),
            datum.get("status"),
        ]
        table.add_row(*values)
    console.print(table)
