import typing as t
from random import Random

from ._base import Factory, decide_rnd
from .._utils.nullsafe import dfor
from ..exceptions import FactoryConstructionError

T = t.TypeVar("T", bound=t.Sequence)


def randlist(
    *items: Factory,
    length: t.Union[int, Factory[int], None] = None,
    type: t.Callable[[t.Iterator[t.Any]], T] = list,
    rnd: t.Optional[Random] = None,
    items_list: t.Optional[t.Sequence[Factory]] = None,
) -> Factory[list]:
    """Return a factory generating random list.

    Parameters
    ----------
    items : Factory
        the factories of each item.
        If `items_list` is specified, `items` will be ignored.
    length : int|Factory[int], optional
        length of generated list.
        If not specified,
        the length of generated list will be equals to the number of `items`.
    type : type, default=list
        the type of generated object
    rnd : Random, optional
        random number generator to be used
    items_list : Sequence[Factory], optional
        the factories of each item. Use when positional arguments cannot be specified.

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    if items_list is not None:
        items = items_list

    return ListRandomFactory(items, length=length, type=type, rnd=rnd)


class ListRandomFactory(Factory[list], t.Generic[T]):
    """factory generating random list values"""

    _random: Random
    _length: t.Union[int, Factory[int]]
    _factories: t.Sequence[Factory]
    _type: t.Callable[[t.Iterator[t.Any]], T]

    def __init__(
        self,
        items: t.Sequence[Factory],
        *,
        length: t.Union[int, Factory[int], None] = None,
        type: t.Callable[[t.Iterator[t.Any]], T] = list,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random list values.

        Parameters
        ----------
        items : t.Sequence[Factory]
            the factories of each item
        length : int|Factory[int], optional
            length of generated list.
            If not specified,
            the length of generated list will be equals to the number of `items`.
        type : type, default=list
            the type of generated object
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._length = dfor(length, len(items))
        self._factories = items
        self._type = type

        non_factory_item_indexes = [
            str(i)
            for i, factory in enumerate(self._factories)
            if not isinstance(factory, Factory)
        ]
        if len(non_factory_item_indexes) > 0:
            raise FactoryConstructionError(
                "randlist received non-factory object for item: "
                f"index {', '.join(non_factory_item_indexes)}"
            )

        if isinstance(self._length, Factory) and len(self._factories) == 0:
            raise FactoryConstructionError(
                "the factory of element must be given to randlist() "
                "if length is at random"
            )
        if (
            not isinstance(self._length, Factory)
            and self._length > 0
            and len(self._factories) == 0
        ):
            raise FactoryConstructionError(
                "the factory of element must be given to randlist() "
                "if length is positive"
            )

    def _factory_generator(self, length) -> t.Iterator[Factory]:
        generated = 0
        last_factory = None
        for factory in self._factories:
            if generated >= length:
                return
            yield factory
            last_factory = factory
            generated += 1
        while generated < length:
            yield last_factory
            generated += 1

    def _next_generator(self) -> t.Iterator[t.Any]:
        length = self._next_length()
        return _GeneratedAsIter(self._factory_generator(length))

    def _next_length(self) -> int:
        if isinstance(self._length, Factory):
            return self._length.next()
        else:
            return self._length

    def _next(self) -> T:
        try:
            return self._type(self._next_generator())
        except _StopIterationOfItem:
            raise StopIteration()


class _GeneratedAsIter(t.Iterator[t.Any]):
    _factories_iter: t.Iterator[Factory]

    def __init__(self, factories_iter: t.Iterator[Factory]):
        self._factories_iter = factories_iter

    def __next__(self) -> t.Any:
        factory = next(self._factories_iter)
        try:
            return factory.next()
        except StopIteration:
            raise _StopIterationOfItem()


class _StopIterationOfItem(Exception):
    pass
