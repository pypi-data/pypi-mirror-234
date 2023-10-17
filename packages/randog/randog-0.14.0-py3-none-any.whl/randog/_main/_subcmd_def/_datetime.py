import argparse
import datetime as dt
import typing as t

import randog.factory
from ..._utils.type import datetime
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random


class SubcmdDefDatetime(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Datetime

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        datetime_parser = subparsers.add_parser(
            Subcmd.Datetime.value,
            usage=(
                "python -m randog datetime [MINIMUM MAXIMUM] [--iso | --fmt FORMAT] "
                "[common-options]"
            ),
            description="It generates values of type datetime.datetime.",
            add_help=False,
        )
        datetime_args_group = datetime_parser.add_argument_group("arguments")
        datetime_args_group.add_argument(
            "minimum",
            type=datetime,
            nargs="?",
            metavar="MINIMUM",
            help=(
                "the minimum value. "
                "In addition to ISO-8601 format, 'now', which indicates the datetime "
                "of execution, can also be used. "
                "The datetime can also be expressed by adding the timedelta to the "
                "datetime, for example, 'now+12h' or '2022-01-01-30d'. "
                "If the datetime term is omitted, e.g., '-12h', "
                "then the MINIMUM is the MAXIMUM plus the specified timedelta. "
                "However, if the datetime term is omitted in MAXIMUM or MAXIMUM itself "
                "is omitted, then the MINIMUM is the current datetime plus the "
                "specified timedelta. "
                "If both MINIMUM and MAXIMUM are omitted completely, "
                "the behavior is left to the specification of "
                "randog.factory.randdatetime."
            ),
        )
        datetime_args_group.add_argument(
            "maximum",
            type=datetime,
            nargs="?",
            metavar="MAXIMUM",
            help=(
                "the maximum value. "
                "In addition to ISO-8601 format, 'now', which indicates the datetime "
                "of execution, can also be used. "
                "The datetime can also be expressed by adding the timedelta to the "
                "datetime, for example, 'now+12h' or '2022-01-01-30d'. "
                "If the datetime term is omitted, e.g., '+12h', "
                "then the MAXIMUM is the MINIMUM plus the specified timedelta. "
                "However, if the datetime term is omitted in MINIMUM or MINIMUM itself "
                "is omitted, then the MAXIMUM is the current datetime plus the "
                "specified timedelta. "
                "If both MINIMUM and MAXIMUM are omitted completely, "
                "the behavior is left to the specification of "
                "randog.factory.randdatetime."
            ),
        )
        group_date_fmt = datetime_args_group.add_mutually_exclusive_group()
        group_date_fmt.add_argument(
            "--iso",
            action="store_true",
            help="if specified, it outputs generated object with ISO-8601 format",
        )
        group_date_fmt.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated object with the specified format, "
            "such as '%%Y/%%m/%%d %%H:%%M:%%S.%%f'",
        )
        add_common_arguments(datetime_parser)

        return datetime_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Datetime:
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
        return randog.factory.randdatetime


def _normalize_min_max(
    arg0: t.Union[dt.datetime, dt.timedelta, None],
    arg1: t.Union[dt.datetime, dt.timedelta, None],
) -> t.Tuple[t.Optional[dt.datetime], t.Optional[dt.datetime]]:
    minimum: t.Optional[dt.datetime]
    maximum: t.Optional[dt.datetime]

    now = dt.datetime.now()
    if None not in (arg0, arg1):
        if isinstance(arg0, dt.timedelta) and isinstance(arg1, dt.timedelta):
            minimum = now + arg0
            maximum = now + arg1
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
            minimum, maximum = sorted((now, now + arg0))
        else:
            minimum = arg0
            maximum = None
    else:
        minimum = None
        maximum = None

    return minimum, maximum
