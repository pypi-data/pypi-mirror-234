# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import typing as t
from os import getcwd
from pathlib import Path

import click
import pytermor as pt
from pytermor import NOOP_STYLE

from es7s.commons import GitRepo
from es7s.commons import PLangColor
from es7s.commons import Scale
from es7s.shared import FrozenStyle, Styles, get_logger, get_stdout
from es7s.shared import Linguist
from es7s.shared import SubprocessExitCodeError
from .._decorators import catch_and_log_and_exit, cli_argument, cli_command, cli_option


@cli_command(__file__, short_help="programming language statistics")
@cli_argument("path", type=click.Path(exists=True), nargs=-1, required=False)
@cli_option(
    "-D",
    "--docker",
    is_flag=True,
    default=False,
    help="Run github-linguist in a docker container.",
)
@cli_option(
    "-N",
    "--no-cache",
    is_flag=True,
    default=False,
    help="Calculate the value regardless of the cache state and do not update it.",
)
@catch_and_log_and_exit
class invoker:
    """
    ...
    """

    COL_PAD = pt.pad(2)
    SHARED_SCALE_LEN = 40
    SHARED_SCALE_CHAR = "━"  # "━▁"
    SHARED_SCALE_CHAR_START = "╺"

    def __init__(
        self,
        docker: bool,
        no_cache: bool,
        path: tuple[Path, ...] | None = None,
        **kwargs,
    ):
        self._use_cache = not no_cache

        stdout = get_stdout()
        if not path:
            path = [
                getcwd(),
            ]

        psetd = dict()
        psetf = set()
        for p in path:
            absp = Path(p).resolve()
            if os.path.isdir(absp):
                try:
                    repo = GitRepo(absp)
                except ValueError as e:
                    get_logger().warning(f"Skipping: {e}")
                    continue
                psetd.setdefault(absp, repo)
            else:
                psetf.add(absp)

        for absp, repo in psetd.items():
            self._run(absp, docker, repo)
        if psetd and psetf:
            stdout.echo()
        for absp in sorted(psetf):
            self._run(absp, docker, None)

    def _run(self, absp: Path, docker: bool, repo: GitRepo = None):
        stdout = get_stdout()
        target = absp
        target_is_dir = repo is not None

        title = str(target)
        data = None

        if repo:
            target = repo.path
            if self._use_cache:
                data = repo.get_cached_stats()
            if str(absp) == os.path.commonpath([absp, repo.path]):
                if repo_name := repo.get_repo_name():
                    title = repo_name
                    if target_is_dir:
                        self._echo_dir_title(title, Styles.TEXT_SUBTITLE)
                        title = None

        if not data:
            try:
                data = Linguist.get_lang_statistics(target, docker, breakdown=target_is_dir)
            except SubprocessExitCodeError as e:
                stdout.echo_rendered(f"Error: {title}", Styles.ERROR)
                get_logger().non_fatal_exception(e)
                return
            if data and repo and self._use_cache:
                repo.update_cached_stats(data)

        if not data:
            stdout.echo((title + ": " if title else ""), nl=False)
            stdout.echo_rendered("<no data>", Styles.TEXT_DEFAULT)
            get_logger().debug("Empty stdout -- no data")
            return

        if target_is_dir:
            get_logger().debug(f"Rendering as directory stats: {absp}")
            self._render_dir_info(data, absp, repo, title)
        else:
            for file_path, file_data in data.items():
                get_logger().debug(f"Rendering as file stats: {file_path}")
                self._render_file_info(file_data, title)
                stdout.echo()

    def _render_dir_info(self, data: dict, absp: Path, repo: GitRepo, title: str | None):
        stdout = get_stdout()
        result: t.List[t.Sequence[pt.RT, ...]] = []
        shared_scale: pt.Text = pt.Text()

        data_flat = [{**v, "lang": k, "linenum": 0} for k, v in data.items()]

        lines_total = 0
        logger = get_logger()
        for lang_data in data_flat:
            linenum = 0
            for filename in lang_data.get("files"):
                stat_file = os.path.abspath(os.path.join(repo.path, filename))
                if str(absp) == os.path.commonpath([absp, Path(stat_file)]):
                    if os.path.isfile(stat_file):
                        logger.debug(f"Counting lines in: {stat_file!r}")
                        try:
                            with open(stat_file, "rt") as fd:
                                linenum += len(fd.readlines())
                        except UnicodeDecodeError as e:
                            logger.non_fatal_exception(
                                f"Failed to count lines (non-UTF8?): {stat_file!r}: {e}"
                            )
                            logger.debug(f"Counting lines (BINARY MODE) in: {stat_file!r}")
                            with open(stat_file, "rb") as fd:
                                linenum += len(fd.readlines())
            if not linenum:
                continue
            lang_data.update({"linenum": linenum})
            lines_total += linenum

        data_filtered = filter(lambda v: v["linenum"] > 0, data_flat)

        for idx, lang_data in enumerate(sorted(data_filtered, key=lambda v: -v.get("linenum"))):
            lang = lang_data.get("lang")
            # perc = lang_data.get("percentage")
            # sizeratio = float(perc.removesuffix("%")) / 100
            linenum = lang_data.get("linenum")
            lineratio = linenum / lines_total

            lang_st = self._get_lang_st(lang)
            scale = Scale(lineratio, NOOP_STYLE, lang_st)

            shared_scale += Scale(
                lineratio,
                NOOP_STYLE,
                lang_st,
                self.SHARED_SCALE_LEN,
                False,
                self.SHARED_SCALE_CHAR,
                # (None, self.SHARED_SCALE_CHAR_START)[idx>0],
            ).blocks

            result.append(
                (
                    scale,
                    pt.highlight(str(linenum)),
                    pt.Fragment(lang, lang_st),
                )
            )

        if not result:
            return

        if title:
            self._echo_dir_title(title)

        if len(shared_scale) and len(frags := shared_scale.as_fragments()):
            if (chars_short := self.SHARED_SCALE_LEN - len(shared_scale)) > 0:
                if first_frag := frags.pop(0):
                    shared_scale.prepend(
                        pt.Fragment(first_frag.raw()[-1] * chars_short, first_frag.style)
                    )
            stdout.echo_rendered(shared_scale)

        def col_lens():
            for col in range(len(result[0])):
                yield max(len(r[col]) for r in result)

        col_len = [*col_lens()]
        for line in result:
            for idx, cell in enumerate(line):
                val = cell
                vpad = pt.pad(col_len[idx] - len(cell))
                if idx in (0, 1):
                    val = vpad + val
                else:
                    val += vpad
                val += self.COL_PAD
                stdout.echo_rendered(val, nl=False)
            stdout.echo()
        stdout.echo()

    def _render_file_info(self, data: dict, title: str):
        stdout = get_stdout()
        col_lens = [9, 9, PLangColor.get_longest_key_len(), None]
        data_row = []

        code_lines, logic_lines = data["lines"], data["sloc"]
        if zero_len := (code_lines == 0 or logic_lines == 0):
            zfrag = pt.Fragment("-", pt.Highlighter.STYLE_NUL)
            data_row.extend([zfrag] * 2)
        else:
            data_row.extend((pt.highlight(str(code_lines)), pt.highlight(str(logic_lines))))

        ftype = data["type"]
        lang = data["language"]

        if not lang:
            lang_st = NOOP_STYLE if not zero_len else pt.Highlighter.STYLE_NUL
            lang_frag = pt.Fragment(ftype, lang_st)
        else:
            lang_st = self._get_lang_st(lang)
            lang_frag = pt.Fragment(lang, lang_st)
        data_row.append(lang_frag)

        for idx, cell in enumerate(data_row):
            vpad = pt.pad((col_lens[idx] or 0) - len(cell))
            if idx < 2:
                val = vpad + cell
            else:
                val = cell + vpad
            stdout.echo_rendered(self.COL_PAD + val, nl=False)

        stdout.echo(title, nl=False)

    def _echo_dir_title(self, title: str, st: pt.FT = NOOP_STYLE) -> None:
        get_stdout().echo()
        get_stdout().echo_rendered(
            pt.FrozenText(
                pt.cut(title, self.SHARED_SCALE_LEN, align=pt.Align.RIGHT),
                # print only the ending if title is longer than limit...
                st,
                width=self.SHARED_SCALE_LEN,
                align=pt.Align.CENTER,
                # ...while keeping it centered otherwise.
            )
        )

    def _get_lang_st(self, lang_str: str) -> FrozenStyle:
        try:
            if lang_color := PLangColor.find_by_name(lang_str.strip()):
                return FrozenStyle(fg=lang_color)
        except LookupError as e:
            get_logger().warning(e)
            return NOOP_STYLE
