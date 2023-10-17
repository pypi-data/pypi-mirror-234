from pathlib import Path
from typing import Union

from .abstract import ConfigSource, CfgDict

import yaml


class YamlFileSource(ConfigSource):
    """
    A YAML file source of configuration information.
    Note that if the top level of the yaml file is not a dict, it will be set as the value of an empty key.
    """
    def __init__(self, filename: Union[Path, str]):
        self.path = Path(filename) if filename else None

    def as_dict(self) -> CfgDict:
        if self.path is None:
            return dict()
        if not self.path.exists():
            return dict()
        if not self.path.is_file():
            return dict()
        with self.path.open() as f:
            val = yaml.safe_load(f)
        if not isinstance(val, dict):
            val = { '': val }
        return val
