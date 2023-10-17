import random
from abc import ABC, abstractmethod
import typing as t
from fractions import Fraction
from random import Random

from .._utils.nullsafe import dfor
from ._logging import logger

T = t.TypeVar("T")
R = t.TypeVar("R")

REGENERATE_PROB_MAX = float(Fraction(1023, 1024))


class Factory(ABC, t.Generic[T]):
    def next(
        self,
        *,
        raise_on_factory_stopped: bool = False,
    ) -> T:
        """Generate a value randomly according to the rules specified
        when assembling the factory.

        Parameters
        ----------
        raise_on_factory_stopped : bool, default=False
            If True, raises `FactoryStopException`
            in case the factory cannot generate value due to `StopIteration`.
            If False, simply raises `StopIteration`.

        Returns
        -------
        T
            a value generated randomly
        """
        try:
            return self._next()
        except StopIteration:
            if raise_on_factory_stopped:
                raise FactoryStopException()
            else:
                raise

    @abstractmethod
    def _next(self) -> T:
        pass

    def or_none(
        self,
        prob: float = 0.1,
        *,
        lazy_choice: bool = False,
        rnd: t.Optional[Random] = None,
    ) -> "Factory[t.Union[T, None]]":
        """Returns a factory whose result may be None with the specified probability.

        Examples
        --------
        >>> import randog
        >>>
        >>> factory = randog.factory.randstr().or_none(0.2)
        >>>
        >>> generated = factory.next()
        >>> assert generated is None or isinstance(generated, str)

        Parameters
        ----------
        prob : float, default=0.1
            Probability that the result is None
        lazy_choice : bool, optional
            If it is True, when generating a value,
            first generate value with the base factory and then decides
            whether to adopt it or None.
            Otherwise, it first decides whether to return None or generate a value
            and return it,
            and then generates a value only if it is returned.
        rnd : Random, optional
            random number generator to be used

        Returns
        -------
        Factory[T|None]
            A factory whose result may be None with the specified probability.
        """
        import randog.factory

        return randog.factory.union(
            self,
            randog.factory.const(None),
            weights=[1 - prob, prob],
            lazy_choice=lazy_choice,
            rnd=rnd,
        )

    def post_process(self, post_process: t.Callable[[T], R]) -> "Factory[R]":
        """Returns a factory whose result will be modified by `post_process`

        Examples
        --------
        >>> import randog
        >>>
        >>> # use post_process to format the random decimal value
        >>> factory = (
        ...     randog.factory.randdecimal(0, 50000, decimal_len=2)
        ...                  .post_process(lambda x: f"${x:,}")
        ... )
        >>>
        >>> # examples: '$12,345.67', '$3,153.21', '$12.90', etc.
        >>> generated = factory.next()
        >>> assert isinstance(generated, str)
        >>> assert generated[0] == "$"

        Parameters
        ----------
        post_process : Callable[[T], R]
            the mapping to modify the result

        Returns
        -------
        Factory[R]
            A factory whose result will be modified by `post_process`.
        """
        return PostFactory(self, post_process)

    def post_process_items(
        self,
        default_process: t.Optional[t.Callable[[t.Any], t.Any]] = None,
        **processes: t.Callable[[t.Any], t.Any],
    ) -> "Factory[R]":
        """Returns a factory whose result will be dict
        whose items is modified by `processes`

        Examples
        --------
        >>> import randog
        >>>
        >>> # use post_process_items to format the random decimal value '["count"]'
        >>> factory = (
        ...     randog.factory.randdict(
        ...         name=randog.factory.randstr(),
        ...         count=randog.factory.randdecimal(0, 50000, decimal_len=2),
        ...     ).post_process_items(count=lambda x: f"${x:,}")
        ... )
        >>>
        >>> # examples: {'name': 'sir1w94s', 'count': '$12,345.67'}, etc.
        >>> generated = factory.next()
        >>> assert isinstance(generated["count"], str)
        >>> assert generated["count"][0] == "$"

        Parameters
        ----------
        default_process : Callable[[Any], Any] | None
            the mapping to modify items which is not defined in `processes`
        processes: Callable[[Any], Any]
            functions to modify each item

        Returns
        -------
        Factory[R]
            A factory whose result will be dict whose items is modified by `processes`
        """
        return PostDictFactory(self, processes, default_process)

    def iter(
        self,
        size: int,
        *,
        regenerate: float = 0.0,
        discard: float = 0.0,
        raise_on_factory_stopped: bool = False,
        rnd: t.Optional[Random] = None,
    ) -> t.Iterator[T]:
        """Returns an iterator which serves result randomly `size` times.

        Examples
        --------
        >>> import randog
        >>> factory = randog.factory.randstr(length=5)
        >>>
        >>> for result in factory.iter(10):
        ...     assert isinstance(result, str)
        >>>
        >>> results = list(factory.iter(5))
        >>> assert len(results) == 5

        Parameters
        ----------
        size : int
            the number of the iterator.
            However, if the argument `raise_on_factory_stopped` is not True,
            fewer iterations than the specified `size` will be executed
            if the factory is stopped.
            Also, if the argument `discard` is specified, the size may be less.
        regenerate : float, default=0.0
            the probability that the original factory generation value is not returned
            as is, but is regenerated.
            It affects cases where the original factory returns a value
            that is not completely random.
        discard : float, default=0.0
            the probability that the original factory generation value is not returned
            as is, but is discarded.
            If discarded, the number of times the value is generated is less than
            `size`.
        raise_on_factory_stopped : bool, default=False
            If True, the iteration raises `FactoryStopException` in case the factory
            cannot generate value due to `StopIteration`.
            If False, the iteration simply stops in the case.
        rnd : Random, optional
            random number generator to be used

        Returns
        -------
        Iterator[T]
            An iterator
        """
        return FactoryIter(
            self,
            size,
            regenerate=regenerate,
            discard=discard,
            raise_on_factory_stopped=raise_on_factory_stopped,
            rnd=rnd,
        )

    def infinity_iter(
        self,
        *,
        regenerate: float = 0.0,
        raise_on_factory_stopped: bool = False,
        rnd: t.Optional[Random] = None,
    ) -> t.Iterator[T]:
        """Returns an infinity iterator which serves result randomly.

        The result is INFINITY so do NOT use it directly with `for`, `list`, and so on.

        However, if the argument `raise_on_factory_stopped` is not True,
        the iterator will be stopped if the factory is stopped.

        Examples
        --------
        >>> import randog
        >>> factory = randog.factory.randstr(length=5)
        >>>
        >>> keys = ["foo", "bar"]
        >>> for k, v in zip(keys, factory.infinity_iter()):
        ...     assert k in keys
        ...     assert isinstance(v, str)

        Parameters
        ----------
        regenerate : float, default=0.0
            the probability that the original factory generation value is not returned
            as is, but is regenerated.
            It affects cases where the original factory returns a value that is not
            completely random.
        raise_on_factory_stopped : bool, default=False
            If True, the iteration raises `FactoryStopException` in case the factory
            cannot generate value due to `StopIteration`.
            If False, the iteration simply stops in the case.
        rnd : Random, optional
            random number generator to be used

        Returns
        -------
        Iterator[T]
            An infinity iterator
        """
        return FactoryIter(
            self,
            None,
            regenerate=regenerate,
            raise_on_factory_stopped=raise_on_factory_stopped,
            rnd=rnd,
        )


