from typing import Dict

import typer
from rich import print

from datazone.core.common.types import ExtractMode, SourceType
from datazone.service_callers.crud import CrudServiceCaller


def mysql_source_parameters(payload: Dict):
    mode = payload.get("mode")
    if mode == "append":
        replication_key = typer.prompt("Replication Key", type=str, default="id")
        payload.update({"replication_key": replication_key})

    table_name: str = typer.prompt("Table Name")
    payload.update({"source_parameters": {"table_name": table_name}})

    return payload


def aws_s3_csv_source_parameters(payload: Dict):
    search_prefix: str = typer.prompt("Search Prefix", default="/")
    search_pattern: str = typer.prompt("Search Pattern", default=".*\\.csv")

    payload.update({"source_parameters": {"search_prefix": search_prefix, "search_pattern": search_pattern}})
    return payload


source_type_parameter_func_mapping = {
    SourceType.MYSQL: mysql_source_parameters,
    SourceType.AWS_S3_CSV: aws_s3_csv_source_parameters,
}


def check_source(source_id: str) -> Dict:
    print("[bold blue]Checking source instance...[/bold blue]")
    source = CrudServiceCaller(service_name="dataset", entity_name="source").get_entity_with_id(entity_id=source_id)
    return source


def create(
    name: str = typer.Option(..., prompt=True),
    source_id: str = typer.Option(..., prompt=True),
    mode: ExtractMode = typer.Option(ExtractMode.OVERWRITE, prompt=True),
):
    source = check_source(source_id=source_id)
    source_type = source.get("connection_parameters").get("source_type")

    func = source_type_parameter_func_mapping[source_type]
    payload = {
        "name": name,
        "mode": mode,
        "source_id": source_id,
    }
    payload = func(payload)
    CrudServiceCaller(service_name="job", entity_name="extract").create_entity(payload=payload)

    print("[bold green]Extract has created successfully [/bold green] :tada:")
