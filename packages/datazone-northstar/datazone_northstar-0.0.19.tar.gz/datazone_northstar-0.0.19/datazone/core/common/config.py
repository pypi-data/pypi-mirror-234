import json
import os
from pathlib import Path
from typing import Optional

import yaml
from bson import ObjectId

from datazone.constants import Constants
from datazone.errors.local_errors import FileNotExist
from datazone.models.config import Config, Pipeline


class ConfigReader:
    def __init__(self, config_file_path: Optional[str] = None):
        self.config_file_path = config_file_path or Constants.DEFAULT_CONFIG_FILE_NAME

    def get_config_file_content(self) -> str:
        """Get config file content."""
        with open(self.config_file_path) as f:
            config = f.read()
        return config

    def read_config_file(self) -> Config:
        """
        Read config file and return it as a dictionary.
        Returns:
            config as a Config instance
        """
        config = self.get_config_file_content()
        data = yaml.load(config, Loader=yaml.FullLoader)
        return Config(**data)

    def is_config_file_exist(self) -> bool:
        """Check if config file exist."""
        config_file_path = Path(self.config_file_path)
        return os.path.exists(config_file_path)

    def get_pipeline_id(self, file: str):
        config: Config = self.read_config_file()

        file_path = f"{os.getcwd()}/{file}"

        if not os.path.exists(file):
            raise FileNotExist

        pipeline_id = next(
            (pipeline.id for pipeline in config.pipelines if file_path.endswith(pipeline.path.as_posix())),
            None,
        )

        if pipeline_id is None:
            print("[bold red]File is not saved in config file![/bold red]")
            return

        return pipeline_id

    def add_new_pipeline(self, path: str):
        pipeline_id = ObjectId()

        file = self.read_config_file()
        file.pipelines.append(Pipeline(id=pipeline_id, path=path))

        with open(self.config_file_path, 'w') as fp:
            yaml.dump(json.loads(json.dumps(file.dict(), default=str)), fp, Dumper=yaml.SafeDumper)
