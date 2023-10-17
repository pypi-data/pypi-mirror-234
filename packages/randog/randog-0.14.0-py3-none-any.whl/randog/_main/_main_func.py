import csv
import datetime
import itertools
import json
import os
import random
import sys
import typing as t
import warnings

import randog.factory
from . import Args, Subcmd, get_subcmd_def
from ._logging import (
    logger,
    apply_stderr_logging_config,
    apply_logging_config_file,
    apply_default_logging_config,
)
from ._rnd import construct_random
from ._warning import RandogCmdWarning, apply_formatwarning
from .._utils.exceptions import get_message_recursive
from ..factory import FactoryDef, FactoryStopException


def _build_factories(
    args: Args,
) -> t.Iterator[t.Tuple[int, str, randog.factory.Factory]]:
    subcmd_def = get_subcmd_def(args.sub_cmd)

    if args.sub_cmd == Subcmd.Byfile:
        for factory_count, filepath in enumerate(args.factories):
            rnd = construct_random(args.seed)
            if filepath == "-":
                def_file_name = ""
                factory_def = randog.factory.from_pyfile(
                    sys.stdin, full_response=True, rnd=rnd
                )
            else:
                def_file_name = os.path.basename(filepath)
                if def_file_name.endswith(".py"):
                    def_file_name = def_file_name[:-3]
                factory_def = randog.factory.from_pyfile(
                    filepath, full_response=True, rnd=rnd
                )
            factory = factory_def.factory

            post_process = _gen_post_function_for_byfile_mode(args, factory_def)
            if post_process is not None:
                factory = factory.post_process(post_process)

            yield factory_count, def_file_name, factory
    else:
        iargs, kwargs = subcmd_def.build_args(args)
        construct_factory = subcmd_def.get_factory_constructor()
        logger.debug(
            "construct factory: %s",
            _repr_function_call(construct_factory, iargs, kwargs),
        )
        factory = construct_factory(*iargs, **kwargs)
        if args.iso:
            factory = factory.post_process(
                lambda x: x.isoformat() if x is not None else None
            )
        elif args.format:
            factory = factory.post_process(
                lambda x: format(x, args.format) if x is not None else None
            )
        yield 0, "", factory


def _get_csv_field(pre_value: t.Mapping, col) -> t.Any:
    if isinstance(col, t.Callable):
        return col(pre_value)
    else:
        return pre_value.get(col)


def _gen_post_function_for_byfile_mode(
    args: Args, factory_def: FactoryDef
) -> t.Optional[t.Callable[[t.Any], t.Any]]:
    """args に応じて、factory_def.factory に適用する post_process 関数を作成する。

    この関数は、byfile モードでのみ使用する。
    """
    if args.sub_cmd is not Subcmd.Byfile:
        raise RuntimeError("internal error; Unexpected function call")

    # CSV 出力の場合、CSVの行 (Sequence[Any]) を生成するような post_process を作成する。
    if args.get("csv", False):
        if factory_def.csv_columns is not None:

            def _post_function(pre_value) -> t.Optional[t.Sequence[t.Any]]:
                if pre_value is None:
                    return None
                elif isinstance(pre_value, t.Mapping):
                    return [
                        _get_csv_field(pre_value, col)
                        for col in factory_def.csv_columns
                    ]
                elif isinstance(pre_value, t.Sequence) and not isinstance(
                    pre_value, str
                ):
                    return pre_value
                else:
                    warnings.warn(
                        "--csv is recommended for only collections (such as "
                        "dict, list, tuple, etc.); "
                        "In CSV output, one generated value is treated as one row, "
                        "so the result is the same as --repeat except for collections; "
                        "CSV_COLUMNS in the definition file is ignored.",
                        RandogCmdWarning,
                    )
                    return [pre_value]

        else:

            def _post_function(pre_value) -> t.Optional[t.Sequence[t.Any]]:
                if pre_value is None:
                    return None
                elif isinstance(pre_value, t.Mapping):
                    # Why msg_part is defined:
                    #   Consider the possibility that future modifications will allow
                    #   users to reach here in other than byfile mode,
                    #   and branch the error message.
                    msg_part = (
                        " in the definition file"
                        if args.sub_cmd is Subcmd.Byfile
                        else ""
                    )
                    warnings.warn(
                        f"Since CSV_COLUMNS is not defined{msg_part}, "
                        "the fields are inserted in the order returned by the "
                        "dictionary; In this case, fields may not be aligned "
                        "depending on the FACTORY definition, "
                        "so it is recommended to define CSV_COLUMNS.",
                        RandogCmdWarning,
                    )
                    return list(pre_value.values())
                elif isinstance(pre_value, t.Sequence) and not isinstance(
                    pre_value, str
                ):
                    return pre_value
                else:
                    warnings.warn(
                        "--csv is recommended for only collections (such as "
                        "dict, list, tuple, etc.); "
                        "In CSV output, one generated value is treated as one row, "
                        "so the result is the same as --repeat except for collections.",
                        RandogCmdWarning,
                    )
                    return [pre_value]

        return _post_function
    else:
        return None


