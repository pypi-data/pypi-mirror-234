from typing import Optional

from rich.console import Console
from rich.table import Table
from rich import print
from datazone.service_callers.dataset import DatasetServiceCaller


def show(dataset_id: str, branch_name: str = "master", size: int = 10, transaction_id: Optional[str] = None) -> None:
    """
    Show dataset sample data. It fetches sample data from dataset service and prints out as rich table
    Args:
        dataset_id (str): dataset id
        branch_name (str): data branch name
        size (int): table size
        transaction_id (Optional[str]): specific transaction id
    """
    response_data = DatasetServiceCaller.get_sample_data(dataset_id=dataset_id, transaction_id=transaction_id)

    if len(response_data) == 0:
        print("[bold orange]No data[/bold orange]")

    data = response_data[:size]
    columns = data[0].keys()

    console = Console()

    table = Table(*columns)
    for datum in data:
        values = [str(value) for value in datum.values()]
        table.add_row(*values)
    console.print(table)
