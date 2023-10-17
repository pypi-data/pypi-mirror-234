"""
the package contains the Args of module execution and its builder
"""

import argparse
import codecs
import datetime
import itertools
import typing as t

from . import Linesep
from ._subcmd import Subcmd


class Args:
    """Argument object when using randog as command"""

    _args: argparse.Namespace
    _commanded_args: t.Sequence[str]

    def __init__(self, argv: t.Sequence[str]):
        from ._subcmd_def import iter_subcmd_def

        self._commanded_args = argv[1:]

        parser = argparse.ArgumentParser(
            prog="randog",
            description="It generates values randomly according to the specified mode "
            "and arguments.",
        )
        subparsers = parser.add_subparsers(
            required=True,
            dest="sub",
            metavar="MODE",
            help=(
                "mode of value generation; candidates: "
                f"{', '.join(map(lambda c: c.value, Subcmd))}. "
                "For more information, see the command 'randog MODE --help'."
            ),
        )

        # create subcommands and add them to the ArgumentParser
        subcmd_parsers = {}
        for subcmd in iter_subcmd_def():
            subcmd_parsers[subcmd.cmd()] = subcmd.add_parser(subparsers)

        # parse the arguments
        self._args = parser.parse_args(self.commanded_args)

        # validate arguments for subcommands
        for subcmd in iter_subcmd_def():
            subcmd.validate_parser(self, subcmd_parsers[subcmd.cmd()])

    @property
    def commanded_args(self) -> t.Sequence[str]:
        return self._commanded_args

    @property
    def sub_cmd(self) -> Subcmd:
        return Subcmd(self._args.sub)

    @property
    def factories(self) -> t.Sequence[str]:
        return self._args.factories

    @property
    def repeat(self) -> int:
        return self._args.repeat

    @property
    def list(self) -> t.Optional[int]:
        return self._args.list

    @property
    def output_fmt(self) -> t.Optional[str]:
        return self._args.output_fmt

    @property
    def output_path(self) -> t.Optional[str]:
        return self._args.output

    @property
    def output_encoding(self) -> t.Optional[str]:
        specified = self._args.output_encoding
        if specified is None or self.output_path is None:
            return None
        try:
            codecs.lookup(specified)
            return specified
        except LookupError:
            raise ValueError(f"illegal encoding: {specified}")

    @property
    def output_linesep(self) -> t.Optional[str]:
        specified = self._args.output_linesep
        if specified is None or self.output_path is None:
            return None
        try:
            return Linesep[specified].value
        except KeyError:
            raise ValueError(f"illegal linesep: {specified}")

    @property
    def seed(self) -> t.Optional[t.Any]:
        return self._args.seed

    @property
    def iso(self) -> bool:
        if hasattr(self._args, "iso"):
            return self._args.iso
        else:
            return False

    @property
    def format(self) -> t.Optional[str]:
        if hasattr(self._args, "format"):
            return self._args.format
        else:
            return None

    @property
    def regenerate(self) -> float:
        if hasattr(self._args, "regenerate"):
            return self._args.regenerate
        else:
            return 0.0

    @property
    def discard(self) -> float:
        if hasattr(self._args, "discard"):
            return self._args.discard
        else:
            return 0.0

    @property
    def csv(self) -> t.Optional[int]:
        if hasattr(self._args, "csv"):
            return self._args.csv
        else:
            return None

    @property
    def error_on_factory_stopped(self) -> bool:
        return self.get("error_on_factory_stopped", False)

    @property
    def hide_randog_warnings(self) -> bool:
        return self.get("quiet", False)

    @property
    def log_stderr(self) -> t.Optional[str]:
        specified: t.Optional[str] = self.get("log_stderr", None)

        if specified is None:
            return None
        elif "full" in specified:
            return specified.replace("-full", "")
        else:
            return specified

    @property
    def log_stderr_is_full(self) -> bool:
        specified: t.Optional[str] = self.get("log_stderr", None)

        return specified is not None and "full" in specified

    @property
    def log_config_file(self) -> t.Optional[str]:
        return self.get("log", None)

    @property
    def env(self) -> t.Mapping[str, str]:
        if self._args.env is None:
            return {}

        result = {}
        for item in itertools.chain(*self._args.env):
            key_value = item.split("=", 1)
            if len(key_value) <= 1:
                result[key_value[0]] = ""
            else:
                key, value = key_value
                result[key] = value
        return result

    def output_path_for(
        self,
        number: int,
        *,
        def_file: str,
        repeat_count: int,
        factory_count: int,
        now: datetime.datetime,
        env: t.Mapping[str, str],
    ) -> t.Optional[str]:
        if self._args.output is None:
            return None
        else:
            return self._args.output.format(
                number,
                def_file=def_file,
                repeat_count=repeat_count,
                factory_count=factory_count,
                now=now,
                **env,
            )

    def get(self, key: str, default: t.Any = None) -> t.Any:
        if hasattr(self._args, key):
            return getattr(self._args, key)
        else:
            return default