class _DummyIO:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _open_output_fp(
    args: Args,
    number: int,
    *,
    def_file: str,
    repeat_count: int,
    factory_count: int,
    now: datetime.datetime,
    already_written_files: t.MutableSet[str],
) -> t.Union[_DummyIO, t.TextIO]:
    output_path = args.output_path_for(
        number,
        def_file=def_file,
        repeat_count=repeat_count,
        factory_count=factory_count,
        now=now,
        env=os.environ,
    )

    if output_path is None:
        return _DummyIO()
    else:
        options = {}

        if output_path in already_written_files:
            options["mode"] = "at"
        else:
            options["mode"] = "wt"
            already_written_files.add(output_path)

        if args.get("csv", False):
            options["newline"] = ""
        elif args.output_linesep is not None:
            options["newline"] = args.output_linesep

        if args.output_encoding is not None:
            options["encoding"] = args.output_encoding

        logger.debug(f"open file: {output_path}")

        return open(output_path, **options)


def _output_generated(generated: t.Any, fp: t.TextIO, args: Args):
    if args.output_fmt == "repr":
        print(repr(generated), file=fp)
    elif args.output_fmt == "json":
        json.dump(generated, fp, default=str)
        fp.write("\n")
    else:
        print(generated, file=fp)


def _output_to_csv(
    factory: randog.factory.Factory[t.Optional[t.Sequence[t.Sequence[t.Any]]]],
    line_num: int,
    fp: t.TextIO,
    regenerate: float,
    discard: float,
    raise_on_factory_stopped: bool,
    linesep: t.Optional[str],
):
    writer_options = {}
    if fp in (sys.stdout, sys.stderr):
        # windows で "\r\n" にすると、標準出力時に改行が "\r\r\n" に変換されてしまう。
        # よって、windows で改行を "\r\n" にしたい場合も、標準出力時はここには　"\n" を指定する。
        writer_options["lineterminator"] = "\n"
    elif linesep is None:
        writer_options["lineterminator"] = os.linesep
    else:
        writer_options["lineterminator"] = linesep

    csv_writer = csv.writer(fp, **writer_options)
    csv_writer.writerows(
        filter(
            lambda x: x is not None,
            factory.iter(
                line_num,
                regenerate=regenerate,
                discard=discard,
                raise_on_factory_stopped=raise_on_factory_stopped,
            ),
        )
    )


class _Discarded(Exception):
    pass


def _generate_according_args(
    args: Args,
    factory: randog.factory.Factory,
) -> t.Tuple[t.Any, t.Literal["generated", "stop_iter", "discarded"]]:
    """generated a value according arguments

    This method generates values assuming it is not a csv output.

    Parameters
    ----------
    args
        the arguments
    factory
        the factory

    Returns
    -------
    Tuple[Any, Literal["generated", "stop_iter", "discarded"]]
        the generated value and a return type

    Raises
    ------
    RuntimeError
        When CSV output is specified.
        This method generates values assuming it is not a csv output.
    """
    if args.csv:
        raise RuntimeError("cannot use this method if --csv is specified")

    if args.list is not None:
        generated = list(
            factory.iter(
                args.list,
                regenerate=args.regenerate,
                discard=args.discard,
                raise_on_factory_stopped=args.error_on_factory_stopped,
            )
        )
    else:
        try:
            while True:
                generated = factory.next(
                    raise_on_factory_stopped=args.error_on_factory_stopped
                )
                if random.random() >= args.regenerate:
                    break
        except StopIteration:
            return None, "stop_iter"
        if random.random() < args.discard:
            return None, "discarded"

    return generated, "generated"


