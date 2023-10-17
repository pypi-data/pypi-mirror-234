import argparse
import typing as t
from fractions import Fraction

from .. import Args, Subcmd
from ._base import SubcmdDef, add_common_arguments
from ..._utils.type import positive_int, probability
from ...factory import REGENERATE_PROB_MAX


class SubcmdDefByfile(SubcmdDef):
    def cmd(self) -> Subcmd:
        return Subcmd.Byfile

    def add_parser(self, subparsers) -> argparse.ArgumentParser:
        byfile_parser = subparsers.add_parser(
            Subcmd.Byfile.value,
            usage=(
                "python -m randog byfile FACTORY_PATH [FACTORY_PATH ...] "
                "[--regenerate PROB_REGEN] [--discard PROB_DISCARD] [--csv ROW_NUM] "
                "[--error-on-factory-stopped] [common-options]"
            ),
            description="It generates values according to factory definition files.",
            add_help=False,
        )
        byfile_args_group = byfile_parser.add_argument_group("arguments")
        byfile_args_group.add_argument(
            "factories",
            nargs="+",
            metavar="FACTORY_PATH",
            help="path of factory definition files",
        )
        byfile_args_group.add_argument(
            "--regenerate",
            metavar="PROB_REGEN",
            type=probability,
            default=0.0,
            help=(
                "the probability that the factory generation value is not returned as "
                "is, but is regenerated. "
                "It affects cases where the original factory returns a value "
                "that is not completely random."
            ),
        )
        byfile_args_group.add_argument(
            "--discard",
            metavar="PROB_DISCARD",
            type=probability,
            default=0.0,
            help=(
                "the probability that the factory generation value is not returned as "
                "is, but is discarded. "
                "If discarded, the number of times the value is generated is less than "
                "'--repeat'/'-r' or '--list'/'-L' or '--csv'."
            ),
        )
        byfile_args_group.add_argument(
            "--csv",
            metavar="ROW_NUM",
            type=positive_int,
            help=(
                "if specified, it outputs generated ROW_NUM objects as CSV. "
                "When using this option, it is recommended to use a factory "
                "that generates dictionaries and to define CSV_COLUMNS in the "
                "definition file to specify the fields of the CSV."
            ),
        )
        byfile_args_group.add_argument(
            "--error-on-factory-stopped",
            action="store_true",
            help=(
                "If specified, error is occurred in case the factory cannot generate "
                "value due to StopIteration. "
                "If not specified, the generation simply stops in the case."
            ),
        )
        add_common_arguments(byfile_parser)

        return byfile_parser

    def validate_parser(self, args: Args, subparser: argparse.ArgumentParser):
        if args.output_fmt == "repr" and args.csv is not None:
            subparser.error("argument --csv: not allowed with argument --repr")
        elif args.output_fmt == "json" and args.csv is not None:
            subparser.error("argument --csv: not allowed with argument --json")
        elif args.list is not None and args.csv is not None:
            subparser.error("argument --csv: not allowed with argument --list/-L")

        if args.regenerate > REGENERATE_PROB_MAX:
            prob_max = Fraction(REGENERATE_PROB_MAX)
            subparser.error(
                f"argument --regenerate: must be lower than or equal to {prob_max}"
            )

    def build_args(
        self, args: Args
    ) -> t.Tuple[t.Sequence[t.Any], t.Mapping[str, t.Any]]:
        pass

    def get_factory_constructor(self) -> t.Callable:
        pass
