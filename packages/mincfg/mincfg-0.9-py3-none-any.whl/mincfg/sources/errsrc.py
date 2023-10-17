"""
Fake sources for throwing errors
"""

from .abstract import ConfigSource


def ErrorMessagingSource(msg):
    """
    This is used to allow sources with external dependencies to have a value that
    will throw an error if and only if they're actually used
    """

    class ErrMsgSrc(ConfigSource):
        def __init__(self, *a, **kw):
            raise ValueError(msg)

        def as_dict(self):
            raise ValueError(msg)

    return ErrMsgSrc
