from datazone.core.connections.auth import AuthService
from rich import print


def login():
    auth = AuthService()
    auth.login()

    print("You logged in successfully :tada:")
