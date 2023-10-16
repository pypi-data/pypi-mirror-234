from typing import List, Optional

from pydantic import BaseModel, FilePath, Field

from datazone.utils.types import PydanticObjectId


class Spec(BaseModel):
    cpu: Optional[str]
    memory: Optional[str]


class SparkExecutorSpec(BaseModel):
    memory: Optional[str]
    cpu: Optional[str]
    instances: Optional[int]


class Resources(BaseModel):
    requests: Optional[Spec]
    limits: Optional[Spec]


class SparkConfig(BaseModel):
    executor: Optional[SparkExecutorSpec]
    driver: Optional[Spec]
    deploy_mode: Optional[str] = "local"


class Pipeline(BaseModel):
    id: PydanticObjectId
    name: Optional[str]
    path: FilePath
    resources: Optional[Resources]
    spark_config: Optional[SparkConfig]


class Config(BaseModel):
    project_name: str
    project_id: PydanticObjectId
    pipelines: List[Pipeline] = Field(default_factory=list)
