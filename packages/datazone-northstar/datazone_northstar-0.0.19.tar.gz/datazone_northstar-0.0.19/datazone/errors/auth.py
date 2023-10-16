from datazone.errors.base import DatazoneError


class MissingConfigurationError(DatazoneError):
    message = "You should auth your profile first! Run command: `datazone auth`"
