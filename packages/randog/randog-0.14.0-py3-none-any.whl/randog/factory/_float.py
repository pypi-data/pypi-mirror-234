import abc
import math
import sys
import typing as t
from random import Random

from ._base import Factory, decide_rnd
from .._utils import floatutils
from .._utils.floatutils import FRACTION_MAX
from ..exceptions import FactoryConstructionError
from ..rangeutils import interval, IntInterval


def randfloat(
    minimum: t.Optional[t.SupportsFloat] = None,
    maximum: t.Optional[t.SupportsFloat] = None,
    *,
    p_inf: t.SupportsFloat = 0.0,
    n_inf: t.SupportsFloat = 0.0,
    nan: t.SupportsFloat = 0.0,
    distribution: t.Literal["uniform", "exp_uniform"] = "uniform",
    rnd: t.Optional[Random] = None,
) -> Factory[float]:
    """Return a factory generating random float values.

    Parameters
    ----------
    minimum : float, optional
        the minimum
    maximum : float, optional
        the maximum
    p_inf : float, default=0
        the probability of positive infinity
    n_inf : float, default=0
        the probability of negative infinity
    nan : float, default=0
        the probability of NaN
    distribution : "uniform"|"exp_uniform", default="uniform"
        probability distribution. If 'uniform', the distribution is uniform.
        If 'exp_uniform', the distribution of digits (log with a base of 2) is uniform.
    rnd : Random, optional
        random number generator to be used

    Raises
    ------
    FactoryConstructionError
        When the specified generating conditions are inconsistent.
    """
    if distribution is None or distribution == "uniform":
        return FloatRandomFactory(
            minimum,
            maximum,
            p_inf=p_inf,
            n_inf=n_inf,
            nan=nan,
            rnd=rnd,
        )
    elif distribution == "exp_uniform":
        return FloatExpRandomFactory(
            minimum,
            maximum,
            p_inf=p_inf,
            n_inf=n_inf,
            nan=nan,
            rnd=rnd,
        )
    else:
        raise ValueError(f"illegal distribution: {distribution}")


class _BaseFloatRandomFactory(Factory[float], abc.ABC):
    _random: Random
    _min: float
    _max: float
    _p_inf: float
    _n_inf: float
    _nan: float

    def __init__(
        self,
        minimum: t.Optional[t.SupportsFloat] = None,
        maximum: t.Optional[t.SupportsFloat] = None,
        *,
        p_inf: t.SupportsFloat = 0.0,
        n_inf: t.SupportsFloat = 0.0,
        nan: t.SupportsFloat = 0.0,
        rnd: t.Optional[Random] = None,
    ):
        """Return a factory generating random float values.

        Parameters
        ----------
        minimum : float, optional
            the minimum
        maximum : float, optional
            the maximum
        p_inf : float, default=0
            the probability of positive infinity
        n_inf : float, default=0
            the probability of negative infinity
        nan : float, default=0
            the probability of NaN
        rnd : Random, optional
            random number generator to be used

        Raises
        ------
        FactoryConstructionError
            When the specified generating conditions are inconsistent.
        """
        self._random = decide_rnd(rnd)
        self._min, self._max = self._normalize(minimum, maximum)
        self._p_inf = float(p_inf)
        self._n_inf = float(n_inf)
        self._nan = float(nan)

        if (
            self._min > self._max
            or self._min == float("inf")
            or self._max == float("-inf")
        ):
            raise FactoryConstructionError("empty range for randfloat")
        if math.isnan(self._min) or math.isnan(self._max):
            raise FactoryConstructionError("minimum and maximum are must not be nan")
        if self._p_inf < 0.0 or self._n_inf < 0.0 or self._nan < 0.0:
            raise FactoryConstructionError(
                "the probabilities `p_inf`, `n_inf`, and `nan` must range from 0 to 1"
            )
        if self._p_inf + self._n_inf + self._nan > 1.0:
            raise FactoryConstructionError(
                "the sum of probabilities `p_inf`, `n_inf`, and `nan` "
                "must range from 0 to 1"
            )

    def _next(self) -> float:
        pre_weight = self._random.random()
        pre_weight -= self._p_inf
        if pre_weight < 0:
            return float("inf")
        pre_weight -= self._n_inf
        if pre_weight < 0:
            return float("-inf")
        pre_weight -= self._nan
        if pre_weight < 0:
            return float("NaN")

        return self._next_finite()

    @abc.abstractmethod
    def _next_finite(self) -> float:
        pass

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[t.SupportsFloat],
        maximum: t.Optional[t.SupportsFloat],
    ) -> t.Tuple[float, float]:
        default_range = 1.0

        if minimum is None and maximum is None:
            return 0.0, 1.0
        elif minimum is None:
            maximum = float(maximum)
            return maximum - default_range, maximum
        elif maximum is None:
            minimum = float(minimum)
            return minimum, minimum + default_range
        else:
            return float(minimum), float(maximum)


