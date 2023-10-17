from random import Random
import typing as t

from ._base import Factory
from ._choice import randchoice


def const(
    value: t.Any,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory which returns the specified value.

    Parameters
    ----------
    value : Any
        the value
    rnd : Random, optional
        It is not normally used, but it can be accepted as an argument
        to match other Factory construction functions.
    """
    return randchoice(value, rnd=rnd)
