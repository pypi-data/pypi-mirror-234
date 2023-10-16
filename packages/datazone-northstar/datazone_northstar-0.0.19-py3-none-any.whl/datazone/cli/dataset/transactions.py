from rich.console import Console
from rich.table import Table

from datazone.service_callers.dataset import DatasetServiceCaller

transaction_columns = [
    "ID",
    "Version",
    "Operation",
    "Mode",
    "Number Files",
    "Output Bytes",
    "Output Rows",
    "Transaction ID",
    "Timestamp",
]


def transactions(dataset_id: str):
    response_data = DatasetServiceCaller.get_transaction_list_by_dataset(dataset_id=dataset_id)

    console = Console()

    table = Table(*transaction_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            str(datum.get("version")),
            datum.get("operation"),
            datum.get("mode"),
            str(datum.get("operation_metrics").get("number_files")),
            str(datum.get("operation_metrics").get("number_output_bytes")),
            str(datum.get("operation_metrics").get("number_output_rows")),
            datum.get("transaction_id"),
            datum.get("timestamp"),
        ]
        table.add_row(*values)
    console.print(table)
