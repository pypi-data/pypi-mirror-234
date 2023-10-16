from typing import Optional

from rich import print

from datazone.service_callers.crud import CrudServiceCaller
from datazone.utils.helpers import initialize_git_repo, create_path


def create_repository(name: str, repository_name: str) -> None:
    create_path(path=name, change_directory=True)
    initialize_git_repo(repository_name=repository_name)

    print("[green]Repository is ready.[/green]:rocket:")
    print(f":point_right: [blue]Go to directory: cd {name}/[/blue]")


def clone(project_id: Optional[str] = None, source_id: Optional[str] = None) -> None:
    if (project_id is None and source_id is None) or (project_id is not None and source_id is not None):
        print("[bold red]Project id or source id required![/bold red]")
        return

    if project_id is not None:
        project = CrudServiceCaller(service_name="job", entity_name="project").get_entity_with_id(entity_id=project_id)
        create_repository(name=project.get("name"), repository_name=project.get("repository_name"))
    elif source_id is not None:
        source = CrudServiceCaller(service_name="dataset", entity_name="source").get_entity_with_id(entity_id=source_id)
        create_repository(name=source.get("name"), repository_name=source.get("repository_name"))
