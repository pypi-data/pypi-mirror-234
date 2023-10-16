# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import sys
import typing as t
from functools import update_wrapper

import click
from click import Argument
from click.decorators import _param_memo

from es7s.shared import get_logger, get_stderr, exit_gracefully
from ._base import CliGroup, CliCommand
from ._base_opts_params import HelpPart, CommandOption, CMDTYPE_BUILTIN, CommandType, EnumChoice
from ..shared.uconfig import get_merged

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
FC = t.TypeVar("FC", bound=t.Union[t.Callable[..., t.Any], click.Command])


def catch_and_log_and_exit(func: F) -> F:
    def wrapper(*args, **kwargs):
        logger = get_logger()
        try:
            logger.debug(f"Entering: '{func.__module__}'")
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            exit_gracefully(exit_code=1)
        except SystemExit as e:
            logger.debug(f"SystemExit: {e.args}")
        else:
            logger.debug(f"Leaving: '{func.__module__}'")
        return func

    return update_wrapper(t.cast(F, wrapper), func)


def catch_and_print(func: F) -> F:
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            if stderr := get_stderr(require=False):
                stderr.echo("ERROR")
            else:
                sys.stderr.write("ERROR\n")
            raise
        return func

    return update_wrapper(t.cast(F, wrapper), func)


def cli_group(
    name: str,
    short_help: str = None,
    epilog: str | HelpPart | list[str | HelpPart] = None,
    autodiscover_extras: "AutoDiscoverExtras" = None,
    **attrs: t.Any,
) -> CliGroup:
    if attrs.get("cls") is None:
        attrs["cls"] = CliGroup
    attrs.setdefault("short_help", short_help)
    attrs.setdefault("epilog", epilog)
    attrs.setdefault("autodiscover_extras", autodiscover_extras)

    return t.cast(CliGroup, click.group(name, **attrs))


def cli_command(
    name: str,
    short_help: str = None,
    cls: type = CliCommand,
    type: CommandType = CMDTYPE_BUILTIN,
    command_examples: list[str] = [],
    output_examples: list[str] = [],
    **attrs: t.Any,
) -> CliCommand:
    attrs.setdefault("short_help", short_help)
    attrs.setdefault("type", type)
    attrs.update(
        {
            "command_examples": command_examples,
            "output_examples": output_examples,
        }
    )

    return t.cast(CliCommand, click.command(name, cls, **attrs))


def _handle_from_config_attr(invoker, attrs: t.Any):
    if n := attrs.pop("from_config", None):
        fb = attrs.get("default", None)

        deferred_load = (
            lambda o=invoker, n=n, fb=fb: get_merged().get_module_section(o).get(n, fallback=fb)
        )
        attrs.update({"default": deferred_load})


def cli_argument(*param_decls: str, **attrs: t.Any) -> t.Callable[[FC], FC]:
    def decorator(f: FC) -> FC:
        _handle_from_config_attr(f, attrs)
        ArgumentClass = attrs.pop("cls", None) or Argument
        _param_memo(f, ArgumentClass(param_decls, **attrs))
        return f

    return decorator


def cli_option(
    *param_decls: str,
    help: str,
    cls=CommandOption,
    **attrs: t.Any,
) -> t.Callable[[FC], FC]:
    opt_type = attrs.get("type")
    if isinstance(opt_type, EnumChoice) and opt_type.inline_choices:
        help += opt_type.get_choices()
    attrs.setdefault("help", help)

    def decorator(f: FC) -> FC:
        _handle_from_config_attr(f, attrs)
        option_attrs = attrs.copy()
        OptionClass = cls or option_attrs.pop("cls", CommandOption)
        _param_memo(f, OptionClass(param_decls, **option_attrs))
        return f

    return decorator


cli_pass_context = click.pass_context
