import datetime as dt
import math
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ._int import randint
from ..exceptions import FactoryConstructionError

_ZERO = dt.timedelta(0)
_DAY = dt.timedelta(days=1)
_HOUR = dt.timedelta(hours=1)
_MINUTE = dt.timedelta(minutes=1)
_SECOND = dt.timedelta(seconds=1)
_MILLISECOND = dt.timedelta(milliseconds=1)
_MICROSECOND = dt.timedelta(microseconds=1)


_NEXT = {
    _MICROSECOND: _MILLISECOND,
    _MILLISECOND: _SECOND,
    _SECOND: _MINUTE,
    _MINUTE: _HOUR,
    _HOUR: _DAY,
    _DAY: 30 * _DAY,
}


def randtimedelta(
    minimum: t.Optional[dt.timedelta] = None,
    maximum: t.Optional[dt.timedelta] = None,
    *,
    unit: t.Optional[dt.timedelta] = None,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.timedelta]:
    """Return a factory generating random timedelta values.

    Parameters
    ----------
    minimum : timedelta, optional
        the minimum
    maximum : timedelta, optional
        the maximum
    unit : timedelta, optional
        the atomic unit
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return TimedeltaRandomFactory(
        minimum,
        maximum,
        unit=unit,
        rnd=rnd,
    )


class TimedeltaRandomFactory(Factory[dt.timedelta]):
    """factory generating random timedelta values"""

    _random: Random
    _inner_factory: Factory[int]
    _min: dt.timedelta
    _max: dt.timedelta
    _min_by_unit: int
    _max_by_unit: int
    _unit: dt.timedelta

    def __init__(
        self,
        minimum: t.Optional[dt.timedelta] = None,
        maximum: t.Optional[dt.timedelta] = None,
        *,
        unit: t.Optional[dt.timedelta] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random timedelta values.

        Parameters
        ----------
        minimum : timedelta, optional
            the minimum
        maximum : timedelta, optional
            the maximum
        unit : timedelta, optional
            the atomic unit
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        if unit is not None:
            if unit == dt.timedelta(0):
                raise FactoryConstructionError(
                    "the unit for randtimedelta must not be zero"
                )
            if unit < dt.timedelta(0):
                unit = -unit

        self._random = decide_rnd(rnd)
        self._min, self._max, self._unit = self._normalize(minimum, maximum, unit)

        if self._min > self._max:
            raise FactoryConstructionError("empty range for randtimedelta")

        self._min_by_unit = math.ceil(self._min / self._unit)
        self._max_by_unit = math.floor(self._max / self._unit)
        if self._min_by_unit > self._max_by_unit:
            raise FactoryConstructionError("empty range for randtimedelta")
        self._inner_factory = randint(self._min_by_unit, self._max_by_unit, rnd=rnd)

    def _next(self) -> dt.timedelta:
        return self._unit * self._inner_factory.next()

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[dt.timedelta] = None,
        maximum: t.Optional[dt.timedelta] = None,
        unit: t.Optional[dt.timedelta] = None,
    ) -> t.Tuple[dt.timedelta, dt.timedelta, dt.timedelta]:
        if minimum is not None and maximum is not None:
            if unit is None:
                unit = calc_unit(minimum, maximum)
            return minimum, maximum, unit

        elif minimum is not None:
            if unit is None:
                unit = calc_unit(minimum, maximum)
                return minimum, minimum + _NEXT[unit], unit
            else:
                return minimum, minimum + 10 * unit, unit

        elif maximum is not None:
            if unit is None:
                unit = calc_unit(minimum, maximum)
                return maximum - _NEXT[unit], maximum, unit
            else:
                return maximum - 10 * unit, maximum, unit

        else:
            if unit is None:
                return _ZERO, _DAY, _HOUR
            else:
                return _ZERO, _NEXT[unit], unit


def calc_unit(
    *timedelta_list: t.Optional[dt.timedelta], default: dt.timedelta = _DAY
) -> dt.timedelta:
    result = default
    for timedelta in filter(lambda x: x is not None, timedelta_list):
        if timedelta.microseconds != 0:
            if result > _MICROSECOND and timedelta.microseconds % 1000 != 0:
                result = _MICROSECOND
            elif result > _MILLISECOND:
                result = _MILLISECOND
        elif result <= _MILLISECOND:
            continue
        elif timedelta.seconds != 0:
            if result > _SECOND and timedelta.seconds % 60 != 0:
                result = _SECOND
            elif result > _MINUTE and timedelta.seconds % 3600 != 0:
                result = _MINUTE
            elif result > _HOUR:
                result = _HOUR

    return result
