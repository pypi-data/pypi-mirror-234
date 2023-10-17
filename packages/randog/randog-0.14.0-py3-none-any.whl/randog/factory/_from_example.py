import datetime as dt
import enum
from decimal import Decimal
import typing as t
from random import Random

from . import (
    by_callable,
    by_iterator,
    DictItem,
    Factory,
    randbool,
    randenum,
    randtimedelta,
    randdatetime,
    randdate,
    randtime,
    randdecimal,
    randdict,
    randfloat,
    randlist,
    randint,
    randstr,
    union,
    const,
)
from ._timedelta import calc_unit
from ._logging import logger
from ..exceptions import FactoryConstructionError

import randog


def _from_decimal(
    example: Decimal,
    rnd: t.Optional[Random],
) -> Factory[Decimal]:
    p_inf, n_inf, nan = 0.0, 0.0, 0.0
    decimal_len = None
    if example.is_infinite():
        if example > 0:
            p_inf = 1.0
        else:
            n_inf = 1.0
    elif example.is_nan():
        nan = 1.0
    else:
        decimal_len = -example.as_tuple()[2]
    return randdecimal(
        p_inf=p_inf, n_inf=n_inf, nan=nan, decimal_len=decimal_len, rnd=rnd
    )


def _from_timedelta(
    example: dt.timedelta,
    rnd: t.Optional[Random],
) -> Factory[dt.timedelta]:
    unit = calc_unit(example)

    if example < dt.timedelta(0):
        return randtimedelta(None, dt.timedelta(0), unit=unit, rnd=rnd)
    else:
        return randtimedelta(dt.timedelta(0), None, unit=unit, rnd=rnd)


def _from_datetime(
    example: dt.datetime,
    rnd: t.Optional[Random],
) -> Factory[dt.datetime]:
    return randdatetime(tzinfo=example.tzinfo, rnd=rnd)


def _from_time(
    example: dt.time,
    rnd: t.Optional[Random],
) -> Factory[dt.time]:
    return randtime(tzinfo=example.tzinfo, rnd=rnd)


_FACTORY_CONSTRUCTOR_BY_TYPE: t.Dict[
    type, t.Callable[[t.Optional[Random]], Factory]
] = {
    bool: lambda rnd: randbool(rnd=rnd),
    int: lambda rnd: randint(0, 100, rnd=rnd),
    float: lambda rnd: randfloat(0, 1.0, rnd=rnd),
    Decimal: lambda rnd: randdecimal(0, 1.0, rnd=rnd),
    str: lambda rnd: randstr(rnd=rnd),
    dt.timedelta: lambda rnd: randtimedelta(rnd=rnd),
    dt.datetime: lambda rnd: randdatetime(rnd=rnd),
    dt.date: lambda rnd: randdate(rnd=rnd),
    dt.time: lambda rnd: randtime(rnd=rnd),
    list: lambda rnd: randlist(randstr(), rnd=rnd),
    tuple: lambda rnd: randlist(randstr(), type=tuple, rnd=rnd),
    dict: lambda rnd: randdict({"key": randint(0, 100, rnd=rnd)}, rnd=rnd),
}

_FACTORY_CONSTRUCTOR_BY_EXAMPLE: t.Dict[
    type, t.Callable[[t.Any, t.Optional[Random]], Factory]
] = {
    Decimal: _from_decimal,
    dt.timedelta: _from_timedelta,
    dt.datetime: _from_datetime,
    dt.time: _from_time,
}


