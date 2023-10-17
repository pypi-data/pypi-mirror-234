import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ..exceptions import FactoryConstructionError


def union(
    *factories: Factory,
    weights: t.Optional[t.Sequence[float]] = None,
    lazy_choice: bool = False,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory generating value by one of specified factories.

    Parameters
    ----------
    factories : Factory
        the factories
    weights : Sequence[float], optional
        the probabilities that each factory is chosen.
        The length must equal to the number of factories.
    lazy_choice : bool, optional
        If it is True, when generating a value,
        first generate values with all factories and then decide which of them to adopt.
        Otherwise, it first decides which factory to adopt,
        and then generates a value using only that factory.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No factories are specified.
    """
    if lazy_choice:
        return UnionRandomLazyChoiceFactory(*factories, weights=weights, rnd=rnd)

    else:
        return UnionRandomFactory(*factories, weights=weights, rnd=rnd)


class UnionRandomFactory(Factory[t.Any]):
    """factory generating value by one of specified factories."""

    _random: Random
    _weights: t.Optional[t.Sequence[float]]
    _factories: t.Sequence[Factory]

    def __init__(
        self,
        *factories: Factory,
        weights: t.Optional[t.Sequence[float]] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating value by one of specified factories.

        Parameters
        ----------
        factories : Factory
            the factories
        weights : Sequence[float], optional
            the probabilities that each factory is chosen.
            The length must equal to the number of factories.
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            No factories are specified.
        """
        self._random = decide_rnd(rnd)
        self._weights = weights
        self._factories = factories

        if len(factories) <= 0:
            raise FactoryConstructionError("no factory is given to union()")
        if self._weights is not None and len(self._weights) != len(self._factories):
            raise FactoryConstructionError(
                "the number of weights must match the factories"
            )

    def _next(self) -> t.Any:
        return self._random.choices(self._factories, self._weights)[0].next()


class UnionRandomLazyChoiceFactory(UnionRandomFactory):
    def _next(self) -> t.Any:
        values = [f.next() for f in self._factories]
        return self._random.choices(values, self._weights)[0]
