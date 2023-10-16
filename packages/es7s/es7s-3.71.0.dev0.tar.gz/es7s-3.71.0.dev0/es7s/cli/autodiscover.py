# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import re
import typing as t
from functools import lru_cache
from importlib.abc import Traversable
from typing import Iterable

import pytermor as pt

from es7s.shared import get_logger, get_app_config_yaml, get_stdout, Styles
from ._base import CliGroup, CliCommand, Context, HelpFormatter, InvokerT
from ._base_opts_params import (
    CMDTYPE_INTEGRATED,
    CMDTRAIT_TEMPLATE,
    CommandType,
    CMDTYPE_INVALID,
)
from ._decorators import catch_and_log_and_exit, cli_command, cli_pass_context

AutoDiscoverExtras = t.Callable[[], Iterable["CliBaseCommand"]]


class AutoDiscover:
    @classmethod
    @lru_cache
    def get_config(cls, name: str) -> dict[str]:
        try:
            return get_app_config_yaml(name)
        except FileNotFoundError as e:
            get_logger(require=False).error(e)
        return {}

    @classmethod
    def run(cls, command, filepath, extras: AutoDiscoverExtras = None):
        import importlib.resources

        subpkg = os.path.relpath(os.path.dirname(filepath), os.path.dirname(__file__))
        pkg = (__package__ + "." + subpkg.replace("/", ".")).rstrip(".")

        for el in importlib.resources.files(pkg).iterdir():
            if el.name.startswith("_"):
                continue
            try:
                if cmd := cls._element_to_command(el, pkg):
                    command.add_command(cmd)
            except Exception as e:
                target = f"{subpkg}/{el.name}" + ("/" if el.is_dir() else "")
                get_logger(require=False).warning('Autodiscover skipping "%s": %s' % (target, e))
                command.add_command(InvalidCommandPlaceholder(el.name, CMDTYPE_INVALID, e))

        if extras:
            command.add_commands(extras())

        if isinstance(command, CliGroup) and not len(command.get_commands()):
            get_logger(require=False).warning(f"Empty command group: {pt.get_qname(command)}")

    @classmethod
    def _element_to_command(cls, el: Traversable, pkg: str) -> t.Any:
        name, ext = os.path.splitext(el.name)
        cfgkey = f"{pkg}.{name}"

        if el.is_dir() or (el.is_file() and el.name.startswith("_group")):
            if cfgs := AutoDiscover.get_config("cmd-autogroup"):
                return cls._register_group(el, pkg, cfgs.get(cfgkey))
            raise RuntimeError(f"No group config for {str(el)!r}")

        if el.is_file() and ext:
            if re.match(r"^\.", name) or re.match(r"\..*_$", ext):  # skipping temporary files
                return None
            match ext:
                case ".py":
                    return cls._register_builtin(f".{name}", pkg)
                case ".txt":
                    if cfgs := AutoDiscover.get_config("cmd-template"):
                        return cls._register_template(el, pkg, cfgs.get(cfgkey))
                case ".sh":
                    if cfgs := AutoDiscover.get_config("cmd-integrated"):
                        return cls._register_integrated(el, pkg, cfgs.get(cfgkey))
                case _:
                    raise RuntimeError(f"Unknown extension: {el}")
            raise RuntimeError(f"No command config for {str(el)!r}")
        raise RuntimeError(f"Unknown element at {str(el)!r}")

    @classmethod
    def _register_group(cls, el: Traversable, pkg: str, cfg: dict) -> t.Any:
        import importlib

        name = el.name.removesuffix(".py")
        mod = importlib.import_module("." + name, pkg)

        if fn := getattr(mod, "group", None):
            return fn

        from ._decorators import cli_group

        extras = getattr(mod, "autodiscover_extras", None)
        filepath = os.path.abspath(str(el.joinpath("__init__.py")))
        grp = cli_group(name=filepath, autodiscover_extras=extras, **cfg)(lambda: None)
        return grp

    @classmethod
    def _register_builtin(cls, modname: str, pkg: str) -> InvokerT | None:
        import importlib

        mod = importlib.import_module(modname, pkg)
        return getattr(mod, "invoker", None)

    @classmethod
    def _register_template(cls, el: Traversable, pkg: str, cfg: dict) -> t.Any:
        from ._template import TemplateCommand

        filepath = os.path.abspath(str(el))
        scmd = lambda filepath=filepath: TemplateCommand(filepath).run()
        scmd = catch_and_log_and_exit(scmd)
        scmd = cli_command(
            name=el.name,
            traits=[CMDTRAIT_TEMPLATE],
            **(cfg or dict(help=f"/*substitute {os.path.basename(el)}*/")),
        )(scmd)
        return scmd

    @classmethod
    def _register_integrated(cls, el: Traversable, pkg: str, cfg: dict) -> t.Any:
        from ._foreign import ForeignCommand

        cfg = cfg or dict(short_help=f"/*run {os.path.basename(el)}*/")
        fcmd = ForeignCommand(os.path.abspath(str(el)), cfg, CMDTYPE_INTEGRATED)
        return fcmd


class InvalidCommandCliPlaceholder(CliCommand):
    def __init__(self, **kwargs):
        self._err: Exception = kwargs.pop("err")
        super().__init__(**kwargs)

    def run(self):
        get_logger().exception(self._err)
        raise RuntimeError(f"Command load failed") from self._err

    def format_help(self, ctx: Context, formatter: HelpFormatter):
        super().format_help(ctx, formatter)
        formatter.write_paragraph()
        with formatter.indentation():
            formatter.write_text(get_stdout().render(self._format_error(), Styles.ERROR_ACCENT))
        get_stdout().echo(formatter.getvalue())
        formatter.buffer.clear()

    def _format_error(self) -> str:
        err_cls = pt.get_qname(self._err)
        return f"{err_cls}: {self._err}"

    def _make_short_help(self, **kwargs) -> str:
        return f"++Load++ ++failed:++ /*{self._err}*/"


def InvalidCommandPlaceholder(name: str, type: CommandType, err: Exception):
    cmd = lambda ctx: ctx.command.run()
    cmd = catch_and_log_and_exit(cmd)
    cmd = cli_pass_context(cmd)
    cmd = cli_command(
        name=name,
        cls=InvalidCommandCliPlaceholder,
        type=type,
        ignore_unknown_options=True,
        allow_extra_args=True,
        include_common_options_epilog=False,
        err=err,
    )(cmd)
    return cmd
