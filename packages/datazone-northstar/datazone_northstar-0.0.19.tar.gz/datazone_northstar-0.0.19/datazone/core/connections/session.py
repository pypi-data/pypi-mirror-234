import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

from datazone.core.connections.auth import AuthService
from os import environ as env

from datazone.errors.common import DatazoneServiceError, DatazoneServiceNotAccessibleError, DatazoneAuthError

AUTH_DISABLED = env.get("AUTH_DISABLED", "false") == "true"


UNKNOWN_ERROR_MESSAGE = "Unknown Service Error"


class CustomHTTPAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        try:
            response = super().send(request, **kwargs)
            response.raise_for_status()
            return response
        except RequestException as e:
            if e.response is not None:
                error = e.response.json()
                if error is not None:
                    # Auth exception control
                    if "error" in error and error["error"] == "invalid_grant":
                        raise DatazoneAuthError(detail=error)
                    else:
                        _kwargs = {"message": error["message"] if "message" in error else UNKNOWN_ERROR_MESSAGE}
                        if "detail" in error:
                            _kwargs["detail"] = error["detail"]
                        raise DatazoneServiceError(**_kwargs)
            raise DatazoneServiceNotAccessibleError


adapter = CustomHTTPAdapter()


def get_session():
    if AUTH_DISABLED:
        session = requests.Session()
    else:
        auth = AuthService()
        session = auth.get_session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
