from typing import Dict

import typer
from rich import print

from datazone.core.common.types import SourceType
from datazone.service_callers.crud import CrudServiceCaller


def mysql_source_configurations(payload: Dict):
    host = typer.prompt("Host", type=str)
    port = typer.prompt("Port", type=str)
    user = typer.prompt("User", type=str)
    password = typer.prompt("Password", hide_input=True, confirmation_prompt=True, type=str)
    database_name = typer.prompt("Database Name", type=str)
    schema_name = typer.prompt("Schema Name", type=str, default="None")

    # We can't set None value as default, so we are forced to that hackish method.
    schema_name = None if schema_name == "None" else schema_name

    payload["connection_parameters"].update(
        {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database_name": database_name,
            "schema_name": schema_name,
        },
    )

    return payload


def aws_s3_csv_source_configurations(payload: Dict):
    bucket_name: str = typer.prompt("Bucket Name")
    aws_access_key_id: str = typer.prompt("AWS Access Key ID")
    aws_secret_access_key: str = typer.prompt("AWS Secret Access Key", hide_input=True)

    payload["connection_parameters"].update(
        {
            "bucket_name": bucket_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        },
    )
    return payload


source_type_configuration_func_mapping = {
    SourceType.MYSQL: mysql_source_configurations,
    SourceType.AWS_S3_CSV: aws_s3_csv_source_configurations,
}


def create(
    name: str = typer.Option(..., prompt=True),
    source_type: SourceType = typer.Option(..., prompt=True),
):
    payload = {"name": name, "connection_parameters": {"source_type": source_type}}
    func = source_type_configuration_func_mapping[source_type]
    payload = func(payload)

    CrudServiceCaller(service_name="dataset", entity_name="source").create_entity(
        payload=payload,
    )

    # TODO add test connection mechanism
    print("Source has created successfully :tada:")
