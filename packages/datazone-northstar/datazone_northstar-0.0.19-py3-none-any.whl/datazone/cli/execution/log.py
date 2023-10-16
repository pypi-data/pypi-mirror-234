import time

from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from datazone.models.common import FINISHED_STATUSES, ExecutionStatus
from datazone.service_callers.job import JobServiceCaller


def fetch_logs(execution_id: str):
    cursor = None
    while True:
        log_response_data = JobServiceCaller.get_execution_logs(execution_id=execution_id, cursor=cursor)
        status = log_response_data.get("status")
        cursor = log_response_data.get("cursor")
        new_logs = log_response_data.get("logs", [])
        if new_logs:
            yield new_logs

        if status in FINISHED_STATUSES:
            break
        time.sleep(1)


def get_status(execution_id: str) -> ExecutionStatus:
    status_response_data = JobServiceCaller.get_execution_status(execution_id=execution_id)
    return status_response_data.get("status")


def log(execution_id: str):
    status = get_status(execution_id)

    while status == ExecutionStatus.CREATED:
        time.sleep(3)
        status = get_status(execution_id)

    if status == ExecutionStatus.WAITING_UPSTREAMS:
        with Progress(
            SpinnerColumn(finished_text="[green]✔[/green]"),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task_1 = progress.add_task(description="Waiting for upstream executions...")
            while not progress.finished:
                status = get_status(execution_id)
                if status != ExecutionStatus.WAITING_UPSTREAMS:
                    progress.update(task_1, advance=100)
                time.sleep(2)

    console = Console()
    logs_table = Table(show_header=True, show_edge=False)
    logs_table.add_column()
    logs_table.add_column("Timestamp")
    logs_table.add_column("Transform")
    logs_table.add_column("Step Key", style="dim")
    logs_table.add_column("Explanation")

    with Live(console=console, screen=False, auto_refresh=False, refresh_per_second=2) as live:
        log_generator = fetch_logs(execution_id=execution_id)
        for log_batch in log_generator:
            for log_data in log_batch:
                log_time = log_data["log_time"]
                event_type = log_data.get("event_type", " - ")
                step_key = log_data.get("step_key") or " - "
                message = log_data['message']
                cause_message = log_data.get('error_cause_message')
                if cause_message is not None:
                    message += f" [bold red]{cause_message}[/bold red]"
                logs_table.add_row(
                    "[green]✔[/green]",
                    f"[bold]{log_time}[/bold]",
                    f"[bold]{step_key}[/bold]",
                    f"{event_type}",
                    message,
                )
            if len(log_batch):
                live.update(logs_table)
                live.refresh()
