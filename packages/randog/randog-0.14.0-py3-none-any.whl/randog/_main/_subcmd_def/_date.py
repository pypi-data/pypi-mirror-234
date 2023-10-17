import argparse
import datetime as dt
import typing as t

import randog.factory
from ..._utils.type import date
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random


class SubcmdDefDate(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Date

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        date_parser = subparsers.add_parser(
            Subcmd.Date.value,
            usage=(
                "python -m randog date [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] "
                "[common-options]"
            ),
            description="It generates values of type datetime.date.",
            add_help=False,
        )
        date_args_group = date_parser.add_argument_group("arguments")
        date_args_group.add_argument(
            "minimum",
            type=date,
            nargs="?",
            metavar="MINIMUM",
            help=(
                "the minimum value. "
                "In addition to ISO-8601 format, 'today', which indicates the date "
                "of execution, can also be used. "
                "The date can also be expressed by adding the timedelta to the "
                "date, for example, 'today+2d' or '2022-01-01-30d'. "
                "If the date term is omitted, e.g., '-7d', "
                "then the MINIMUM is the MAXIMUM plus the specified timedelta. "
                "However, if the date term is omitted in MAXIMUM or MAXIMUM itself "
                "is omitted, then the MINIMUM is the current date plus the "
                "specified timedelta. "
                "If both MINIMUM and MAXIMUM are omitted completely, "
                "the behavior is left to the specification of "
                "randog.factory.randdate."
            ),
        )
        date_args_group.add_argument(
            "maximum",
            type=date,
            nargs="?",
            metavar="MAXIMUM",
            help=(
                "the maximum value. "
                "In addition to ISO-8601 format, 'today', which indicates the date "
                "of execution, can also be used. "
                "The date can also be expressed by adding the timedelta to the "
                "date, for example, 'today+2d' or '2022-01-01-30d'. "
                "If the date term is omitted, e.g., '+7d', "
                "then the MAXIMUM is the MINIMUM plus the specified timedelta. "
                "However, if the date term is omitted in MINIMUM or MINIMUM itself "
                "is omitted, then the MAXIMUM is the current date plus the "
                "specified timedelta. "
                "If both MINIMUM and MAXIMUM are omitted completely, "
                "the behavior is left to the specification of "
                "randog.factory.randdate."
            ),
        )
        group_date_fmt = date_args_group.add_mutually_exclusive_group()
        group_date_fmt.add_argument(
            "--iso",
            action="store_true",
            help=(
                "if specified, it outputs generated object with ISO-8601 format. "
                "Since the str of datetime.date is identical to the iso-8601 format, "
                "this option is meaningless."
            ),
        )
        group_date_fmt.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help=(
                "if specified, it outputs generated object with the specified format, "
                "such as '%%Y/%%m/%%d'"
            ),
        )
        add_common_arguments(date_parser)

        return date_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Date:
            return

        iargs, kwargs = self.build_args(args)
        minimum, maximum = iargs

        if minimum is not None and maximum is not None and minimum > maximum:
            subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")

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
        return randog.factory.randdate


def _normalize_min_max(
    arg0: t.Union[dt.date, dt.timedelta, None],
    arg1: t.Union[dt.date, dt.timedelta, None],
) -> t.Tuple[t.Optional[dt.date], t.Optional[dt.date]]:
    minimum: t.Optional[dt.date]
    maximum: t.Optional[dt.date]

    today = dt.date.today()
    if None not in (arg0, arg1):
        if isinstance(arg0, dt.timedelta) and isinstance(arg1, dt.timedelta):
            minimum = today + arg0
            maximum = today + arg1
        elif isinstance(arg0, dt.timedelta):
            minimum = arg1 + arg0
            maximum = arg1
        elif isinstance(arg1, dt.timedelta):
            minimum = arg0
            maximum = arg0 + arg1
        else:
            minimum = arg0
            maximum = arg1
    elif arg0 is not None:
        if isinstance(arg0, dt.timedelta):
            minimum, maximum = sorted((today, today + arg0))
        else:
            minimum = arg0
            maximum = None
    else:
        minimum = None
        maximum = None

    return minimum, maximum
