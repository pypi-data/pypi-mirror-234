from dataclasses import dataclass

from datazone.core.common.types import ExtractMode


@dataclass
class ExtractDefinition:
    name: str
    source_id: str
    source_table: str
    mode: ExtractMode = ExtractMode.OVERWRITE
