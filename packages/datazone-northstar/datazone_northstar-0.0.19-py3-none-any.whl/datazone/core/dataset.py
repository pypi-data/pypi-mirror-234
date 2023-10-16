from typing import Optional


class Dataset:
    def __init__(self, id: str, run_upstream: bool = False, freshness_duration: Optional[int] = None):
        self._id = id
        self._run_upstream = run_upstream
        self._freshness_duration = freshness_duration
