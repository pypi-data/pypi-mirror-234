'''
Sources based on python's built-in libraries.
'''

import os
import logging

from .abstract import ConfigSource, CfgDict

logger = logging.getLogger(__name__)


class DictSource(ConfigSource):
    """
    Uses the supplied dict as a config source.  Useful for defaults.
    """

    def __init__(self, cfg_dict: CfgDict):
        self.cfg = cfg_dict

    def __repr__(self):
        return f'DictSource({self.cfg!r})'

    def as_dict(self) -> CfgDict:
        return self.cfg


class KeySplittingDictSource(ConfigSource):
    """
    Uses a dict whose keys are split into a hierarcy as a config source.
    eg. a = 1, b.c = 2, b.d = 3 => { a:1, b: {c:2, d:3} }
    """

    def __init__(self, cfg_dict_lambda, sep: str, prefix: str):
        self.sep = sep
        self.cfg_dict_lambda = cfg_dict_lambda
        self.prefix: str = prefix.strip(sep).upper()

    def as_dict(self) -> CfgDict:
        result: CfgDict = dict()
        input_dict = self.cfg_dict_lambda()
        logger.debug("KeySplittingDictSource transforming dict %r", input_dict)
        for full_key in input_dict:
            if not full_key.startswith(self.prefix):
                continue
            key_path = full_key.split('_')
            if self.prefix:
                key_path = key_path[1:]
            if not key_path:
                continue
            *ns_list, key = key_path
            logger.debug("KeySplittingDictSource: %s -> %r,%s ", full_key, ns_list, key)
            namespace = result
            for subns in ns_list:
                namespace = namespace.setdefault(subns, dict())
            namespace[key] = input_dict[full_key]
        return result


class OSEnvironSource(KeySplittingDictSource):
    """
    Uses os.environ as a config source, by parsing PREFIXd keys into hierarchical dictionaries, splitting on _
    """

    def __init__(self, prefix: str):
        super().__init__(lambda: os.environ, '_', prefix)
