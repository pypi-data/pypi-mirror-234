# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import os
import click

from .._base_opts_params import EnumChoice, CMDTRAIT_X11, CMDTYPE_BUILTIN
from .._decorators import (
    cli_pass_context,
    catch_and_log_and_exit,
    cli_option,
    cli_argument,
    cli_command,
)
from es7s.shared import run_subprocess


class EventStyle(str, enum.Enum):  # @TODO str enums will be avilable in python 3.11
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

    @property
    def filename(self) -> str:
        return STYLE_TO_ICON_MAP.get(self, "info")

    def __str__(self):
        return self.value


STYLE_TO_ICON_MAP: dict = {
    EventStyle.INFO: "info",
    EventStyle.WARNING: "emblem-ohno",
    EventStyle.ERROR: "dialog-close",
    EventStyle.SUCCESS: "dialog-ok",
}


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="create and send a notification",
)
@cli_argument("ident")
@cli_argument("message")
@cli_option(
    "-s",
    "--style",
    type=EnumChoice(EventStyle, inline_choices=True),
    default=EventStyle.INFO,
    show_default=True,
    metavar="NAME",
    help="Event style.",
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, ctx: click.Context, ident: str, message: str, style: EventStyle, **kwargs):
        match ident:
            case "pytermor":
                icon = "/home/a.shavykin/dl/pytermor/docs/_static_src/logo-white-bg.svg"
            case "es7s/core":
                icon = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logo.svg")
            case _:
                icon = style.filename

        run_subprocess(  # @temp
            "notify-send",
            "-i",
            icon,
            ident,
            message,
            check=True,
        )
