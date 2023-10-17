from .abstract import CfgDict, ConfigSource
from .builtin import DictSource, OSEnvironSource
from .errsrc import ErrorMessagingSource as ErrSrc
from .meta import SubsetSource

__all__ = [ 
    'CfgDict',
    'ConfigSource',
    'DictSource',
    'OSEnvironSource',
    'YamlFileSource',
    'SubsetSource',
    'INIFileSource',
    'DotEnvFileSource',
]

try:
    from .yamlfilesrc import YamlFileSource
except ImportError:
    YamlFileSource = ErrSrc("Using YamlFileSource requires mincfg[yaml] or mincfg[all] be installed") # type: ignore

try:
    from .inifilesrc import INIFileSource
except ImportError:
    INIFileSource = ErrSrc("Using INIFileSource requries mincfg[ini] or mincfg[all] be installed")  # type: ignore

try:
    from .dotenv import DotEnvFileSource
except ImportError:
    DotEnvFileSource = ErrSrc("Using DotEnvFileSource requires mincfg[env] or mincfg[all] be installed")  # type: ignore
