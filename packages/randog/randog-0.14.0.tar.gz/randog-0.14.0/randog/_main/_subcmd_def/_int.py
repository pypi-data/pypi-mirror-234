import argparse
import typing as t

import randog.factory
from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from .._rnd import construct_random


class SubcmdDefInt(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Int

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        int_parser = subparsers.add_parser(
            Subcmd.Int.value,
            usage=(
                "python -m randog int MINIMUM MAXIMUM [--exp-uniform] [--fmt FORMAT] "
                "[common-options]"
            ),
            description="It generates integer values.",
            add_help=False,
        )
        int_args_group = int_parser.add_argument_group("arguments")
        int_args_group.add_argument(
            "minimum",
            type=int,
            metavar="MINIMUM",
            help="the minimum value",
        )
        int_args_group.add_argument(
            "maximum",
            type=int,
            metavar="MAXIMUM",
            help="the maximum value",
        )
        int_args_group.add_argument(
            "--exp-uniform",
            dest="distribution",
            action="store_const",
            const="exp_uniform",
            help=(
                "if specified, the distribution of digits (log with base 2) is uniform."
            ),
        )
        int_args_group.add_argument(
            "--fmt",
            dest="format",
            metavar="FORMAT",
            help="if specified, it outputs generated value with the specified format, "
            "such as '011.2f'",
        )
        add_common_arguments(int_parser)

        return int_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.sub_cmd != Subcmd.Int:
            return

        iargs, kwargs = self.build_args(args)
        minimum, maximum = iargs

        if minimum is not None and maximum is not None and minimum > maximum:
            subparser.error("arguments must satisfy MINIMUM <= MAXIMUM")

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        rnd = construct_random(args.seed)
        return (args.get("minimum"), args.get("maximum")), {
            "distribution": args.get("distribution"),
            "rnd": rnd,
        }

    def get_factory_constructor(self) -> t.Callable:
        return randog.factory.randint
