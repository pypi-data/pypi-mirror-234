import json

import keyring
import typer
from rich import print

from datazone.constants import Constants
from datazone.core.connections.auth import AuthService


def configure(
    host: str = typer.Option("app.datazone.co", prompt=True),
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., hide_input=True, confirmation_prompt=True, prompt=True),
):
    configuration = {"host": host, "username": username, "password": password}
    keyring.set_password(Constants.DEFAULT_KEYRING_APP_NAME, "conf", json.dumps(configuration))

    auth = AuthService()
    auth.login()

    print("You logged in successfully :tada:")
