from pathlib import Path
from typing import Union

from dotenv import dotenv_values  # type: ignore

from .builtin import KeySplittingDictSource


class DotEnvFileSource(KeySplittingDictSource):
    """
    A .env-file source of configuration information
    """
    def __init__(self, filename: Union[Path, str], prefix=None):
        key_prefix = '' if prefix is None else prefix        
        super().__init__(lambda: dotenv_values(str(filename)), '_', key_prefix)
