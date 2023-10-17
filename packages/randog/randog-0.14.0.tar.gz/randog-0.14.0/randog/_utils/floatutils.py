import struct
import typing as t


FRACTION_MAX = 2**52 - 1

FloatAsTuple = t.Tuple[t.Literal[0, 1], int, int]


def to_tuple(value: float) -> FloatAsTuple:
    """Decompose a floating-point number into its sign, exponent, and fraction parts.

    Parameters
    ----------
    value
        a floating-point number

    Returns
    -------
    int, int, int
        sign, exponent, and fraction parts
    """
    as_bytes = struct.pack(">d", value)

    sign = t.cast(t.Literal[0, 1], as_bytes[0] >> 7)
    exp = (int.from_bytes(as_bytes[:2], "big") & 0x7FF0) >> 4
    fraction = int.from_bytes(as_bytes, "big") & 0x000FFFFFFFFFFFFF

    return sign, exp, fraction


def parse(sign: t.Literal[0, 1], exp: int, fraction: int) -> float:
    """create float value

    The result value is `(-1)^sign * 1.fraction * 2^(exp - 1023)` according to IEEE 754.

    Parameters
    ----------
    sign
        the sign of result value; 0 means positive, and 1 means negative.
    exp
        the exponent part (0-2047)
    fraction
        the fraction part

    Returns
    -------
    float:
        float value
    """
    as_bytes_as_int = sign << 63 | exp << 52 | fraction
    as_bytes = as_bytes_as_int.to_bytes(8, "big", signed=False)

    return struct.unpack(">d", as_bytes)[0]


def next_to_0(sign: t.Literal[0, 1], exp: int, fraction: int) -> FloatAsTuple:
    """Returns the number closest to x among the numbers that can be expressed in float
    type and are closer to 0 than x.

    x is `(-1)^sign * 1.fraction * 2^(exp - 1023)` according to IEEE 754.

    Parameters
    ----------
    sign
        the sign of x; 0 means positive, and 1 means negative.
    exp
        the exponent part (0-2047)
    fraction
        the fraction part

    Returns
    -------
    float:
        the number closest to x among the numbers that can be expressed in float
        type and are closer to 0 than x.
    """
    if fraction == 0:
        if exp == 0:
            return sign, 0, 0
        else:
            return sign, exp - 1, FRACTION_MAX
    else:
        return sign, exp, fraction - 1
