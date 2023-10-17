"""
Abstract source definitions, useful for typing and subclassing
"""

from typing import Any, Dict
from abc import ABC, abstractmethod

# CfgDict = Dict[str, Union[str, 'CfgDict']]  # the correct, recursive type... unsupported by mypy
CfgDict = Dict[str, Any]


class ConfigSource(ABC):

    @abstractmethod
    def as_dict(self) -> CfgDict:
        """
        return a dict containing configuration information from this source.

        NOTE: Errors _MUST_ _NOT_ be raised; in case of error, return as much configuration information as possible.
        An empty dict is acceptable (and expected, in cases where, for instance, the supplied configuration file
        doesn't exist)
        """
        raise NotImplementedError
