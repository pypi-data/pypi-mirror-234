import enum
import numbers
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ..exceptions import FactoryConstructionError


def randchoice(
    *values: t.Any,
    weights: t.Optional[t.Sequence[float]] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory choosing one of values.

    Parameters
    ----------
    values : Any
        the values
    weights : Sequence[float], optional
        the probabilities that each value is chosen.
        The length must equal to the number of values.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No values are specified.
    """
    return ChoiceRandomFactory(values, weights=weights, rnd=rnd)


def randenum(
    enum_cls: t.Type[enum.Enum],
    weights: t.Optional[t.Callable[[t.Any], float]] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[t.Any]:
    """Return a factory choosing one of specified enum.

    Parameters
    ----------
    enum_cls : Type[Enum]
        the enum class
    weights : Callable[[Enum], float], optional
        the probabilities that each value is chosen.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        No values are specified.
    """
    values = [*enum_cls]
    weights_list = [weights(value) for value in values] if weights is not None else None

    # validate weight_list
    if weights_list is not None:
        for weight in weights_list:
            __validate_num(
                weight,
                err_msg="the weights must serve weight for each enum value",
            )

    return ChoiceRandomFactory(values, weights=weights_list, rnd=rnd)


class ChoiceRandomFactory(Factory[t.Any]):
    """factory choosing one of values."""

    _random: Random
    _weights: t.Optional[t.Sequence[float]]
    _values: t.Sequence[t.Any]

    def __init__(
        self,
        values: t.Sequence,
        weights: t.Optional[t.Sequence[float]] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory choosing one of values.

        Parameters
        ----------
        values : Any
            the values
        weights : Sequence[float], optional
            the probabilities that each value is chosen.
            The length must equal to the number of values.
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            No values are specified.
        """
        self._random = decide_rnd(rnd)
        self._weights = weights
        self._values = values

        if len(values) <= 0:
            raise FactoryConstructionError("empty candidate for randchoice")
        if self._weights is not None and len(self._weights) != len(self._values):
            raise FactoryConstructionError(
                "the number of weights must match the candidates"
            )

    def _next(self) -> t.Any:
        return self._random.choices(self._values, self._weights)[0]


def __validate_num(value, *, err_msg) -> numbers.Real:
    if isinstance(value, numbers.Real) and not isinstance(value, bool):
        return value
    else:
        raise FactoryConstructionError(err_msg)
