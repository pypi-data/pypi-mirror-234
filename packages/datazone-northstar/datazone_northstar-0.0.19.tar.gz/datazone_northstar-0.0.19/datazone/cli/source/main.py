import typer

from datazone.cli.source.create import create
from datazone.cli.source.list import list_func
from datazone.cli.source.delete import delete
from datazone.cli.source.update import update

app = typer.Typer()
app.command()(create)
app.command(name="list")(list_func)
app.command()(delete)
app.command()(update)
