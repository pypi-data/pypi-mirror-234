from datazone.errors.base import DatazoneError


class DatazoneAuthError(DatazoneError):
    message = "Datazone Authentication Error"


class DatazoneServiceError(DatazoneError):
    message = "Datazone Service Error"


class DatazoneServiceNotAccessibleError(DatazoneError):
    message = "Datazone Service is not accessible."
