import codecs
import datetime as dt
import re
import typing as t
from decimal import Decimal, InvalidOperation

from .. import timedelta_util


def decimal(value):
    try:
        return Decimal(value)
    except InvalidOperation:
        raise ValueError("invalid Decimal string")


def positive_int(value):
    value_int = int(value)
    if value_int <= 0:
        raise ValueError("must be positive")
    return value_int


def non_negative_int(value):
    value_int = int(value)
    if value_int < 0:
        raise ValueError("must be non-negative")
    return value_int


def probability(value):
    value_float = float(value)
    if 0 <= value_float <= 1:
        return value_float
    else:
        raise ValueError("must be in the range [0, 1]")


_DATETIME_REGEX = re.compile(
    r"^(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?)?|now)?([-+].+)?$"
)


def datetime(value) -> t.Union[dt.datetime, dt.timedelta]:
    """datetime include expression type of datetime+timedelta or timedelta

    This function accepts according inputs:

    - ISO-8601 (YYYY-mm-ddTHH:MM:SS, YYYY-mm-ddTHH:MM:SS.ffffff, ...)
    - YYYY-mm-dd HH:MM:SS, YYYY-mm-dd HH:MM:SS.ffffff, ...
    - now
    - timedelta simple expr (1h, +30m, -1h20m, ...)
    - datetime+timedelta (now+1h, YYYY-mm-ddTHH:MM:SS+30m, ...)

    Parameters
    ----------
    value
        string value

    Returns
    -------
    datetime | timedelta
        parsed value
    """
    found = _DATETIME_REGEX.match(value)

    if not found or value == "":
        raise ValueError(f"failed to parse datetime: {value}")

    base_str = found.group(1)
    shift_str = found.group(2)

    if base_str is None:
        base = None
    elif base_str == "now":
        base = dt.datetime.now()
    else:
        base = dt.datetime.fromisoformat(base_str)

    if shift_str is None or shift_str == "":
        shift = dt.timedelta(0)
    else:
        shift = timedelta_util.from_str(shift_str)

    if base is None:
        return shift
    else:
        return base + shift


_TIME_REGEX = re.compile(r"^(\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?|now)?([-+].+)?$")


def time(value):
    """time include expression type of time+timedelta or timedelta

    This function accepts according inputs:

    - ISO-8601 (HH:MM:SS, HH:MM:SS.ffffff, HH:MM, ...)
    - now
    - timedelta simple expr (1h, +30m, -1h20m, ...)
    - time+timedelta (now+1h, HH:MM:SS+30m, ...)

    Parameters
    ----------
    value
        string value

    Returns
    -------
    time | timedelta
        parsed value
    """
    found = _TIME_REGEX.match(value)

    if not found or value == "":
        raise ValueError(f"failed to parse time: {value}")

    base_str = found.group(1)
    shift_str = found.group(2)

    if base_str is None:
        base = None
    elif base_str == "now":
        base = dt.datetime.now()
    else:
        base = dt.datetime.combine(dt.date.today(), dt.time.fromisoformat(base_str))

    if shift_str is None or shift_str == "":
        shift = dt.timedelta(0)
    else:
        shift = timedelta_util.from_str(shift_str)

    if base is None:
        return shift
    else:
        return (base + shift).time()


_DATE_REGEX = re.compile(r"^(\d{4}-\d{2}-\d{2}|today)?([-+].+)?$")


def date(value):
    """date include expression type of date+timedelta or timedelta

    This function accepts according inputs:

    - ISO-8601 (YYYY-mm-dd, ...)
    - today
    - timedelta simple expr (+1d, ...)
    - date+timedelta (today+1d, YYYY-mm-dd-2d, ...)

    Parameters
    ----------
    value
        string value

    Returns
    -------
    date | timedelta
        parsed value
    """
    found = _DATE_REGEX.match(value)

    if not found or value == "":
        raise ValueError(f"failed to parse date: {value}")

    base_str = found.group(1)
    shift_str = found.group(2)

    if base_str is None:
        base = None
    elif base_str == "today":
        base = dt.date.today()
    else:
        base = dt.date.fromisoformat(base_str)

    if shift_str is None or shift_str == "":
        shift = dt.timedelta(0)
    else:
        shift = timedelta_util.from_str(shift_str)
        if shift % dt.timedelta(days=1) != dt.timedelta(0):
            raise ValueError(
                f"failed to parse date: {value}; "
                "timedelta part must be divided by a day"
            )

    if base is None:
        return shift
    else:
        return base + shift


def timedelta(value):
    return timedelta_util.from_str(value)


def positive_timedelta(value):
    result = timedelta_util.from_str(value)
    if result <= dt.timedelta(0):
        raise ValueError("must be positive")
    return timedelta_util.from_str(value)


def encoding(value):
    try:
        codecs.lookup(value)
    except LookupError as e:
        raise ValueError(*e.args)
    return value
