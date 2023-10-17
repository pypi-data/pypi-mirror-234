import argparse
import typing as t

import randog.factory
from ..._utils.type import non_negative_int
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random


class SubcmdDefString(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.String

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        str_parser = subparsers.add_parser(
            Subcmd.String.value,
            usage=(
                "python -m randog str [--length LENGTH] [--charset CHARSET] "
                "[--regex REGEX] [--fmt FORMAT] [common-options]"
            ),
            description="It generates values of type str.",
            add_help=False,
        )
        str_args_group = str_parser.add_argument_group("arguments")
        str_args_group.add_argument(
            "--length",
            type=non_negative_int_range,
            default=None,
            metavar="LENGTH",
            help=(
                "the length of generated strings. "
                "You can specify an integer such as '--length 5' or a range such as "
                "'--length 3:8'."
            ),
        )
        str_args_group.add_argument(
            "--charset",
            type=str,
            default=None,
            metavar="CHARSET",
            help="the characters which contained by generated strings",
        )
        str_args_group.add_argument(
            "--regex",
            type=str,
            default=None,
            metavar="REGEX",
            help=(
                "the regular expression for generated string. "
                "It cannot be used with `--length` or `--charset`."
            ),
        )
        str_args_group.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated value with the specified format, "
            "such as '>10'",
        )
        add_common_arguments(str_parser)

        return str_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        iargs, kwargs = self.build_args(args)
        regex = kwargs["regex"]
        length = kwargs.get("length")
        charset = kwargs["charset"]

        if regex is not None:
            try:
                import rstr  # noqa: F401
            except ImportError:
                subparser.error(
                    "argument --regex: package 'rstr' is required to use --regex"
                )

        if regex is not None and length is not None:
            subparser.error("argument --regex: not allowed with argument --length")
        if regex is not None and charset is not None:
            subparser.error("argument --regex: not allowed with argument --charset")

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        rnd = construct_random(args.seed)
        kwargs = {
            "charset": args.get("charset"),
            "regex": args.get("regex"),
            "rnd": rnd,
        }
        length = args.get("length")
        if length is not None:
            if length[0] == length[1]:
                kwargs["length"] = length[0]
            else:
                kwargs["length"] = randog.factory.randint(*length)

        return tuple(), kwargs

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randstr


def non_negative_int_range(value: str) -> t.Tuple[int, int]:
    if ":" in value:
        value_s_str, value_e_str = value.split(":", 1)
        value_s = non_negative_int(value_s_str)
        value_e = non_negative_int(value_e_str)

        if value_s > value_e:
            raise ValueError("range must not be empty")

    else:
        value_s = value_e = non_negative_int(value)

    return value_s, value_e
