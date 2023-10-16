import os
import shutil
from pathlib import Path

import typer

from datazone.cli.repository.template_loader import load_template_files
from datazone.service_callers.crud import CrudServiceCaller
from rich import print


def create(repository_name: str) -> None:
    """
    Create new repository. If project with the same name exists, it will be truncated.
    Args:
        repository_name: name of the project
    """
    path = Path(repository_name)
    if path.exists():
        delete = typer.confirm(
            f"There is {repository_name} folder, it will be truncated. Are you sure?",
        )
        if not delete:
            return

        shutil.rmtree(path)

    os.mkdir(repository_name)

    project = CrudServiceCaller(service_name="job", entity_name="project").create_entity(
        payload={"name": repository_name},
    )
    contents = load_template_files(project)

    for file_name, file_content in contents:
        with open(f"{repository_name}/{file_name}", "w") as f:
            f.write(file_content)

    print(f":point_right: [blue]Go to repository directory: cd {repository_name}/[/blue]")
