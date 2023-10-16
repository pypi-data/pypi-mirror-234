from __future__ import annotations

import abc
import enum
import typing as t
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar

import click
import pytermor as pt

from es7s.shared import FrozenStyle

OPTION_DEFAULT = object()

# -----------------------------------------------------------------------------
# Parameter types


class IntRange(click.IntRange):
    """
    ...
    """
    def __init__(
        self,
        _min: int = None,
        _max: int = None,
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
        show_range: bool = True,
    ):
        self._show_range = show_range
        super().__init__(_min, _max, min_open, max_open, clamp)

    def get_metavar(self, param: click.Parameter = None) -> t.Optional[str]:
        return "N"

    def _describe_range(self) -> str:
        if not self._show_range:
            return ""
        return super()._describe_range().replace("x", self.get_metavar())


class FloatRange(click.FloatRange):
    def __init__(
        self,
        _min: float = None,
        _max: float = None,
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
        show_range: bool = True,
    ):
        self._show_range = show_range
        self._range_filters = [
            pt.StringReplacer("x", lambda _: self.get_metavar()),
            pt.StringReplacer("inf", "∞"),
        ]
        super().__init__(_min, _max, min_open, max_open, clamp)

    def get_metavar(self, param: click.Parameter = None) -> t.Optional[str]:
        return "X"

    def _describe_range(self) -> str:
        if not self._show_range:
            return ""
        return pt.apply_filters(super()._describe_range(), *self._range_filters)


class EnumChoice(click.Choice):
    """
    Note: `show_choices` is ignored if param has custom metavar. That's because
    both metavar and choices in the left column of parameter list in --help mode
    look like shit and mess up the whole table. In case you need to set a metavar
    and to display choices at the same, add the latter into "help" message
    by setting `inline_choices` to True.
    """

    def __init__(self, impl: t.Any | enum.Enum, show_choices=True, inline_choices=False):
        self.__impl = impl
        self._show_choices = show_choices
        self.inline_choices = inline_choices
        super().__init__(choices=[item.value for item in impl], case_sensitive=False)

    def get_metavar(self, param: click.Parameter) -> str:
        if not self._show_choices:
            return ""
        return super().get_metavar(param)

    def get_choices(self) -> str:
        return " [" + "|".join(iter(self.__impl)) + "]"

    def convert(self, value, param, ctx):
        if value is None or isinstance(value, enum.Enum):
            return value

        converted_str = super().convert(value, param, ctx)
        return self.__impl(converted_str)


class IpParamType(click.ParamType):
    name = "ip"

    def convert(
        self,
        value: t.Any,
        param: t.Optional[click.Parameter],
        ctx: t.Optional[click.Context],
    ) -> t.Any:
        import ipaddress

        if not value:
            return None

        try:
            return ipaddress.ip_address(value)
        except ValueError:
            self.fail(f"{value!r} is not a valid IP.", param, ctx)

    def __repr__(self) -> str:
        return "IP"


class OptionScope(str, enum.Enum):
    COMMON = "Common options"
    GROUP = "Group options"
    COMMAND = "Options"

    def __str__(self):
        return self.value


# -----------------------------------------------------------------------------
# Command options


class ScopedOption(click.Option, metaclass=abc.ABCMeta):
    @property
    @abstractmethod
    def scope(self) -> OptionScope:
        raise NotImplementedError

    def has_argument(self):
        if isinstance(self.type, click.IntRange):
            return not self.count
        return isinstance(
            self.type,
            (
                click.FloatRange,
                click.Choice,
                click.DateTime,
            ),
        )


class CommonOption(ScopedOption):
    scope = OptionScope.COMMON


class GroupOption(ScopedOption):
    scope = OptionScope.GROUP


class CommandOption(ScopedOption):
    scope = OptionScope.COMMAND


class DayMonthOption(CommandOption):
    _date_formats = ["%b-%d", "%m-%d", "%d-%b", "%d-%b", "%b%d", "%m%d", "%d%b", "%d%m"]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("type", click.DateTime(self._date_formats))
        kwargs.setdefault("show_default", "current")
        kwargs.setdefault("metavar", "DD-MM")

        if kwargs.get("help") == OPTION_DEFAULT:
            kwargs.update(
                {
                    "help": "Date of interest, where DD is a number between 1 and 31, and MM is "
                    "either a number between 1 and 12 or month short name (first 3 characters). "
                    "MM-DD format is also accepted. Hyphen can be omitted.",
                }
            )
        super().__init__(*args, **kwargs)


# -----------------------------------------------------------------------------
# Command description

@dataclass(frozen=True)
class Section:
    title: str
    content: t.Sequence[str]

    def __bool__(self) -> bool:
        return len(self.content) > 0


@dataclass()
class HelpPart:
    text: str
    title: str = None
    group: str = None
    indent_shift: int = 0


EPILOG_COMMAND_HELP = HelpPart(
    "Run '%s' 'COMMAND' '--help' to get the COMMAND usage details (e.g. '%s' '%s' '--help').",
    group="run",
)
EPILOG_COMMON_OPTIONS = HelpPart(
    "Run 'es7s help options' to see common options details ('-v', '-Q', '-c', '-C', '--tmux', "
    "'--default').",
    group="run",
)
EPILOG_ARGS_NOTE = HelpPart(
    "Mandatory or optional arguments to long options are also mandatory or optional for any "
    "corresponding short options."
)


