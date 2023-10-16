import typer

from datazone.cli.auth.configure import configure
from datazone.cli.auth.login import login

app = typer.Typer()
app.command()(configure)
app.command()(login)
