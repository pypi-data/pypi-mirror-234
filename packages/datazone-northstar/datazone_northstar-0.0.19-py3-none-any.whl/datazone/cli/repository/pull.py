import git
from rich import print

from datazone.utils.helpers import is_git_repo


def pull() -> None:
    if not is_git_repo():
        print("[bold red]Repository is not exist in current directory![/bold red]")
        return

    repo = git.Repo()
    origin = repo.remotes.origin

    origin.pull()
    print("[green]Repository is up to date.[/green]:rocket:")