class PostFactory(Factory[R], t.Generic[T, R]):
    _base_factory: Factory[T]
    _post_process: t.Callable[[T], R]

    def __init__(self, base_factory: Factory[T], post_process: t.Callable[[T], R]):
        self._base_factory = base_factory
        self._post_process = post_process

    def _next(self) -> R:
        pre_result = self._base_factory.next()
        return self._post_process(pre_result)


class PostDictFactory(Factory[R], t.Generic[T, R]):
    _base_factory: Factory[T]
    _processes: t.Mapping[str, t.Callable[[t.Any], t.Any]]
    _default_process: t.Callable[[t.Any], t.Any]

    def __init__(
        self,
        base_factory: Factory[T],
        processes: t.Mapping[str, t.Callable[[t.Any], t.Any]],
        default_process: t.Callable[[t.Any], t.Any],
    ):
        self._base_factory = base_factory
        self._processes = processes
        self._default_process = (
            default_process if default_process is not None else lambda x: x
        )

    def _next(self) -> R:
        pre_result = self._base_factory.next()

        if not isinstance(pre_result, t.Mapping):
            return pre_result

        return {
            key: self._process_item(key, pre_value)
            for key, pre_value in pre_result.items()
        }

    def _process_item(self, key, pre_value) -> t.Any:
        if key in self._processes:
            return self._processes[key](pre_value)
        else:
            return self._default_process(pre_value)


