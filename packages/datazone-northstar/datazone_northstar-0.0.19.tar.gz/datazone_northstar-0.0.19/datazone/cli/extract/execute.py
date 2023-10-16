from enum import Enum

from rich import print

from datazone.cli.execution.log import log
from datazone.service_callers.job import JobServiceCaller


class ExecutionTypes(str, Enum):
    ALL = "all"
    SINGLE = "single"
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"


def execute(extract_id: str) -> None:
    """
    Start execution for extract
    """
    response_data = JobServiceCaller.run_execution_extract(extract_id=extract_id)

    _id = response_data.get("_id")
    print(f"[bold blue]Execute ID: {_id}[/bold blue]")

    log(execution_id=_id)