def _setup_primary_configuration(args: Args):
    """Setup primary python configuration

    It performs a setup that should be performed as soon as the arguments are
    determined in accordance with the python specification.

    This method should be executed once and only once when randog is run as command.

    Parameters
    ----------
    args:
        arguments of command execution
    """

    # setup logging
    if args.log_stderr:
        apply_stderr_logging_config(args.log_stderr, args.log_stderr_is_full)
    elif args.log_config_file:
        try:
            apply_logging_config_file(args.log_config_file)
        except Exception as e:
            logger.error(
                "failed to apply the logging configure file; "
                f"{'; '.join(get_message_recursive(e))}",
            )
            # If yaml is missed, warn about it, as that might cause Exception
            try:
                import yaml

                assert yaml is not None
            except ModuleNotFoundError:
                logger.error(
                    "Are you trying to use YAML format logging configuration? "
                    "If you want to use YAML format configuration files, "
                    "PyYAML must be installed."
                )
            exit(1)
    else:
        apply_default_logging_config()

    # setup warning
    if args.hide_randog_warnings:
        warnings.simplefilter("ignore", RandogCmdWarning)


def main():
    apply_formatwarning()

    args = Args(sys.argv)
    now = datetime.datetime.now()
    already_written_files = set()

    _setup_primary_configuration(args)

    # set environments
    os.environ.update(args.env)

    logger.info(f"run randog with args: {args.commanded_args}")

    try:
        index = 0
        for factory_count, def_file, factory in _build_factories(args):
            for r_index in range(args.repeat):
                with _open_output_fp(
                    args,
                    index,
                    def_file=def_file,
                    repeat_count=r_index,
                    factory_count=factory_count,
                    now=now,
                    already_written_files=already_written_files,
                ) as fp_opened:
                    index += 1
                    # args に応じて出力先 fp を決定する。
                    if not isinstance(fp_opened, _DummyIO):
                        fp = fp_opened
                    else:
                        fp = sys.stdout

                    # 生成処理と出力処理
                    # CSV 出力の場合に生成の方法が異なるので、生成と出力をひとまとめにした。
                    if args.csv is not None:
                        _output_to_csv(
                            factory,
                            args.csv,
                            fp,
                            regenerate=args.regenerate,
                            discard=args.discard,
                            raise_on_factory_stopped=args.error_on_factory_stopped,
                            linesep=args.output_linesep,
                        )
                        logger.debug(
                            "output to CSV; "
                            f"factory_count={factory_count}, repeat_count={r_index}"
                        )
                    else:
                        generated, gen_result = _generate_according_args(args, factory)

                        if gen_result == "stop_iter":
                            break
                        elif gen_result == "discarded":
                            continue
                        else:
                            _output_generated(generated, fp, args=args)
                            logger.debug(
                                "output generated; "
                                f"factory_count={factory_count}, repeat_count={r_index}"
                            )
    except FactoryStopException:
        logger.error("the factory stopped generating before the process was complete")
        exit(1)
    except Exception as e:
        logger.error("; ".join(get_message_recursive(e)), exc_info=e)
        exit(1)


def _repr_function_call(
    func_name: t.Union[str, t.Callable],
    args: t.Sequence[t.Any],
    kwargs: t.Mapping[str, t.Any],
) -> str:
    if not isinstance(func_name, str):
        func_name = getattr(func_name, "__name__", "function")

    args_str = itertools.chain(
        (repr(arg) for arg in args),
        (f"{key}={repr(value)}" for key, value in kwargs.items()),
    )
    return f"{func_name}({', '.join(args_str)})"
