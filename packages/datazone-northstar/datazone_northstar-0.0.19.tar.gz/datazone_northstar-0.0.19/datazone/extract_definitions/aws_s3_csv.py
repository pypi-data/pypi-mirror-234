from abc import abstractmethod

from datazone.extract_definitions.base import BaseExtractDefinition


class AWSS3CsvExtractDefinition(BaseExtractDefinition):

    @property
    @abstractmethod
    def search_prefix(self) -> str:
        ...

    @property
    @abstractmethod
    def search_pattern(self) -> str:
        ...
