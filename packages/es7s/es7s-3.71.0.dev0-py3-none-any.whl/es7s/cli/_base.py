# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import inspect
import re
import typing as t
from collections.abc import Iterable
from contextlib import contextmanager
from os.path import basename, dirname, splitext
from re import compile
from typing import ClassVar, cast, overload, TypeVar

import Levenshtein  # noqa (not listed in requirements)
import click
import pytermor as pt

from es7s import APP_NAME
from es7s.shared import (
    FrozenStyle,
    Styles,
    get_logger,
    get_stdout,
    LoggerSettings,
    uconfig,
)
from es7s.commons import format_attrs
from es7s.commons import NamedGroupsRefilter, RegexValRefilter
from es7s.commons import Regex
from es7s.shared.uconfig import UserConfigSection
from ._base_opts_params import (
    CMDTRAIT_NONE,
    CMDTYPE_BUILTIN,
    CMDTYPE_GROUP,
    CommandAttribute,
    CommandTrait,
    CommandType,
    EPILOG_ARGS_NOTE,
    EPILOG_COMMAND_HELP,
    EPILOG_COMMON_OPTIONS,
    HelpPart,
    OptionScope,
    Section,
    ScopedOption,
    CMDTYPE_EXTERNAL,
    CMDTYPE_INTEGRATED, CMDTYPE_INVALID,
)

FS = FrozenStyle


class base_invoker:
    @staticmethod
    @overload
    def uconfig(origin) -> UserConfigSection:
        ...

    @classmethod
    @overload
    def uconfig(cls) -> UserConfigSection:
        ...

    def uconfig(self) -> UserConfigSection:
        return uconfig.get_for(self)


InvokerT = TypeVar("InvokerT", bound=base_invoker)


# fmt: off
class HelpStyles(Styles):
    TEXT_HEADING = FS(fg=pt.cv.YELLOW, bold=True)          # ¯SYNOPSIS¯    | ¯ | also used by help formatter     # noqa
    TEXT_COMMAND_NAME = FS(fg=pt.cv.BLUE)                  # es7s exec     |   | auto-detection                  # noqa
    TEXT_OPTION_DEFAULT = FS(fg=pt.cv.HI_YELLOW)           # [default: 1]  |[ ]| requires wrapping in [ ]        # noqa
    TEXT_EXAMPLE = FS(fg=pt.cv.CYAN, bg='full-black')      # `4 11`        | ` | input/output example            # noqa
                                                           # ´4 11´        | ´ | ⤒ static-length I/O example     # noqa
    TEXT_ENV_VAR = FS(fg=pt.cv.GREEN, bold=True)           # @ES7S_LE_VAR@ |@ @| environment variable name       # noqa
                                                           # {ES7S_LE_VAR} |{ }| ⤒ static-length env var name    # noqa
    TEXT_ABOMINATION = FS(pt.Style(bg='blue').autopick_fg()) # ::NOTE::    |:: | needs to be wrapped in ::       # noqa
    TEXT_DEPENDENCY = FS(fg=pt.cv.RED, underlined=True)    # ++REQ++       |++ | ++required dependency++         # noqa
    TEXT_INLINE_CONFIG_VAR = FS(fg=pt.cv.MAGENTA)          # <section.opt> |< >| config variable name            # noqa
    TEXT_PLACEHOLDER = FS(italic=True, dim=True)           # <<filename>>  |<<>> placeholder                     # noqa
    TEXT_ALTER_MODE = FS(italic=True)                      # ^ALT MODE^    |^ ^| alt monitor mode                # noqa
    TEXT_COMMENT = FS(fg=pt.cv.GRAY)                       # // COMMENT    |// | till end of the line            # noqa
    TEXT_WALL = FS(fg=pt.cv.WHITE)                         # ░░░░░░░░      |░░░| "░" char in tables              # noqa
    TEXT_ABBREV_SINGLE = FS(fg=pt.cv.YELLOW, bold=True)    # &p &(gre)p    |&()| highlighed part of abbrev       # noqa
    TEXT_ABBREV_MULTI = FS(bold=True)                      #               &(..) highlighed part of abbrev       # noqa
    TEXT_ARGUMENT = FS(underlined=True)                    # FILE ARGUMENT |ABC| caps auto-detection             # noqa
    TEXT_LITERAL = FS(bold=True)                           # 'ls | cat'    | ' | non-es7s commands (punctuation) # noqa
    TEXT_LITERAL_WORDS = FS(underlined=True)               # 'ls | cat'    | ' | non-es7s commands (words)       # noqa
    TEXT_ACCENT = FS(bold=True)                            # *important*   | * | words  shrinked                 # noqa
                                                             #  '--option' | ' | options format   shrinked       # noqa
                                                             #  "--option" | " |                  any* expanded  # noqa
                                                             #  ""option"" |"" | -> 'option'      any* fixed     # noqa
    TEXT_KEY = FS(bold=True, underlined=True)              #  “*ON/OFF+”   |“ ”| ACCENTED ACCENT, any* shrinked  # noqa
