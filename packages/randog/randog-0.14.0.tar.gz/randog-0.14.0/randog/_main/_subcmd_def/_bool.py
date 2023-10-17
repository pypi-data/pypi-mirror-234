import argparse
import typing as t

import randog.factory
from ..._utils.type import probability
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random


class SubcmdDefBool(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Bool

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        bool_parser = subparsers.add_parser(
            Subcmd.Bool.value,
            usage="python -m randog bool [PROP_TRUE] [--fmt FORMAT] [common-options]",
            description="It generates boolean values.",
            add_help=False,
        )
        bool_args_group = bool_parser.add_argument_group("arguments")
        bool_args_group.add_argument(
            "prop_true",
            type=probability,
            default=0.5,
            nargs="?",
            metavar="PROP_TRUE",
            help="the probability of True",
        )
        bool_args_group.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated value with the specified format, "
            "such as '1'",
        )
        add_common_arguments(bool_parser)

        return bool_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        pass

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        rnd = construct_random(args.seed)
        return (args.get("prop_true"),), {"rnd": rnd}

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randbool
