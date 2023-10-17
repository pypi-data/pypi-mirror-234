import string
import typing as t
from random import Random

from .._base import Factory, decide_rnd
from ..._utils.nullsafe import dfor
from ...exceptions import FactoryConstructionError


@t.overload
def randstr(
    *,
    length: t.Union[int, Factory[int], None] = None,
    charset: t.Optional[str] = None,
    regex: None = None,
    rnd: t.Optional[Random] = None,
) -> Factory[str]:
    pass


@t.overload
def randstr(
    *,
    length: None = None,
    charset: None = None,
    regex: t.Union[str, t.Pattern],
    rnd: t.Optional[Random] = None,
) -> Factory[str]:
    pass


def randstr(
    *,
    length: t.Union[int, Factory[int], None] = None,
    charset: t.Optional[str] = None,
    regex: t.Optional[str] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[str]:
    """Return a factory generating random str values.

    Parameters
    ----------
    length : int|Factory[int], default=8
        length of generated string
    charset : str, optional
        characters to be used
    regex : str, optional
        regular expression for generated string.
        It cannot be used with `length` or `charset`.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    if regex is not None and (length is not None or charset is not None):
        raise FactoryConstructionError(
            "cannot specify argument 'regex' for randstr() with 'length' or 'charset'"
        )

    if regex is not None:
        try:
            from ._regex import StrRegexRandomFactory
        except ImportError:
            raise FactoryConstructionError(
                "package 'rstr' must be installed to specify 'regex' to randstr()"
            )
        return StrRegexRandomFactory(regex=regex, rnd=rnd)
    else:
        return StrRandomFactory(length=length, charset=charset, rnd=rnd)


class StrRandomFactory(Factory[str]):
    """factory generating random int values"""

    _random: Random
    _length: t.Union[int, Factory[int]]
    _charset: str

    def __init__(
        self,
        *,
        length: t.Union[int, Factory[int], None] = None,
        charset: t.Optional[str] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random str values.

        Parameters
        ----------
        length : int|Factory[int], default=8
            length of generated string
        charset : str, optional
            characters to be used
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._length = dfor(length, 8)
        self._charset = dfor(charset, string.ascii_letters + string.digits)

        if isinstance(self._length, Factory) and len(self._charset) == 0:
            raise FactoryConstructionError(
                "the charset for randstr() must not be empty if length is at random"
            )
        if (
            not isinstance(self._length, Factory)
            and self._length > 0
            and len(self._charset) == 0
        ):
            raise FactoryConstructionError(
                "the charset for randstr() must not be empty if length is positive"
            )

    def _next(self) -> str:
        length = self._next_length()
        return "".join(self._random.choices(self._charset, k=length))

    def _next_length(self) -> int:
        if isinstance(self._length, Factory):
            return self._length.next()
        else:
            return self._length