# fmt: on


class NWMarkup:
    OPTION_REGEX = Regex(R"(?P<val>--?[\w-]+)")
    # language=regexp
    WRAP_REGEX = R"(?P<noop>\n\s*|)"

    class CommandTypeReplacer(pt.StringReplacer):
        COMMAND_TYPE_NAME_MAP: t.Dict[str, CommandAttribute] = {
            ct.name.lower(): ct for ct in CommandAttribute._values if ct.name
        }

        def __init__(self):
            names = "|".join(self.COMMAND_TYPE_NAME_MAP.keys())
            super().__init__(rf"\[\[({names})\]\]", self.replace)

        @classmethod
        def replace(cls, m: t.Match) -> str:
            if ct := cls.COMMAND_TYPE_NAME_MAP.get(m.group(1), None):
                return get_stdout().render(HelpFormatter.format_command_type_inlined(ct))
            return m.group()

    class LiteralReplacer(pt.StringReplacer):
        def __init__(self):
            super().__init__(
                Regex(Rf"(?<!\\)'{NWMarkup.WRAP_REGEX}([\w./ \n|=-]+?)'"),
                self.replace,
            )

        @classmethod
        def replace(cls, sm: re.Match) -> str:
            text_literal_is_present = False
            word_count = 0

            def replace_literal(wm: re.Match) -> str:
                nonlocal text_literal_is_present, word_count
                word_count += 1
                word = wm.group()
                if len(word) < 2 and not word.isalpha():  # bold instead of underline
                    text_literal_is_present = True  # for 1-character non-letters,
                    style = HelpStyles.TEXT_LITERAL  # e.g. for '|' pipe symbol.
                elif word in HelpFormatter.command_names or word.startswith(APP_NAME):
                    style = HelpStyles.TEXT_COMMAND_NAME
                elif word.startswith("-"):
                    style = HelpStyles.TEXT_ACCENT
                else:
                    text_literal_is_present = True
                    style = HelpStyles.TEXT_LITERAL_WORDS
                return get_stdout().render(word, style)

            replaced = re.sub(r"(\S+)", replace_literal, (sm.group(1) or "") + sm.group(2))
            if text_literal_is_present and word_count > 1:
                replaced = f"'{replaced}'"
            return replaced

    def __init__(self):
        self._filters: t.List[pt.StringReplacer] = [
            # (-2) ¯HEADER_NAME¯
            RegexValRefilter(
                Regex(Rf"¯{self.WRAP_REGEX}(?P<val>.+?)¯"),
                HelpStyles.TEXT_HEADING,
            ),
            # [ 0] CMD_ARGUMENT
            RegexValRefilter(
                Regex(R"(?P<val>(?<![{@`´<])\b[A-Z][A-Z0-9_]{3,})(s?\b)"),
                FS(underlined=True),
            ),
            # (-2) *TEXT*
            RegexValRefilter(
                Regex(R"(^|)?\*(?P<val>[\w!/.-]+?)\*"),
                HelpStyles.TEXT_ACCENT,
            ),
            # (**) 'es7s exec ls'
            self.LiteralReplacer(),
            # (-2) `dynamic result width`
            #  =>  dynamic result width    (result will be shorter by 2 chars)
            RegexValRefilter(
                Regex(Rf"`{self.WRAP_REGEX}(?P<val>.+?)`"),
                HelpStyles.TEXT_EXAMPLE,
            ),
            # [ 0] | ´FIXED RESULT WIDTH´ |
            #  =>  |  FIXED RESULT WIDTH  |  (post-markup-removing width compensation)
            pt.filter.StringReplacerChain(
                Regex(Rf"´.+?´"),
                RegexValRefilter(
                    Regex(Rf"´{self.WRAP_REGEX}(?P<val>.+?)´"),
                    HelpStyles.TEXT_EXAMPLE,
                ),
                pt.OmniPadder(),
            ),
            # (-2) <CONFIG_VAR>
            pt.StringReplacerChain(
                Regex(Rf"(?<!<)<{self.WRAP_REGEX}([\w\s.-]+?)>"),
                pt.StringReplacer(Regex("[<>]"), ""),
                RegexValRefilter(
                    Regex(R"(?P<val>[^.]+)"),
                    HelpStyles.TEXT_INLINE_CONFIG_VAR,
                ),
            ),
            # [ 0] | {ENVIRONMENT_VAR} |
            #  =>  |  ENVIRONMENT_VAR  |
            pt.StringReplacerChain(
                Regex(Rf"(\{{){self.WRAP_REGEX}([\w.*-]+?)(}})"),
                pt.StringReplacer(Regex(R"\{(.+)}"), r" \1 "),
                RegexValRefilter(
                    Regex(R"(?P<val>.+)"),
                    HelpStyles.TEXT_ENV_VAR,
                ),
            ),
            # (-2) @ENVIRONMENT_VAR@
            #  =>  ENVIRONMENT_VAR
            RegexValRefilter(
                Regex(r"@(?P<val>[()\w._-]+?)@"),
                HelpStyles.TEXT_ENV_VAR,
            ),
            # (-4) ++dependency++
            #  =>  dependency
            RegexValRefilter(
                Regex(r"\+\+(?P<val>[\w./-]+?:*)\+\+"),
                HelpStyles.TEXT_DEPENDENCY,
            ),
            # (±0) | ::LABEL:: |
            #  ≈>  |  #L#B#L#  |
            pt.StringReplacerChain(
                Regex(R"::(?P<val>[\w./-]+?:*)::"),
                pt.OmniPadder(2),
                NamedGroupsRefilter(
                    Regex(R"(?P<s1>\s)(\s)::(.+)::(\s)(?P<s2>\s)"),
                    {"": HelpStyles.TEXT_ABOMINATION},  # any
                ),
            ),
            # (-2)L //this is comment
            #  =>   this is comment
            RegexValRefilter(
                Regex(R"(^|\s+)//(?P<val>\s.+)"),
                HelpStyles.TEXT_COMMENT,
            ),
            # (-4) /*this is comment, too*/
            #  =>  this is comment, too
            RegexValRefilter(
                Regex(R"/\*(?P<val>.+?)\*/", dotall=True),
                HelpStyles.TEXT_COMMENT,
            ),
            # (±0) | [[builtin]] |
            #  ≈>  | #∙# builtin |
            self.CommandTypeReplacer(),
            # (-2) <<placeholder>>
            #  =>  <placeholder>
            NamedGroupsRefilter(
                Regex(Rf"<(<){self.WRAP_REGEX}([\w\s.-]+?)(>)>"),
                {"": HelpStyles.TEXT_PLACEHOLDER},  # any
            ),
            # (-2) 'important'
            #  =>  important
            RegexValRefilter(
                Regex(Rf"(?<!\\)'{self.WRAP_REGEX}{self.OPTION_REGEX.pattern}'"),
                HelpStyles.TEXT_ACCENT,
            ),
            # (-2) ""important""
            #  =>  "important"
            pt.filter.StringReplacerChain(
                Regex(Rf'(?<!\\)""[^\x1b]+?""'),
                RegexValRefilter(
                    Regex(Rf'"{self.WRAP_REGEX}(?P<val>".+?")"'),
                    HelpStyles.TEXT_ACCENT,
                ),
                pt.StringReplacer(Regex(R'"'), R"\""),
            ),
            # [ 0] | "important" |
            #  =>  |  important  |
            pt.filter.StringReplacerChain(
                Regex(Rf'(?<!\\)"[^\x1b]+?"'),
                RegexValRefilter(
                    Regex(Rf'"{self.WRAP_REGEX}(?P<val>.+?)"'),
                    HelpStyles.TEXT_ACCENT,
                ),
                pt.OmniPadder(),
            ),
            # (-2) “non-empty”
            #  =>  non-empty
            pt.filter.StringReplacerChain(
                Regex(R"“(.+?)”", dotall=True),
                NamedGroupsRefilter(
                    Regex(R"“(?P<val>.+?)”", dotall=True),
                    {"val": HelpStyles.TEXT_KEY},  # any
                ),
            ),
            # [ 0] ...texttext [default: 3 hours].
            RegexValRefilter(
                Regex(Rf"(default:){self.WRAP_REGEX}(?P<val>.+?)([];])"),
                HelpStyles.TEXT_OPTION_DEFAULT,
            ),
            # [ 0] ...texttext [which is a default].
            RegexValRefilter(
                Regex(Rf"(\[)([\w\s]+)(?P<val>default)(])"),
                HelpStyles.TEXT_OPTION_DEFAULT,
            ),
            # [ 0] | ^ALTERNATIVE^ |
            #  =>  |  ALTERNATIVE  |
            pt.filter.StringReplacerChain(
                Regex(Rf"\^.+?\^"),
                RegexValRefilter(
                    Regex(Rf"\^{self.WRAP_REGEX}(?P<val>.+?)\^"),
                    HelpStyles.TEXT_ALTER_MODE,
                ),
                pt.OmniPadder(),
            ),
            # [ 0] ░░░░░░░
            RegexValRefilter(
                Regex(R"(?P<val>░{2,})"),
                HelpStyles.TEXT_WALL,
            ),
            # (-1) &process ≈> Process
            # (-N) s&(ocks) ≈> sOCKS
            NamedGroupsRefilter(
                Regex(r"&(?:(?P<sval>\w)|\((?P<mval>\w+)\))"),
                {
                    "sval": HelpStyles.TEXT_ABBREV_SINGLE,
                    "mval": HelpStyles.TEXT_ABBREV_MULTI,
                },
            ),
            # (-1) it\'s
            #  =>  it's
            pt.StringReplacer(r"\\\'", "'"),
            # (-2) \"as is\"
            #  =>  "as is"
            pt.StringReplacer(r"\\\"", '"'),
        ]

    def apply(self, string: str) -> str:
        return pt.apply_filters(string, *self._filters)


