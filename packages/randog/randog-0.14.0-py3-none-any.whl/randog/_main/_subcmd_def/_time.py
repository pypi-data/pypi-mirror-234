import argparse
import datetime as dt
import typing as t

import randog.factory
from ..._utils.type import time
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random


class SubcmdDefTime(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Time

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        time_parser = subparsers.add_parser(
            Subcmd.Time.value,
            usage=(
                "python -m randog time [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] "
                "[common-options]"
            ),
            description="It generates values of type datetime.time.",
            add_help=False,
        )
        time_args_group = time_parser.add_argument_group("arguments")
        time_args_group.add_argument(
            "minimum",
            type=time,
            nargs="?",
            metavar="MINIMUM",
            help=(
                "the minimum value. "
                "In addition to ISO-8601 format, 'now', which indicates the time "
                "of execution, can also be used. "
                "The time can also be expressed by adding the timedelta to the "
                "time, for example, 'now+12h' or '12:00:00-42m'. "
                "If the time term is omitted, e.g., '-12h', "
                "then the MINIMUM is the MAXIMUM plus the specified timedelta. "
                "However, if the time term is omitted in MAXIMUM or MAXIMUM itself "
                "is omitted, then the MINIMUM is the current time plus the "
                "specified timedelta. "
                "If both MINIMUM and MAXIMUM are omitted completely, "
                "the behavior is left to the specification of "
                "randog.factory.randtime."
            ),
        )
        time_args_group.add_argument(
            "maximum",
            type=time,
            nargs="?",
            metavar="MAXIMUM",
            help=(
                "the maximum value. "
                "In addition to ISO-8601 format, 'now', which indicates the time "
                "of execution, can also be used. "
                "The time can also be expressed by adding the timedelta to the "
                "time, for example, 'now+12h' or '12:00:00-42m'. "
                "If the time term is omitted, e.g., '+12h', "
                "then the MAXIMUM is the MINIMUM plus the specified timedelta. "
                "However, if the time term is omitted in MINIMUM or MINIMUM itself "
                "is omitted, then the MAXIMUM is the current time plus the "
                "specified timedelta. "
                "If both MINIMUM and MAXIMUM are omitted completely, "
                "the behavior is left to the specification of "
                "randog.factory.randtime."
            ),
        )
        group_date_fmt = time_args_group.add_mutually_exclusive_group()
        group_date_fmt.add_argument(
            "--iso",
            action="store_true",
            help=(
                "if specified, it outputs generated object with ISO-8601 format"
                "Since the str of datetime.time is identical to the iso-8601 format, "
                "this option is meaningless."
            ),
        )
        group_date_fmt.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help=(
                "if specified, it outputs generated object with the specified format, "
                "such as '%%H:%%M:%%S.%%f'"
            ),
        )
        add_common_arguments(time_parser)

        return time_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Time:
            return

        if args.output_fmt == "repr" and args.iso:
            subparser.error("argument --iso: not allowed with argument --repr")
        elif args.output_fmt == "repr" and args.format:
            subparser.error("argument --fmt: not allowed with argument --repr")

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        rnd = construct_random(args.seed)
        minimum, maximum = _normalize_min_max(args.get("minimum"), args.get("maximum"))

        return (minimum, maximum), {"rnd": rnd}

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randtime


def _normalize_min_max(
    arg0: t.Union[dt.time, dt.timedelta, None],
    arg1: t.Union[dt.time, dt.timedelta, None],
) -> t.Tuple[t.Optional[dt.time], t.Optional[dt.time]]:
    minimum: t.Optional[dt.time]
    maximum: t.Optional[dt.time]

    now = dt.datetime.now()
    if None not in (arg0, arg1):
        if isinstance(arg0, dt.timedelta) and isinstance(arg1, dt.timedelta):
            minimum = (now + arg0).time()
            maximum = (now + arg1).time()
        elif isinstance(arg0, dt.timedelta):
            arg1_dt = dt.datetime.combine(dt.date.today(), arg1)
            minimum = (arg1_dt + arg0).time()
            maximum = arg1
        elif isinstance(arg1, dt.timedelta):
            arg0_dt = dt.datetime.combine(dt.date.today(), arg0)
            minimum = arg0
            maximum = (arg0_dt + arg1).time()
        else:
            minimum = arg0
            maximum = arg1
    elif arg0 is not None:
        if isinstance(arg0, dt.timedelta):
            if arg0 >= dt.timedelta(0):
                minimum = now.time()
                maximum = (now + arg0).time()
            else:
                minimum = (now + arg0).time()
                maximum = now.time()
        else:
            minimum = arg0
            maximum = None
    else:
        minimum = None
        maximum = None

    return minimum, maximum
