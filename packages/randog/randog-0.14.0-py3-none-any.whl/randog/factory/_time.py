import datetime as dt
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ._datetime import DatetimeRandomFactory
from ..exceptions import FactoryConstructionError


def randtime(
    minimum: t.Optional[dt.time] = None,
    maximum: t.Optional[dt.time] = None,
    *,
    tzinfo: t.Union[t.Literal[False], None, dt.tzinfo] = False,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.time]:
    """Return a factory generating random time values.

    Parameters
    ----------
    minimum : time, optional
        the minimum
    maximum : time, optional
        the maximum
    tzinfo : tzinfo | None, optional
        If specified, the tzinfo of result will be fixed to this value
        (False means no specification).
        When it fixes aware datetime to aware, the time is corrected.
        Otherwise, only the tzinfo is changed.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    return TimeRandomFactory(
        minimum,
        maximum,
        fix_timezone=tzinfo is not False,
        fixed_timezone=tzinfo if tzinfo is not False else None,
        rnd=rnd,
    )


class TimeRandomFactory(Factory[dt.time]):
    """factory generating random time values"""

    _random: Random
    _min: dt.time
    _max: dt.time
    _base: Factory[dt.time]

    def __init__(
        self,
        minimum: t.Union[dt.time, None] = None,
        maximum: t.Union[dt.time, None] = None,
        *,
        fix_timezone: bool = False,
        fixed_timezone: t.Optional[dt.tzinfo] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random time values.

        Parameters
        ----------
        minimum : time, optional
            the minimum
        maximum : time, optional
            the maximum
        fix_timezone : bool, default=False
            If it is True, the tzinfo of result is fixed to `fixed_timezone`.
        fixed_timezone : tzinfo, default=None
            If `fix_timezone` is True, the tzinfo of result is fixed to this.
        rnd : Random, optional
            random number generator to be used
        """
        self._random = decide_rnd(rnd)
        self._min, self._max = self._normalize(minimum, maximum)
        self._fix_timezone = fix_timezone
        self._fixed_timezone = fixed_timezone

        if (self._min.tzinfo is None and self._max.tzinfo is not None) or (
            self._min.tzinfo is not None and self._max.tzinfo is None
        ):
            raise FactoryConstructionError(
                "cannot define range for randtime with a naive time and an aware time"
            )

        if self._max >= self._min:
            dummy_date = dt.date(1970, 7, 1)
            min_datetime = dt.datetime.combine(dummy_date, self._min)
            max_datetime = dt.datetime.combine(dummy_date, self._max)
        else:
            dummy_date1 = dt.date(1970, 7, 1)
            dummy_date2 = dt.date(1970, 7, 2)
            min_datetime = dt.datetime.combine(dummy_date1, self._min)
            max_datetime = dt.datetime.combine(dummy_date2, self._max)

        self._base = DatetimeRandomFactory(
            min_datetime,
            max_datetime,
            fix_timezone=fix_timezone,
            fixed_timezone=fixed_timezone,
            rnd=rnd,
        ).post_process(lambda v: v.time().replace(tzinfo=v.tzinfo))

    def _next(self) -> dt.time:
        return self._base.next()

    @classmethod
    def _normalize(
        cls,
        minimum: t.Union[dt.time, None],
        maximum: t.Union[dt.time, None],
    ) -> t.Tuple[dt.time, dt.time]:
        if minimum is not None and maximum is not None:
            return minimum, maximum
        elif minimum is not None:
            return minimum, minimum.replace(hour=(minimum.hour + 1) % 24)
        elif maximum is not None:
            return maximum.replace(hour=(maximum.hour + 23) % 24), maximum
        else:
            return dt.time(0, 0, 0), dt.time(23, 59, 59, 999_999)
