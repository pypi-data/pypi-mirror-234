import math
import typing as t


class FloatInterval:
    _min: float
    _max: float

    def __init__(self, minimum: float, maximum: float):
        self._min = minimum
        self._max = maximum

    def __contains__(self, item):
        return self._min <= item <= self._max

    def __repr__(self):
        return f"interval({self._min}, {self._max})"

    def radius(self, radius: float) -> "FloatInterval":
        radius = abs(radius)
        return FloatInterval(self._min - radius, self._max + radius)

    def count_int(self) -> int:
        return int(math.floor(self._max) - math.ceil(self._min)) + 1

    def minmax(self) -> t.Iterable[float]:
        return self._min, self._max

    def __and__(self, other) -> "FloatInterval":
        if isinstance(other, FloatInterval):
            new_min = max(self._min, other._min)
            new_max = min(self._max, other._max)
            if new_min <= new_max:
                return interval(new_min, new_max)
            else:
                return interval(empty=True)
        else:
            return NotImplemented


class IntInterval(FloatInterval):
    _min: int
    _max: int

    def radius(self, radius: float) -> "FloatInterval":
        radius = abs(radius)
        if isinstance(radius, int):
            return IntInterval(self._min - radius, self._max + radius)
        else:
            return FloatInterval(self._min - radius, self._max + radius)

    def count_int(self) -> int:
        return self._max - self._min + 1

    @t.overload
    def __and__(self, other: "IntInterval") -> "IntInterval":
        pass

    @t.overload
    def __and__(self, other: FloatInterval) -> FloatInterval:
        pass

    def __and__(self, other) -> "FloatInterval":
        return super().__and__(other)


class EmptyInterval(IntInterval):
    def __init__(self):
        super().__init__(float("nan"), float("nan"))

    def __contains__(self, item):
        return False

    def __repr__(self):
        return "interval.empty()"

    def count_int(self) -> int:
        return 0

    def radius(self, radius: float) -> "FloatInterval":
        raise Exception("cannot calc a radius interval whose center is empty interval")

    def minmax(self) -> t.Iterable[float]:
        raise Exception("the empty interval have neither minimum nor maximum")


@t.overload
def interval(
    minimum: int,
    maximum: t.Optional[int] = None,
    *,
    empty: t.Literal[False] = False,
    bit_len: None = None,
    dec_len: None = None,
) -> IntInterval:
    pass


@t.overload
def interval(
    minimum: float,
    maximum: t.Optional[float] = None,
    *,
    empty: t.Literal[False] = False,
    bit_len: None = None,
    dec_len: None = None,
) -> FloatInterval:
    pass


@t.overload
def interval(
    minimum: None = None,
    maximum: None = None,
    *,
    empty: t.Literal[True],
    bit_len: None = None,
    dec_len: None = None,
) -> EmptyInterval:
    pass


@t.overload
def interval(
    minimum: None = None,
    maximum: None = None,
    *,
    empty: t.Literal[False] = False,
    bit_len: int,
    dec_len: None = None,
) -> IntInterval:
    pass


@t.overload
def interval(
    minimum: None = None,
    maximum: None = None,
    *,
    empty: t.Literal[False] = False,
    bit_len: None = None,
    dec_len: int,
) -> IntInterval:
    pass


def interval(
    minimum: t.Optional[float] = None,
    maximum: t.Optional[float] = None,
    *,
    empty: bool = False,
    bit_len: int = None,
    dec_len: int = None,
) -> FloatInterval:
    if empty:
        return EmptyInterval()
    if bit_len is not None:
        unsigned_bit_len = abs(bit_len)

        if bit_len > 0:
            return interval(1 << (unsigned_bit_len - 1), (1 << unsigned_bit_len) - 1)
        elif bit_len < 0:
            return interval(
                -(1 << unsigned_bit_len) + 1, -(1 << (unsigned_bit_len - 1))
            )
        else:
            return interval(0, 0)
    if dec_len is not None:
        unsigned_dec_len = abs(dec_len)

        if dec_len > 0:
            return interval(10 ** (unsigned_dec_len - 1), 10**unsigned_dec_len - 1)
        elif dec_len < 0:
            return interval(
                -(10**unsigned_dec_len) + 1, -(10 ** (unsigned_dec_len - 1))
            )
        else:
            return interval(0, 0)

    if maximum is None:
        maximum = minimum

    if isinstance(minimum, int) and isinstance(maximum, int):
        return IntInterval(minimum, maximum)
    else:
        return FloatInterval(minimum, maximum)
