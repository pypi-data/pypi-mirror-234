import typing as t

T = t.TypeVar("T")
R = t.TypeVar("R")


@t.overload
def dfor(value: t.Optional[T], default: T) -> T:
    ...


@t.overload
def dfor(value0: t.Optional[T], value1: t.Optional[T], default: T) -> T:
    ...


def dfor(*values: t.Optional[T]) -> T:
    for value in values:
        if value is not None:
            return value
    else:
        return values[-1]


def dforc(m: t.Callable[[T], R], value: t.Optional[T]) -> t.Optional[R]:
    if value is None:
        return None
    else:
        return m(value)
