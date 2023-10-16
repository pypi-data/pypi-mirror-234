from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

schedule_columns = ["ID", "Name", "Draft"]


def list_func():
    response_data = CrudServiceCaller(service_name="job", entity_name="project").get_entity_list()
    console = Console()

    table = Table(*schedule_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("name"),
            "Y" if datum.get("is_draft") else "N",
        ]
        table.add_row(*values)
    console.print(table)
