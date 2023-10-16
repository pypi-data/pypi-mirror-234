import typer
from typer.models import DeveloperExceptionConfig

from datazone.errors.base import DatazoneError

DatazoneExceptionType = "typing.Type[DatazoneError]"


class DatazoneTyper(typer.Typer):
    @staticmethod
    def handle_datazone_error(exc: DatazoneExceptionType):
        from rich import print

        error_message = f":warning: [bold red]{exc.message}[/bold red]"

        if hasattr(exc, "detail"):
            error_message += f" - Exception Detail: {exc.detail}"
        print(error_message)

    def __call__(self, *args, **kwargs):
        try:
            super(DatazoneTyper, self).__call__(*args, **kwargs)
        except DatazoneError as datazone_exception:
            self.handle_datazone_error(datazone_exception)
        except Exception as e:
            setattr(
                e,
                "__typer_developer_exception__",
                DeveloperExceptionConfig(
                    pretty_exceptions_enable=self.pretty_exceptions_enable,
                    pretty_exceptions_show_locals=self.pretty_exceptions_show_locals,
                    pretty_exceptions_short=self.pretty_exceptions_short,
                ),
            )
            raise e
