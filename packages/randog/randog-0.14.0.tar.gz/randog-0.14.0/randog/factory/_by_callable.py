import typing as t

from ._base import Factory

T = t.TypeVar("T")


def by_callable(func: t.Callable[[], T]) -> Factory[T]:
    """Return a factory generating values by specified callable.

    Parameters
    ----------
    func : () -> T
        the function generating value
    """
    return ByCallableFactory(func)


class ByCallableFactory(Factory[T]):
    """factory generating values by specified callable"""

    _callable: t.Callable[[], T]

    def __init__(
        self,
        func: t.Callable[[], T],
    ):
        """Return a factory generating values by specified callable.

        Parameters
        ----------
        func : () -> T
            the function generating value
        """
        self._callable = func

    def _next(self) -> T:
        return self._callable()
