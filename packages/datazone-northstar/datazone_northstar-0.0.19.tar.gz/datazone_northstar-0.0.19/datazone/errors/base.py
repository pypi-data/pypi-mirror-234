from typing import Optional, Dict


class DatazoneError(Exception):
    message = "Datazone Error"

    def __init__(self, message: Optional[str] = None, detail: Optional[Dict] = None):
        super().__init__()
        if message:
            self.message = message
        self.detail = detail