class HelpFormatter(click.HelpFormatter):
    command_names: ClassVar[list[str]]

    def __init__(
        self,
        indent_increment: int = 2,
        width: t.Optional[int] = None,
        max_width: t.Optional[int] = None,
    ):
        width = pt.get_preferable_wrap_width(False)
        self._nwml = NWMarkup()
        super().__init__(indent_increment, width, max_width)

        if not hasattr(HelpFormatter, "command_names"):
            HelpFormatter.command_names = [APP_NAME]
            if (ctx := click.get_current_context(True)) is None:
                return
            HelpFormatter.command_names = self._find_all_command_names(ctx.find_root().command)

    def _find_all_command_names(self, command: click.Command) -> set[str]:
        names = set()
        names.add(command.name)
        if hasattr(command, "commands") and isinstance(command.commands, dict):
            for nested_command in command.commands.values():
                names = names.union(self._find_all_command_names(nested_command))
        return names

    @classmethod
    @overload
    def format_command_name(cls, cmd: CliBaseCommand) -> str:
        ...

    @classmethod
    @overload
    def format_command_name(cls, name: re.Match | str) -> str:
        ...

    @classmethod
    def format_command_name(cls, arg) -> str:
        if isinstance(arg, CliBaseCommand):
            ct = arg.get_command_type()
            return get_stdout().render(arg.name, ct.get_name_fmt())
        if isinstance(arg, re.Match):
            arg = arg.group(1)
        return get_stdout().render(arg, HelpStyles.TEXT_COMMAND_NAME)

    def format_accent(self, arg: re.Match | str) -> str:
        if isinstance(arg, re.Match):
            arg = arg.group(1) + arg.group(2)
        return get_stdout().render(arg, HelpStyles.TEXT_ACCENT)

    @contextmanager
    def section(self, name: str | None) -> t.Iterator[None]:
        # modified version of parent implementation; could not inject otherwise
        # changes: `name` is nullable now; do not write heading if `name` is empty
        self.write_paragraph()
        if name:
            self.write_heading(name)
        self.indent()
        try:
            yield
        finally:
            self.dedent()

    @classmethod
    def format_command_icon(cls, cmd: CliBaseCommand) -> pt.Fragment:
        ct = cmd.get_command_type()
        icon_char = ct.char
        icon_color = ct.get_icon_char_fmt(cmd.get_command_trait().fmt)
        return pt.Fragment(icon_char, icon_color)

    @classmethod
    def format_command_icon_and_name(cls, cmd: CliBaseCommand) -> pt.Text:
        return cls.format_command_icon(cmd) + " " + cls.format_command_name(cmd)

    @classmethod
    def format_command_attribute_legend(cls, ct: CommandType | CommandTrait) -> pt.Text:
        if isinstance(ct, CommandType):
            return (
                pt.Fragment("[")
                + pt.Fragment(ct.char, ct.get_icon_char_fmt())
                + pt.Fragment("] " + ct.name)
            )
        return pt.Fragment(f" {ct.char} ", ct.get_icon_char_fmt()) + pt.Fragment(" " + ct.name)

    @classmethod
    def format_command_type_inlined(cls, ct: CommandAttribute) -> pt.Text:
        return cls.format_command_own_type(ct) + pt.Fragment(" " + ct.name)

    @classmethod
    def format_command_own_type(cls, ct: CommandAttribute) -> pt.Fragment:
        return pt.Fragment(ct.get_own_char(), ct.get_own_fmt())

    def write_heading(
        self,
        heading: str,
        newline: bool = False,
        colon: bool = True,
        st: pt.Style = HelpStyles.TEXT_HEADING,
    ):
        # changes: styling of the header, optional newline
        heading = get_stdout().render(heading + (colon and ":" or ""), st)
        self.write(f"{'':>{self.current_indent}}{heading}")
        self.write_paragraph()
        if newline:
            self.write_paragraph()

    def write_text(self, text: str) -> None:
        # changes: sgr-aware wrapper, ⏺ list subseq indent handling
        indent_subseq_extra = self.indent_increment if text.lstrip().startswith("⏺") else 0
        self.write(
            pt.wrap_sgr(
                text,
                self.width,
                indent_first=self.current_indent,
                indent_subseq=self.current_indent + indent_subseq_extra,
            )
        )

    def write_squashed_text(self, string: str):
        wrapped_text = pt.wrap_sgr(
            string,
            self.width,
            indent_first=self.current_indent,
            indent_subseq=self.current_indent,
        )
        self.write(wrapped_text.replace("\n\n", "\n"))  # @REFACTOR wat
        self.write("\n")

    # def write(self, string: str) -> None:
    #     ...
    #     self.buffer.append(string)

    def _postprocess(self, string: str) -> str:
        stripped = string.strip()
        if stripped in HelpFormatter.command_names:
            string = get_stdout().render(string, HelpStyles.TEXT_COMMAND_NAME)
        return self._nwml.apply(string)

    def getvalue(self) -> str:
        return self._postprocess(super().getvalue())