# -----------------------------------------------------------------------------
# Command types


@dataclass(frozen=True)
class CommandAttribute:
    name: str
    char: str
    sorter: int
    description: str
    hidden: bool
    char_big: str  # for "own" format
    fmt: pt.FT

    _values: ClassVar[set[CommandAttribute]] = set()
    _map: ClassVar[dict[str, CommandAttribute]] = dict()

    @classmethod
    def get(cls, name: str) -> CommandAttribute | None:
        return cls._map.get(name, None)

    def __post_init__(self):
        self._values.add(self)
        self._map[self.name] = self

    @abstractmethod
    def get_own_char(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_own_fmt(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_own_label_fmt(self) -> pt.FT:
        raise NotImplementedError

    @abstractmethod
    def get_icon_char_fmt(self) -> pt.FT:
        raise NotImplementedError

    def __eq__(self, other: CommandAttribute) -> bool:
        if not isinstance(other, CommandAttribute):
            return False
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(f"{self.name}{self.sorter}{self.description}")


@dataclass(frozen=True)
class CommandType(CommandAttribute):
    DEFAULT_FMT = FrozenStyle(fg=pt.cv.BLUE)
    HIDDEN_FMT = FrozenStyle(fg=pt.cv.GRAY_35)

    name: str
    char: str
    sorter: int
    description: str = ""
    hidden: bool = False
    char_big: str = None
    fmt: pt.FT = pt.NOOP_STYLE

    def get_own_char(self) -> str:
        return f'{self.char_big or self.char or " ":^3s}'

    def get_own_fmt(self) -> pt.Style:
        base = self.get_icon_char_fmt()
        return FrozenStyle(base, fg=0xFFFFFF, bg=base.fg, dim=True, bold=True)

    def get_own_label_fmt(self) -> pt.FT:
        return self.fmt or self.DEFAULT_FMT

    def get_icon_char_fmt(self, trait: CommandTrait = None) -> pt.Style:
        return pt.merge_styles(
            self.DEFAULT_FMT,
            overwrites=[*filter(None, (trait, self.fmt, FrozenStyle(bold=True)))],
        )

    def get_name_fmt(self) -> pt.Style:
        if self.hidden:
            return self.HIDDEN_FMT
        return self.DEFAULT_FMT

    def __hash__(self) -> int:
        return super().__hash__()


@dataclass(frozen=True)
class CommandTrait(CommandAttribute):
    CHAR = "◩"  # "■"

    name: str | None = None
    char: str = CHAR
    sorter: int = 0
    description: str = ""
    hidden: bool = False
    char_big: str = None
    fmt: pt.FT = CommandType.DEFAULT_FMT

    def get_own_char(self) -> str:
        return self.CHAR

    def get_own_fmt(self) -> pt.FT:
        return self.fmt

    def get_own_label_fmt(self) -> pt.FT:
        return self.fmt

    def get_icon_char_fmt(self) -> pt.FT:
        return pt.Style(self.fmt)

    def __hash__(self) -> int:
        return super().__hash__()


CMDTYPE_INVALID = CommandType(
    name="invalid",
    hidden=True,
    char="×",
    sorter=0,
    fmt=FrozenStyle(fg=pt.cv.RED),
    description="Something is wrong and this command could not be loaded; therefore, "
                "no help can be shown either. Consider running the same command, but "
                "with '-vv' flag to see the details.",
)
CMDTYPE_GROUP = CommandType(
    name="group",
    char="+",
    sorter=10,
    fmt=FrozenStyle(fg=pt.cv.YELLOW),
    description="This command %s|contains|other commands.",
)
CMDTYPE_BUILTIN = CommandType(
    name="builtin",
    char="·",
    sorter=15,
    char_big="∙",
    description="This is a %s|builtin|es7s/core component written in Python 3 (G2/G3).",
)
CMDTYPE_INTEGRATED = CommandType(
    name="integrated",
    char="~",
    sorter=20,
    description="This is an %s|integrated legacy|component included in es7s/core, "
    "which usually requires es7s/commons shell library (G1/G2).",
)
CMDTYPE_EXTERNAL = CommandType(
    name="external",
    char="^",
    sorter=28,
    description="This is an %s|external standalone|component which is not included in "
    "es7s/core, but is (usually) installed as a part of es7s system. Shell/Golang (G1/G4). "
    "Can be launched directly.",
)

CMDTRAIT_NONE = CommandTrait(
    hidden=True,
)
CMDTRAIT_TEMPLATE = CommandTrait(
    name="template",
    sorter=35,
    fmt=FrozenStyle(fg=pt.cv.GRAY_70),
    description="Source is a %s|static|template.",
)
CMDTRAIT_ADAPTIVE = CommandTrait(
    name="adaptive",
    sorter=40,
    fmt=FrozenStyle(fg=pt.cv.GREEN),
    description="The output is %s|adjusted|depending on terminal size.",
)
CMDTRAIT_X11 = CommandTrait(
    name="x11",
    sorter=50,
    fmt=FrozenStyle(fg=pt.cv.MAGENTA),
    description="Requires %s|X11|(GUI) environment.",
)
