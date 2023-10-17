"""
Meta sources - sources that read/filter/fold/spindle/mutilate other sources
"""
from typing import Iterable

from .abstract import ConfigSource, CfgDict


class SubsetSource(ConfigSource):
    """
    Returns a sub-namespace of another source.  Useful with MergedConfiguration if you want partial overrides for
    precedence reasons. eg. source A's namespace  'A' should take priority over source B's namspace 'A', but source B's
    namespace 'B' should take priority over source A's namespace 'B'.
    """

    def __init__(self, source: ConfigSource, keys: Iterable[str]):
        self.source = source
        self.keys = set(keys)

    def as_dict(self) -> CfgDict:
        full = self.source.as_dict()
        return {k: v for k, v in full.items() if k in self.keys}


class SubNamepaceSource(ConfigSource):

    def __init__(self, source: ConfigSource, ns: Iterable[str]):
        self.source = source
        self.ns = set(ns)

    def as_dict(self) -> CfgDict:
        result = self.source.as_dict()
        for subns in self.ns:
            if subns in result:
                result = result[subns]
        return result