class Context(click.Context):
    formatter_class = HelpFormatter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = False
        self.color = get_stdout().color
        self.logger_setup: LoggerSettings = get_logger().setup

    def fail(self, message: str):
        self.failed = True
        raise UsageError(message, ctx=self)


class UsageError(click.UsageError):
    def __init__(self, message: str, ctx: t.Optional[Context] = None) -> None:
        super().__init__(message, ctx)
        self.ctx = ctx

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if not self.ctx.logger_setup.print_usage_errors:
            return
        super().show(file)


class CliBaseCommand(click.Command):
    context_class = Context

    def __init__(self, name, **kwargs):
        kwargs.setdefault("type", CMDTYPE_BUILTIN)
        self._include_common_options_epilog = kwargs.pop("include_common_options_epilog", True)
        self._command_type: CommandType = kwargs.pop("type")
        self._command_traits: t.Sequence[CommandTrait] = kwargs.pop("traits", [])
        self._prolog = kwargs.pop("prolog", [])
        self._usage_section_name = kwargs.pop("usage_section_name", "Usage")

        base_name = name or kwargs.get("name")
        if ".py" in base_name:
            base_name = splitext(basename(base_name))
            self._file_name_parts = base_name[0].lstrip("_").split("_")
        else:
            self._file_name_parts = [base_name]

        context_settings = kwargs.pop("context_settings", {})
        context_settings_extras = {
            "ignore_unknown_options": kwargs.pop("ignore_unknown_options", None),
            "allow_extra_args": kwargs.pop("allow_extra_args", None),
        }
        context_settings.update(
            **{k: v for k, v in context_settings_extras.items() if v is not None}
        )

        super().__init__(name, context_settings=context_settings, **kwargs)

    def get_command_type(self) -> CommandType:
        return self._command_type

    def get_command_trait(self) -> CommandTrait:
        if self._command_traits:
            return self._command_traits[-1]
        return CMDTRAIT_NONE

    def parse_args(self, ctx: Context, args: t.List[str]) -> t.List[str]:
        get_logger().debug(f"Pre-click args:  {format_attrs(args)}")
        try:
            return super().parse_args(ctx, args)
        except click.UsageError as e:
            ctx.fail(e.format_message())

    def invoke(self, ctx: Context) -> t.Any:
        get_logger().debug(f"Post-click args: {format_attrs(ctx.params)}")
        try:
            return super().invoke(ctx)
        except click.ClickException as e:
            ctx.failed = True
            self.show_error(ctx, e)

    def show_error(self, ctx: Context, e: click.ClickException):
        logger = get_logger()
        logger.error(e.format_message())
        if not logger.setup.print_click_errors:
            return

        hint = ""
        if ctx.command.get_help_option(ctx):
            hint = f"\nTry '{ctx.command_path} {ctx.help_option_names[0]}' for help."
        get_stdout().echo(f"{ctx.get_usage()}\n{hint}")

    def _make_command_name(self, orig_name: str) -> str:
        dir_name = basename(dirname(orig_name))
        filename_parts = splitext(basename(orig_name))[0].rstrip("_").split("_")
        if filename_parts[0] == "":  # because of '_group' -> ['', 'group']
            filename_parts = [dir_name.rstrip("_")]  # 'exec_' -> 'exec'
        return "-".join(filename_parts)

    def _make_short_help(self, **kwargs) -> str:
        help_str = kwargs.get("help")
        if not help_str and not kwargs.get("prolog", None):
            get_logger(require=False).warning(f"Missing help for '{kwargs.get('name')}' command")
            help_str = "..."

        short_help = kwargs.get("short_help")
        short_help_auto = help_str.lower().removesuffix(".")
        if isinstance(short_help, t.Callable):
            return short_help(short_help_auto)
        elif short_help:
            return short_help
        return short_help_auto

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pieces = self.collect_usage_pieces(ctx)
        if self._command_type in [CMDTYPE_INTEGRATED, CMDTYPE_EXTERNAL]:
            pieces += ["[--", "PASSARGS]"]
        with formatter.section(self._usage_section_name):
            formatter.write_usage(
                formatter.format_command_name(ctx.command_path), " ".join(pieces), prefix=""
            )

    def format_own_type(self, ctx: Context, formatter: HelpFormatter):
        stdout = get_stdout()

        with formatter.indentation():
            descriptions = []
            for ct in [self.get_command_type(), self.get_command_trait()]:
                ct_icon = stdout.render(formatter.format_command_own_type(ct))
                ct_description = (
                    ct.description % ct_icon if "%s" in ct.description else ct.description
                )

                if ct_description.count("|") == 2:
                    left, hightlight, right = ct_description.split("|", 2)
                    descriptions.append(
                        (
                            stdout.render(left, HelpStyles.TEXT_COMMENT)
                            + stdout.render(" " + hightlight + " ", ct.get_own_label_fmt())
                            + stdout.render(right, HelpStyles.TEXT_COMMENT)
                        )
                    )
                elif ct == CMDTYPE_INVALID:
                    descriptions.append(stdout.render(ct_description, ct.get_own_label_fmt()))
                else:
                    descriptions.append(ct_description)

            formatter.write_paragraph()
            formatter.write_text("\n\n".join(filter(None, descriptions)))

    def format_common_options(self, ctx: Context, formatter: HelpFormatter, add_header: bool):
        if self._include_common_options_epilog:
            with formatter.section("Options" if add_header else ""):
                if add_header:
                    formatter.write_text("No specific options.")
                    formatter.write_paragraph()
                formatter.write_text(EPILOG_COMMON_OPTIONS.text)

    def format_prolog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, [*self._get_help_parts(ctx, self._prolog)])

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, [*self._get_help_parts(ctx, self.epilog)])

    def _get_help_parts(self, ctx: Context, src: t.Iterable[str | HelpPart]) -> t.Generator[list]:
        if src:
            if not isinstance(src, list):
                src = [src]
            yield from src

    def _format_help_parts(self, formatter: HelpFormatter, parts: list[HelpPart]):
        squashed_parts = []
        for idx, part in enumerate(parts):
            if (
                len(squashed_parts)
                and not part.title
                and part.group
                and part.group == squashed_parts[-1].group
            ):
                squashed_parts[-1].text += "\n\n" + part.text
                continue
            squashed_parts.append(part)

        for part in squashed_parts:
            self._format_epilog_part(formatter, part)

    def _format_epilog_part(self, formatter: HelpFormatter, part: HelpPart):
        part_indent = part.indent_shift * formatter.indent_increment
        formatter.current_indent += part_indent
        formatter.write_paragraph()
        if part.title:
            formatter.write_heading(part.title.capitalize(), newline=False, colon=False)

        with formatter.indentation():
            formatter.write_text(part.text)
        formatter.current_indent -= part_indent

    def _is_option_with_argument(self, option: click.Parameter) -> bool:
        if isinstance(option, ScopedOption):
            return option.has_argument()
        return False