class FloatRandomFactory(_BaseFloatRandomFactory):
    """factory generating random float values"""

    _random: Random
    _min: float
    _max: float
    _p_inf: float
    _n_inf: float
    _nan: float

    def _next_finite(self) -> float:
        weight = self._random.random()
        return self._max * weight + self._min * (1 - weight)

    @classmethod
    def _normalize(
        cls,
        minimum: t.Optional[t.SupportsFloat],
        maximum: t.Optional[t.SupportsFloat],
    ) -> t.Tuple[float, float]:
        default_range = 1.0

        if minimum == float("-inf"):
            minimum = -sys.float_info.max
        if maximum == float("inf"):
            maximum = sys.float_info.max

        if minimum is None and maximum is None:
            return 0.0, 1.0
        elif minimum is None:
            maximum = float(maximum)
            return maximum - default_range, maximum
        elif maximum is None:
            minimum = float(minimum)
            return minimum, minimum + default_range
        else:
            return float(minimum), float(maximum)


class FloatExpRandomFactory(_BaseFloatRandomFactory):
    _random: Random
    _min: float
    _max: float
    _min_exp: int
    _max_exp: int
    _pattern_num_of_min_exp: int
    _pattern_num_of_max_exp: int
    _pattern_num: int
    _fraction_range_of_min_exp: IntInterval
    _fraction_range_of_max_exp: IntInterval
    _p_inf: float
    _n_inf: float
    _nan: float

    def __init__(
        self,
        minimum: t.Optional[t.SupportsFloat] = None,
        maximum: t.Optional[t.SupportsFloat] = None,
        *,
        p_inf: t.SupportsFloat = 0.0,
        n_inf: t.SupportsFloat = 0.0,
        nan: t.SupportsFloat = 0.0,
        rnd: t.Optional[Random] = None,
    ):
        super().__init__(minimum, maximum, p_inf=p_inf, n_inf=n_inf, nan=nan, rnd=rnd)

        self._min_exp, self._min_fraction = self._calc_exp_and_fraction(
            self._min,
            # Don't include negative min in the generation range.
            # However, if min == max,
            # it is included so that the generation range is not empty.
            to0_if_neg=self._min != self._max,
        )
        self._max_exp, self._max_fraction = self._calc_exp_and_fraction(
            self._max,
            # Don't include positive max in the generation range.
            # However, if min == max,
            # it is included so that the generation range is not empty.
            to0_if_pos=self._min != self._max,
        )

        if self._min_exp == self._max_exp:
            if self._min_exp < 0:
                self._fraction_range_of_min_exp = interval(
                    self._max_fraction, self._min_fraction
                )
                self._fraction_range_of_max_exp = interval(
                    self._max_fraction, self._min_fraction
                )
            else:
                self._fraction_range_of_min_exp = interval(
                    self._min_fraction, self._max_fraction
                )
                self._fraction_range_of_max_exp = interval(
                    self._min_fraction, self._max_fraction
                )
            self._pattern_num_of_min_exp = self._fraction_range_of_min_exp.count_int()
            self._pattern_num_of_max_exp = self._fraction_range_of_max_exp.count_int()
            self._pattern_num = self._pattern_num_of_min_exp
        else:
            if self._min_exp < 0:
                self._fraction_range_of_min_exp = interval(0, self._min_fraction)
            else:
                self._fraction_range_of_min_exp = interval(
                    self._min_fraction, FRACTION_MAX
                )
            if self._max_exp < 0:
                self._fraction_range_of_max_exp = interval(
                    self._max_fraction, FRACTION_MAX
                )
            else:
                self._fraction_range_of_max_exp = interval(0, self._max_fraction)
            self._pattern_num_of_min_exp = self._fraction_range_of_min_exp.count_int()
            self._pattern_num_of_max_exp = self._fraction_range_of_max_exp.count_int()
            self._pattern_num = (
                (self._max_exp - self._min_exp - 1) * 2**52
                + self._pattern_num_of_min_exp
                + self._pattern_num_of_max_exp
            )

    def _next_finite(self) -> float:
        exp = self._next_exp()
        fraction = self._next_fraction(exp)

        return self._calc_float_from_exp_and_fraction(exp, fraction)

    def _next_exp(self) -> int:
        pre_weight = self._random.randrange(0, self._pattern_num)
        pre_weight -= self._pattern_num_of_min_exp
        if pre_weight < 0:
            return self._min_exp
        pre_weight -= self._pattern_num_of_max_exp
        if pre_weight < 0:
            return self._max_exp

        return self._random.randint(self._min_exp + 1, self._max_exp - 1)

    def _next_fraction(self, next_exp: int) -> int:
        if next_exp == 0:
            return 0
        elif next_exp == self._min_exp:
            return self._random.randint(*self._fraction_range_of_min_exp.minmax())
        elif next_exp == self._max_exp:
            return self._random.randint(*self._fraction_range_of_max_exp.minmax())
        else:
            return self._random.randrange(0, 2**52)

    @classmethod
    def _calc_exp_and_fraction(
        cls, edge: float, to0_if_neg: bool = False, to0_if_pos: bool = False
    ) -> t.Tuple[int, int]:
        sign, exp, fraction = floatutils.to_tuple(edge)

        # don't contain negative min and positive max into random value range
        if to0_if_neg and sign == 1 or to0_if_pos and sign == 0:
            sign, exp, fraction = floatutils.next_to_0(sign, exp, fraction)

        if sign == 1:
            exp *= -1
        return exp, fraction

    @classmethod
    def _calc_float_from_exp_and_fraction(cls, exp: int, fraction: int) -> float:
        sign = t.cast(t.Literal[0, 1], 1 if exp < 0 else 0)
        unsigned_exp = abs(exp)

        return floatutils.parse(sign, unsigned_exp, fraction)
