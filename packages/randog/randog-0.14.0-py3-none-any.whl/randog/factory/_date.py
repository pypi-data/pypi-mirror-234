import datetime as dt
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ..exceptions import FactoryConstructionError


def randdate(
    minimum: t.Union[dt.date, dt.datetime, None] = None,
    maximum: t.Union[dt.date, dt.datetime, None] = None,
    *,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.date]:
    """Return a factory generating random date values.

    Parameters
    ----------
    minimum : date | datetime, optional
        the minimum
    maximum : date | datetime, optional
        the maximum
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return DateRandomFactory(
        minimum,
        maximum,
        rnd=rnd,
    )


class DateRandomFactory(Factory[dt.date]):
    """factory generating random date values"""

    _random: Random
    _min: dt.date
    _max: dt.date
    _range: int

    def __init__(
        self,
        minimum: t.Union[dt.date, dt.datetime, None] = None,
        maximum: t.Union[dt.date, dt.datetime, None] = None,
        *,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random date values.

        Parameters
        ----------
        minimum : date | datetime, optional
            the minimum
        maximum : date | datetime, optional
            the maximum
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._min, self._max = self._normalize(minimum, maximum)

        if self._min > self._max:
            raise FactoryConstructionError("empty range for randdate")

        self._range = (self._max - self._min).days

    def _next(self) -> dt.date:
        relative_days = self._random.randint(0, self._range)
        return self._min + dt.timedelta(days=relative_days)

    @classmethod
    def _normalize(
        cls,
        minimum: t.Union[dt.date, dt.datetime, None] = None,
        maximum: t.Union[dt.date, dt.datetime, None] = None,
    ) -> t.Tuple[dt.date, dt.date]:
        if isinstance(minimum, dt.datetime):
            minimum = minimum.date()
        if isinstance(maximum, dt.datetime):
            maximum = maximum.date()

        if minimum is not None and maximum is not None:
            return minimum, maximum
        elif minimum is not None:
            return minimum, minimum + dt.timedelta(days=364)
        elif maximum is not None:
            return maximum - dt.timedelta(days=364), maximum
        else:
            now = dt.datetime.utcnow().date()
            return now - dt.timedelta(days=182), now + dt.timedelta(hours=182)