class CliCommand(CliBaseCommand):
    option_scopes: list[OptionScope] = [
        OptionScope.COMMAND,
        OptionScope.GROUP,
    ]

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "name": self._make_command_name(kwargs.get("name")),
                "params": self._build_options(kwargs.get("params", [])),
                "short_help": self._make_short_help(**kwargs),
            }
        )
        self._command_examples = Section("Command examples", kwargs.pop("command_examples", []))
        self._output_examples = Section("Output examples", kwargs.pop("output_examples", []))
        self._ext_help_invoker: t.Callable[[Context], str] = kwargs.pop("ext_help_invoker", None)

        super().__init__(**kwargs)

    def _build_options(self, subclass_options: list[ScopedOption]) -> list[ScopedOption]:
        return [
            *subclass_options,
            *self._get_group_options(),
        ]

    def _get_group_options(self) -> list[ScopedOption]:
        return []

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        self.format_usage(ctx, formatter)
        self.format_prolog(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)
        self.format_examples(ctx, formatter, self._command_examples)

        if self._ext_help_invoker is None:
            return
        result_generic = formatter.getvalue()
        formatter.buffer.clear()

        seq_color_bg = f"{pt.cv.GRAY_15.to_sgr(pt.ColorTarget.BG)}"
        seq_color_bg_line = f"{seq_color_bg}{pt.make_clear_line_after_cursor()}"

        inject_bg_rr = pt.StringReplacer(
            pt.SGR_SEQ_REGEX,
            lambda m: m.group(0) + (seq_color_bg if self._has_bg_or_reset_param(m) else ""),
        )
        enclose_bg_rr = pt.StringReplacer(compile("(^|\n|$)"), rf"\1{seq_color_bg_line}")
        result_generic = pt.apply_filters(result_generic, inject_bg_rr, enclose_bg_rr) + str(
            pt.SeqIndex.RESET
        )
        get_stdout().echo(result_generic)
        get_stdout().echo()

        if result_component := self._ext_help_invoker(ctx):
            get_stdout().echo(result_component)
        else:
            formatter.write_heading(f"Component help")
            with formatter.indentation():
                formatter.write_text("<<Empty>>")
            get_stdout().echo(formatter.getvalue())
        formatter.buffer.clear()

    @staticmethod
    def _has_bg_or_reset_param(m: t.Match) -> bool:
        for c in m.group(3).split(";"):
            if not c:  # ""="0"
                return True
            try:
                i = int(c)
            except ValueError:
                continue
            if i in (pt.IntCode.RESET, pt.IntCode.BG_COLOR_OFF, pt.IntCode.INVERSED_OFF):
                return True

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        self.format_examples(ctx, formatter, self._output_examples)
        self.format_own_type(ctx, formatter)

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        opt_scope_to_opt_help_map: dict[str, list[tuple[str, str]] | None] = {
            k: [] for k in OptionScope
        }
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None and hasattr(param, "scope"):
                opt_scope_to_opt_help_map[param.scope].append(rv)

        has_header = False
        for opt_scope in self.option_scopes:
            opt_helps = opt_scope_to_opt_help_map[opt_scope]
            if not opt_helps:
                continue
            if opt_scope.value:
                has_header = True
                with formatter.section(opt_scope.value):
                    formatter.write_dl(opt_helps)
            else:
                formatter.write_paragraph()
                with formatter.indentation():
                    formatter.write_dl(opt_helps)

        if any(self._is_option_with_argument(opt) for opt in ctx.command.params):
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(inspect.cleandoc(EPILOG_ARGS_NOTE.text))

        self.format_common_options(ctx, formatter, not has_header)

    def format_examples(self, ctx: Context, formatter: HelpFormatter, examples: Section) -> None:
        if not examples:
            return
        with formatter.section(examples.title.capitalize()):
            for example in examples.content:
                example = re.sub(
                    r"(\s)" + NWMarkup.OPTION_REGEX.pattern,  # костыль; сам по себе OPTION_REGEX
                    formatter.format_accent(r"\1\2"),  # матчит "-15" в "--date Nov-15"
                    example,
                )
                if "%s" in example:
                    example %= formatter.format_command_name(ctx.command_path)
                formatter.write_text(example)


