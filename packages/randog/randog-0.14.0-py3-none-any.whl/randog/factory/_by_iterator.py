import typing as t

from ._base import Factory

T = t.TypeVar("T")


def by_iterator(iterator: t.Iterator[T]) -> Factory[T]:
    """Return a factory generating values by specified iterator.

    Parameters
    ----------
    iterator : Iterator[T]
        the iterator generating value
    """
    return ByIteratorFactory(iterator)


class ByIteratorFactory(Factory[T]):
    """factory generating values by specified iterator"""

    _iterator: t.Iterator[T]

    def __init__(
        self,
        iterator: t.Iterator[T],
    ):
        """Return a factory generating values by specified iterator.

        Parameters
        ----------
        iterator : Iterator[T]
            the iterator generating value
        """
        self._iterator = iterator

    def _next(self) -> T:
        return next(self._iterator)
