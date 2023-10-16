from abc import abstractmethod

from datazone.extract_definitions.base import BaseExtractDefinition


class MysqlExtractDefinition(BaseExtractDefinition):
    @property
    @abstractmethod
    def table_name(self):
        ...
