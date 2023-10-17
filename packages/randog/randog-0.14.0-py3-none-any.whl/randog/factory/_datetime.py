import datetime as dt
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from ..exceptions import FactoryConstructionError


def randdatetime(
    minimum: t.Union[dt.datetime, dt.date, None] = None,
    maximum: t.Union[dt.datetime, dt.date, None] = None,
    *,
    tzinfo: t.Union[t.Literal[False], None, dt.tzinfo] = False,
    rnd: t.Optional[Random] = None,
) -> Factory[dt.datetime]:
    """Return a factory generating random datetime values.

    Parameters
    ----------
    minimum : datetime | date, optional
        the minimum
    maximum : datetime | date, optional
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
    return DatetimeRandomFactory(
        minimum,
        maximum,
        fix_timezone=tzinfo is not False,
        fixed_timezone=tzinfo if tzinfo is not False else None,
        rnd=rnd,
    )


class DatetimeRandomFactory(Factory[dt.datetime]):
    """factory generating random datetime values"""

    _random: Random
    _min: dt.datetime
    _max: dt.datetime
    _range: dt.timedelta
    _fix_timezone: bool
    _fixed_timezone: t.Optional[dt.tzinfo]

    def __init__(
        self,
        minimum: t.Union[dt.datetime, dt.date, None] = None,
        maximum: t.Union[dt.datetime, dt.date, None] = None,
        *,
        fix_timezone: bool = False,
        fixed_timezone: t.Optional[dt.tzinfo] = None,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random datetime values.

        Parameters
        ----------
        minimum : datetime | date, optional
            the minimum
        maximum : datetime | date, optional
            the maximum
        fix_timezone : bool, default=False
            If it is True, the tzinfo of result is fixed to `fixed_timezone`.
        fixed_timezone : tzinfo, default=None
            If `fix_timezone` is True, the tzinfo of result is fixed to this.
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._min, self._max = self._normalize(minimum, maximum)
        self._fix_timezone = fix_timezone
        self._fixed_timezone = fixed_timezone

        if (self._min.tzinfo is None and self._max.tzinfo is not None) or (
            self._min.tzinfo is not None and self._max.tzinfo is None
        ):
            raise FactoryConstructionError(
                "cannot define range for randdatetime with a naive datetime "
                "and an aware datetime"
            )
        if self._min > self._max:
            raise FactoryConstructionError("empty range for randdatetime")

        self._range = self._max - self._min

    def _next(self) -> dt.datetime:
        weight = self._random.random()

        pre_result = self._min + self._range * weight
        if self._fix_timezone:
            if pre_result.tzinfo is not None and self._fixed_timezone is not None:
                return pre_result.astimezone(self._fixed_timezone)
            else:
                return pre_result.replace(tzinfo=self._fixed_timezone)
        else:
            return pre_result

    @classmethod
    def _normalize(
        cls,
        minimum: t.Union[dt.datetime, dt.date, None],
        maximum: t.Union[dt.datetime, dt.date, None],
    ) -> t.Tuple[dt.datetime, dt.datetime]:
        if isinstance(minimum, dt.date) and not isinstance(minimum, dt.datetime):
            minimum = dt.datetime.combine(minimum, dt.time(0))
        if isinstance(maximum, dt.date) and not isinstance(maximum, dt.datetime):
            maximum = dt.datetime.combine(
                maximum + dt.timedelta(days=1), dt.time(0)
            ) - dt.timedelta(microseconds=1)

        if minimum is not None and maximum is not None:
            return minimum, maximum
        elif minimum is not None:
            return minimum, minimum + dt.timedelta(days=1)
        elif maximum is not None:
            return maximum - dt.timedelta(days=1), maximum
        else:
            now = dt.datetime.utcnow()
            return now - dt.timedelta(hours=12), now + dt.timedelta(hours=12)
