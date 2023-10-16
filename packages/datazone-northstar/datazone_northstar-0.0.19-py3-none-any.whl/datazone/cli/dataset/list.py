from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

extract_columns = ["ID", "Name", "Storage Path", "Created At"]


def list_func():
    response_data = CrudServiceCaller(service_name="dataset", entity_name="dataset").get_entity_list()

    console = Console()

    table = Table(*extract_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("name"),
            datum.get("storage_path"),
            datum.get("created_at"),
        ]
        table.add_row(*values)
    console.print(table)