class FactoryIter(t.Generic[T], t.Iterator[T]):
    _rnd: random.Random
    _factory: Factory[T]
    _size: t.Union[int, float]
    _regenerate_prob: float
    _discard_prob: float
    _raise_on_factory_stopped: bool
    _count: int = 0

    def __init__(
        self,
        factory: Factory[T],
        size: t.Union[int, None],
        *,
        regenerate: float = 0.0,
        discard: float = 0.0,
        raise_on_factory_stopped: bool = False,
        rnd: t.Optional[Random] = None,
    ):
        self._rnd = dfor(rnd, random.Random())
        self._factory = factory

        if regenerate > 0 and discard > 0:
            raise ValueError(
                "`regenerate` and `discard` cannot be specified at the same time"
            )
        if regenerate < 0 or REGENERATE_PROB_MAX < regenerate:
            raise ValueError(
                "the probability `regenerate` must range from 0 to 1023/1024"
            )
        if discard < 0 or 1 < discard:
            raise ValueError("the probability `discard` must range from 0 to 1")

        self._size = size if size is not None else float("Infinity")
        self._regenerate_prob = regenerate
        self._discard_prob = discard
        self._raise_on_factory_stopped = raise_on_factory_stopped

    def __next__(self) -> T:
        while True:
            if self._count >= self._size:
                raise StopIteration()

            self._count += 1

            # Regenerate until break
            while True:
                generated = self._factory.next(
                    raise_on_factory_stopped=self._raise_on_factory_stopped
                )

                if (
                    self._regenerate_prob <= 0
                    or self._rnd.random() >= self._regenerate_prob
                ):
                    break

            # Probabilistically,
            # discard the value generated this time and proceed to the next one
            if self._discard_prob > 0 and self._rnd.random() < self._discard_prob:
                continue

            return generated


class FactoryStopException(Exception):
    def __init__(self):
        super().__init__("the factory stopped generating")


@t.overload
def decide_rnd(
    explicit: t.Optional[random.Random], default: t.Literal[True] = True
) -> random.Random:
    pass


@t.overload
def decide_rnd(
    explicit: t.Optional[random.Random], default: t.Literal[False]
) -> t.Optional[random.Random]:
    pass


def decide_rnd(
    explicit: t.Optional[random.Random], default: bool = True
) -> t.Optional[random.Random]:
    """Decide random object used in the factory instance

    Parameters
    ----------
    explicit : Random | None
        Explicit designation
    default : bool, default=True
        The default behavior is to specify a new Random object if True,
        or None if False.

    Returns
    -------
    Random | None
        decided random object
    """
    if explicit is not None:
        logger.debug("use Random() object specified as argument 'rnd' of the factory")
        return explicit

    from . import _from_pyfile_config

    pyfile_rnd = _from_pyfile_config.rnd
    if pyfile_rnd is not None:
        logger.debug(
            "use Random() object sent into __randog__ "
            "(a factory definition file executed in 'from_pyfile()')"
        )
        return pyfile_rnd

    if default:
        new_rnd = Random()
        logger.debug("use a newly created Random() object since not specified")
        return new_rnd
    else:
        return None
