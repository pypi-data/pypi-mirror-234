from typing import Optional, List, Callable, Dict

from datazone import Dataset
from datazone.context import inspect_mode


class _Transform:
    def __init__(
        self,
        name: str,
        materialized: bool = False,
        input_mapping: Optional[Dict] = None,
        output_mapping: Optional[Dict] = None,
        partition_by: Optional[List[str]] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        self.name = name
        self.materialized = materialized
        self.input_mapping = input_mapping
        self.output_mapping = output_mapping
        self.partition_by = partition_by
        self.description = description
        self.tags = tags

        self._inputs: List = list()

    def __call__(self, original_function: Callable):
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, Dataset) or isinstance(arg, _Transform):
                    self._inputs.append(arg)
            if inspect_mode.get():
                return self

            result = original_function(*args, **kwargs)
            print(f"{self.name} transform executed. Result: {str(result)}")
            return result

        return wrapper