class FromExampleContext:
    _custom_chain_length: int
    _warned_too_long_custom_chain: bool
    _path: t.Tuple[t.Any, ...]
    _custom_funcs: t.Sequence["_CustomFunc"]
    _rnd: t.Optional[Random]
    _examples_stack: t.Tuple[t.Any, ...]

    _signal_terminate_custom: bool = False

    def __init__(
        self,
        path: t.Tuple[t.Any, ...],
        custom_func: t.Union["_CustomFunc", t.Sequence["_CustomFunc"], None],
        rnd: t.Optional[Random],
        examples_stack: t.Tuple[t.Any, ...],
        custom_chain_length: int = 0,
        warned_too_long_custom_chain: bool = False,
    ):
        self._path = path
        if custom_func is None:
            self._custom_funcs = []
        elif isinstance(custom_func, t.Sequence):
            self._custom_funcs = custom_func
        else:
            self._custom_funcs = [custom_func]
        self._rnd = rnd
        self._example_stacks = examples_stack
        self._custom_chain_length = custom_chain_length
        self._warned_too_long_custom_chain = warned_too_long_custom_chain

    @property
    def custom_chain_length(self) -> int:
        return self._custom_chain_length

    @property
    def path(self) -> t.Tuple[t.Any, ...]:
        return self._path

    @property
    def rnd(self) -> t.Optional[Random]:
        return self._rnd

    @property
    def custom_funcs(self) -> t.Sequence["_CustomFunc"]:
        return self._custom_funcs

    @property
    def examples(self) -> t.Tuple[t.Any, ...]:
        return self._example_stacks

    @property
    def current_example(self) -> t.Any:
        if len(self._example_stacks) <= 0:
            return None
        else:
            return self._example_stacks[-1]

    def terminate_custom_chain(self):
        self._signal_terminate_custom = True

    @property
    def signal_terminate_custom(self) -> bool:
        return self._signal_terminate_custom

    def set_warned_too_long_custom_chain(self):
        self._warned_too_long_custom_chain = True

    @property
    def warned_too_long_custom_chain(self) -> bool:
        return self._warned_too_long_custom_chain

    def from_example(self, example: t.Any) -> Factory:
        return from_example(
            example,
            custom_func=self._custom_funcs,
            rnd=self._rnd,
            context=self,
        )

    def recursive(self, child: t.Any, key: t.Any) -> Factory:
        new_context = ContextFactory.child_of(
            self,
            key=key,
            example=child,
        )
        return from_example(
            child,
            custom_func=self._custom_funcs,
            rnd=self._rnd,
            context=new_context,
        )


class _CustomFunc(t.Protocol):
    def __call__(
        self,
        example: t.Any,
        *,
        context: FromExampleContext,
    ) -> t.Any:
        ...


class ContextFactory:
    @classmethod
    def root(
        cls,
        custom_func: t.Union[_CustomFunc, t.Sequence[_CustomFunc], None],
        rnd: t.Optional[Random],
        example: t.Any,
    ) -> FromExampleContext:
        return FromExampleContext(
            path=tuple(),
            custom_func=custom_func,
            rnd=rnd,
            examples_stack=(example,),
        )

    @classmethod
    def child_of(
        cls,
        context: FromExampleContext,
        *,
        key: t.Any,
        example: t.Any,
    ) -> FromExampleContext:
        return FromExampleContext(
            path=(*context.path, key),
            custom_func=context.custom_funcs,
            rnd=context.rnd,
            examples_stack=(*context.examples, example),
        )

    @classmethod
    def count_up_custom(
        cls,
        context: FromExampleContext,
    ) -> "FromExampleContext":
        return FromExampleContext(
            path=context.path,
            custom_func=context.custom_funcs,
            rnd=context.rnd,
            custom_chain_length=context.custom_chain_length + 1,
            warned_too_long_custom_chain=False,
            examples_stack=context.examples,
        )

    @classmethod
    def reset_signals(
        cls,
        context: FromExampleContext,
    ) -> "FromExampleContext":
        return FromExampleContext(
            path=context.path,
            custom_func=context.custom_funcs,
            rnd=context.rnd,
            custom_chain_length=context.custom_chain_length,
            warned_too_long_custom_chain=context.warned_too_long_custom_chain,
            examples_stack=context.examples,
        )


def _dict_item(obj, key, context: FromExampleContext) -> DictItem:
    if isinstance(obj, randog.DictItemExample):
        return DictItem(context.recursive(obj.example, key), obj.prop_exists)
    else:
        return DictItem(context.recursive(obj, key))


