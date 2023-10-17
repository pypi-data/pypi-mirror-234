import typing as t
from dataclasses import dataclass
from random import Random

from ._base import Factory, decide_rnd
from ..exceptions import FactoryConstructionError

_item_tuple = t.Tuple[Factory, float]


@dataclass
class DictItem:
    """
    A rule for generating values corresponding to a key in the random generation of
    dict.
    """

    factory: Factory
    """a factory to generate values"""

    prop_exists: float
    """probability of key generation"""

    @t.overload
    def __init__(self, factory: Factory):
        ...

    @t.overload
    def __init__(self, factory: Factory, prop_exists: float):
        ...

    @t.overload
    def __init__(self, item: _item_tuple):
        ...

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Factory):
            self.prop_exists = 1.0
            self.factory = args[0]
        elif len(args) == 1 and isinstance(args[0], tuple):
            self.prop_exists = args[0][1]
            self.factory = args[0][0]
        elif len(args) == 2:
            self.factory = args[0]
            self.prop_exists = args[1]
        else:
            raise DictItemValueError()


class DictItemValueError(ValueError):
    pass


def randdict(
    items_dict: t.Optional[
        t.Mapping[t.Hashable, t.Union[Factory, _item_tuple, DictItem]]
    ] = None,
    *,
    rnd: t.Optional[Random] = None,
    **items: t.Union[Factory, _item_tuple, DictItem],
) -> Factory[dict]:
    """Return a factory generating random dict.

    Parameters
    ----------
    items : Mapping
        the factories of each key.
        If `items_dict` is specified, `items` will be ignored.
    items_dict: Mapping
        the factories of each key. Use when keyword arguments cannot be specified.
    rnd : Random, optional
        random number generator to be used
    """
    if items_dict is not None:
        items = items_dict

    items_normalized = {}
    non_factory_item_keys = []
    for key, value in items.items():
        try:
            items_normalized[key] = (
                value if isinstance(value, DictItem) else DictItem(value)
            )
        except DictItemValueError:
            non_factory_item_keys.append(str(key))
    if len(non_factory_item_keys) > 0:
        raise FactoryConstructionError(
            "randdict received non-factory object for item: "
            f"{', '.join(non_factory_item_keys)}"
        )

    return DictRandomFactory(items_normalized, rnd=rnd)


class DictRandomFactory(Factory[dict]):
    """factory generating random dict"""

    _random: Random
    _items: t.Mapping[t.Hashable, DictItem]

    def __init__(
        self,
        items: t.Mapping[t.Hashable, DictItem],
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random dict.

        Parameters
        ----------
        items : Mapping
            the factories of each key
        rnd : Random, optional
            random number generator to be used
        """
        self._random = decide_rnd(rnd)
        self._items = items

    def _next(self) -> dict:
        result = {}

        for key, cond in self._items.items():
            if self._random.random() < cond.prop_exists:
                result[key] = cond.factory.next()

        return result
