from typing import Optional

from rich.console import Console
from rich.table import Table

from datazone.core.common.config import ConfigReader
from datazone.service_callers.job import JobServiceCaller

history_columns = ["ID", "Pipeline Name", "Execution Date", "Created By", "Run ID", "Status"]


def history(extract_id: Optional[str] = None) -> None:
    if extract_id:
        response_data = JobServiceCaller.get_extract_execution_history(extract_id=extract_id)
    else:
        config_file = ConfigReader()
        config = config_file.read_config_file()

        response_data = JobServiceCaller.get_repository_execution_history(repository_id=str(config.repository_id))

    console = Console()

    table = Table(*history_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("pipeline").get("name"),
            datum.get("created_at"),
            datum.get("created_by"),
            datum.get("run_id"),
            datum.get("status"),
        ]
        table.add_row(*values)
    console.print(table)
