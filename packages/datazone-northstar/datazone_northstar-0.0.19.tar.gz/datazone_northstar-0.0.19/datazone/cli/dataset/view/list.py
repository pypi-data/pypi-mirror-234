from rich.console import Console
from rich.table import Table

from datazone.service_callers.dataset import DatasetServiceCaller

transaction_columns = [
    "ID",
    "Name",
    "Dataset ID",
    "Created At",
    "Created By",
]


def list_func(dataset_id: str):
    response_data = DatasetServiceCaller.get_view_list_by_dataset(dataset_id=dataset_id)

    console = Console()

    table = Table(*transaction_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("name"),
            datum.get("dataset").get("id"),
            datum.get("created_at"),
            datum.get("created_by"),
        ]
        table.add_row(*values)
    console.print(table)