class CliGroup(click.Group, CliBaseCommand):
    TEXT_COMMAND_MATCHED_PART = FrozenStyle(fg=pt.cv.HI_BLUE, underlined=True)
    TEXT_COMMAND_SUGGEST_1ST_CHR = FrozenStyle(fg=pt.cv.HI_RED, bold=True, underlined=False)
    TEXT_COMMAND_SUGGEST_OTHERS = HelpStyles.TEXT_COMMAND_NAME

    def __init__(self, **kwargs):
        self._filepath = kwargs.get("name")
        self._autodiscover_extras = kwargs.pop("autodiscover_extras", None)

        kwargs["name"] = self._make_command_name(self._filepath)
        kwargs["short_help"] = self._make_short_help(**kwargs)
        kwargs.setdefault("type", CMDTYPE_GROUP)

        super().__init__(**kwargs)
        self.autodiscover()

    def autodiscover(self):
        from .autodiscover import AutoDiscover, AutoDiscoverExtras

        AutoDiscover.run(
            self, self._filepath, t.cast(AutoDiscoverExtras, self._autodiscover_extras)
        )

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        # self.format_own_type(ctx, formatter)

    def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
        # no options for groups
        self.format_commands(ctx, formatter)
        # self.format_subcommand_attributes(formatter)

    def format_subcommand_attributes(self, formatter: HelpFormatter):
        cts = [
            *filter(
                lambda ct: not ct.hidden,
                {*self.get_command_attributes()},
            )
        ]
        if not len(cts):
            return

        formatter.write_paragraph()
        with formatter.indentation():
            formatter.write_text(
                "   ".join(
                    get_stdout().render(formatter.format_command_attribute_legend(ct))
                    for ct in sorted(cts, key=lambda ct: ct.sorter)
                )
            )
        formatter.write_paragraph()

    def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
        # modified version of parent implementation; could not inject otherwise
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        if len(commands):
            # +2 for command type
            limit = formatter.width - 6 - max(2 + len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                cmd_name = get_stdout().render(formatter.format_command_icon_and_name(cmd))
                rows.append((cmd_name, help))

            if rows:
                with formatter.section("Commands"):
                    formatter.write_dl(rows, col_spacing=4)

    def add_commands(self, commands: Iterable[click.Command]):
        for cmd in commands:
            self.add_command(cmd)

    def get_commands(self) -> dict[str, CliBaseCommand]:
        return cast(dict[str, CliBaseCommand], self.commands)

    def get_command(self, ctx, cmd_name) -> CliBaseCommand | None:
        """
        When there is no exact match, search for commands that begin
        with the string the user has been typed, and return the matched
        command if it is the only one matching (e.g., 'es7s e' -> 'es7s exec').
        Otherwise print the closest by levenshtein distance command if no
        matches were found ('es7s ez' -> 'es7s exec'), or print all the partial
        matches if there are more than 1 of them ('es7s m' -> 'es7s manage',
        'es7s monitor').
        """
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return cast(CliBaseCommand, rv)

        matches = []
        lev_match, lev_match_dist = None, None
        for c in self.list_commands(ctx):
            if c.startswith(cmd_name):
                matches.append(c)
            ld = Levenshtein.distance(cmd_name, c)
            if not lev_match or ld <= lev_match_dist:
                lev_match, lev_match_dist = c, ld

        if not matches:
            get_logger().debug(f"No matches")
            lev_msg = ""
            if lev_match:
                get_logger().debug(f"Closest by lev. distance: {lev_match}")
                lev_msg = f"\n\nThe most similar command is:\n    {lev_match}"
            ctx.fail(f"No such command: '{cmd_name}'{lev_msg}")
            return None
        elif len(matches) == 1:
            get_logger().debug(f"Matched by prefix: {matches[0]}")
            return super().get_command(ctx, matches[0])
        # elif len(matches) > 1:

        stdout = get_stdout()

        def format_suggestions(m: t.Iterable[str]) -> str:
            suggs = [*map(lambda s: s.removeprefix(cmd_name), m)]
            same_chars_after = max(map(len, suggs))
            for i in range(same_chars_after):
                if any(len(s) <= i for s in suggs):
                    same_chars_after = i
                    break
                if len({*map(lambda s: s[i], suggs)}) > 1:  # unique characters at position <i>
                    same_chars_after = i + 1
                    break
            get_logger().debug(f"Shortest unique seq. length = {same_chars_after:d}")
            return ", ".join(map(lambda s: format_suggestion(s, same_chars_after), suggs))

        def format_suggestion(s: str, same_chars_after: int) -> str:
            return (
                stdout.render(cmd_name, self.TEXT_COMMAND_MATCHED_PART)
                + stdout.render(s[:same_chars_after], self.TEXT_COMMAND_SUGGEST_1ST_CHR)
                + stdout.render(s[same_chars_after:], self.TEXT_COMMAND_SUGGEST_OTHERS)
            )

        get_logger().debug(f"Several matches ({len(matches)}): {format_attrs(matches)}")
        ctx.fail(f"Several matches: {format_suggestions(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

    def get_command_attributes(self, recursive: bool = False) -> t.Iterable[CommandAttribute]:
        for cmd in self.get_commands().values():
            if recursive and isinstance(cmd, CliGroup):
                yield from cmd.get_command_attributes(True)
            yield cmd.get_command_type()
            yield cmd.get_command_trait()

    def _get_help_parts(self, ctx: Context, src: t.Iterable[str | HelpPart]) -> t.Generator[list]:
        yield from super()._get_help_parts(ctx, src)
        yield EPILOG_COMMON_OPTIONS

        if not self.commands:
            return

        if non_group_subcmds := sorted(
            filter(lambda cmd: not isinstance(cmd, CliGroup), self.commands.values()),
            key=lambda v: v.name,
        ):
            example_cmd = non_group_subcmds[0]
        else:
            example_cmd = [*self.commands.values()][0]

        yield HelpPart(
            EPILOG_COMMAND_HELP.text % (ctx.command_path, ctx.command_path, example_cmd.name),
            group=EPILOG_COMMAND_HELP.group,
        )


def get_current_command_name() -> str:
    if ctx := click.get_current_context(True):
        if cmd := ctx.command:
            return cmd.name
    return "n/a"