def _list_item(item: t.Tuple[int, t.Any], context: FromExampleContext) -> Factory:
    index, obj = item
    return context.recursive(obj, index)


def from_example(
    example: t.Any,
    *,
    custom_func: t.Union[_CustomFunc, t.Sequence[_CustomFunc], None] = None,
    rnd: t.Optional[Random] = None,
    context: t.Optional[FromExampleContext] = None,
) -> Factory:
    """Returns a factory generating value like specified example or type.

    Parameters
    ----------
    example : Any
        the type or the example
    custom_func : Callable | Sequence[Callable]
        If specified, this function is executed first and
        its return value is used as a new example.
        If it returns a factory, it is used as is.
        If it returns `NotImplemented`, `from_example` behaves
        as if `custom_func` was not specified.
        The context is passed to this function.
        Multiple functions may be specified for `custom_func`,
        and if multiple functions are specified,
        they are executed in sequence until a value
        other than NotImplemented is returned.
        This sequence of processing is also used to create factories
        for child elements of dict and list.
        It is recommended that `custom_func` receives `**kwargs`
        to allow for more keyword arguments in future updates.
    rnd : Random, optional
        random number generator to be used
    context : FromExampleContext, optional
        the context of generation. Normally, you should not specify it.
        If specified, the context property takes precedence over other arguments.

    Raises
    ------
    FactoryConstructionError
        When the specified example or type is not supported.
    """
    if isinstance(example, Factory):
        return example
    if context is None:
        context = ContextFactory.root(
            custom_func=custom_func,
            rnd=rnd,
            example=example,
        )

    # print(example, context.custom_chain_length, "before while")
    while True:
        # print(example, context.custom_chain_length, "while")

        # terminate custom chain if custom_func execs terminate_custom_chain()
        if context.signal_terminate_custom:
            break

        # Limit the number of customizations to avoid infinite loops
        if context.custom_chain_length >= 32:
            if not context.warned_too_long_custom_chain:
                logger.warning(
                    "The application of custom_func in this generation was stopped "
                    "because custom_func was executed more than the specified number "
                    "of times during the generation of a single value in from_example."
                )
                context.set_warned_too_long_custom_chain()
            break

        context = ContextFactory.count_up_custom(context)

        for custom_func in context.custom_funcs:
            # print(example, context.custom_chain_length, "for")
            custom_result = custom_func(
                example,
                context=context,
            )
            # print(example, custom_result, "for")
            if isinstance(custom_result, Factory):
                return custom_result
            if custom_result is not NotImplemented and example != custom_result:
                example = custom_result
                break

            # reset signals from custom_func if the example is not customized
            context = ContextFactory.reset_signals(context)
        else:
            # If customization by custom_funcs is not performed,
            # no further customization is chained.
            break

    if isinstance(example, randog.Example):
        return union(*map(context.from_example, example), rnd=context.rnd)
    if isinstance(example, type):
        if issubclass(example, enum.Enum):
            return randenum(example, rnd=context.rnd)
        elif example in _FACTORY_CONSTRUCTOR_BY_TYPE:
            return _FACTORY_CONSTRUCTOR_BY_TYPE[example](context.rnd)
        else:
            raise FactoryConstructionError(
                f"cannot construct factory for unsupported type: {example}"
            )

    if example is None:
        return const(None, rnd=context.rnd)
    for type_, construct in _FACTORY_CONSTRUCTOR_BY_EXAMPLE.items():
        if isinstance(example, type_):
            return construct(example, rnd)
    if isinstance(example, t.Mapping):
        return randdict({k: _dict_item(v, k, context) for k, v in example.items()})
    if isinstance(example, t.Sequence) and not isinstance(example, str):
        if isinstance(example, (tuple, list)):
            _type = type(example)
        else:
            _type = None
        return randlist(
            type=_type,
            rnd=context.rnd,
            items_list=tuple(_list_item(exm, context) for exm in enumerate(example)),
        )
    if isinstance(example, t.Iterator):
        return by_iterator(example)
    if isinstance(example, t.Callable):
        return by_callable(example)

    return context.from_example(type(example))
