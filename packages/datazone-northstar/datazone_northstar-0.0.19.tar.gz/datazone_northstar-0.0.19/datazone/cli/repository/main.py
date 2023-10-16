import typer

from datazone.cli.repository.create import create
from datazone.cli.repository.deploy import deploy
from datazone.cli.repository.summary import summary
from datazone.cli.repository.list import list_func
from datazone.cli.repository.clone import clone
from datazone.cli.repository.pull import pull

app = typer.Typer()
app.command()(create)
app.command()(deploy)
app.command()(summary)
app.command(name="list")(list_func)
app.command()(clone)
app.command()(pull)
