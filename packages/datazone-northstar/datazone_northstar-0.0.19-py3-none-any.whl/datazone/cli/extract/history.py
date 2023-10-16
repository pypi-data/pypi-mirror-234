from rich.console import Console
from rich.table import Table

from datazone.service_callers.job import JobServiceCaller

history_columns = ["ID", "Extract ID", "Execution Date", "Created By", "Run ID", "Status"]


def history(extract_id: str) -> None:
    response_data = JobServiceCaller.get_extract_execution_history(extract_id=extract_id)

    console = Console()

    table = Table(*history_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("extract").get("id"),
            datum.get("created_at"),
            datum.get("created_by"),
            datum.get("run_id"),
            datum.get("status"),
        ]
        table.add_row(*values)
    console.print(table)
