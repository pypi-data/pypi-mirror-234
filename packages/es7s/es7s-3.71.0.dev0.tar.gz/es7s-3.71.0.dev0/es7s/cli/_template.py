# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import re
import tempfile
import typing

import pytermor as pt

from es7s.cli._foreign import Pager
from es7s.shared import get_logger, get_stdout, make_interceptor_io
from es7s.commons import  Regex


class TemplateCommand:
    REGEX_SECTION_START = '\x1b\x1e'
    REGEX_SECTION_END = '\x1b\x7f'
    REGEX_SUBSTITUTE_SEP = Regex(R'\s*\x1f\s*')

    def __init__(self, filepath: str):
        get_logger().debug(f"Input filepath: '{filepath}'")
        with open(filepath, "rt") as f:
            self._tpl = f.read()
        self._sub_expr_count = 0
        get_logger().debug(f"Input size: " + pt.format_si_binary(len(self._tpl)))

    def run(self):
        engine = pt.TemplateEngine()
        substituted = engine.substitute(self._tpl)
        rendered = substituted.render(get_stdout().renderer)
        postprocessed = self._postprocess(rendered)
        self._print(postprocessed)

    def _postprocess(self, rendered: str) -> str:
        if self.REGEX_SECTION_START not in rendered:
            return rendered

        rendered, _, preprocessors = rendered.partition(self.REGEX_SECTION_START)
        preprocessors, _, _ = preprocessors.partition(self.REGEX_SECTION_END)
        for pp in preprocessors.splitlines():
            if not pp:
                continue
            sub_args = [*self.REGEX_SUBSTITUTE_SEP.split(pp, 1)]
            if len(sub_args) != 2:
                get_logger().warning(f"Invalid substitute directive: {pp!r}")
                continue
            try:
                rendered = self._postprocess_apply_subexp(rendered, sub_args)
            except RuntimeError as e:
                get_logger().exception(e)
                continue

        return rendered

    def _postprocess_apply_subexp(self, rendered: str, sub_args: list):
        self._sub_expr_count += 1
        pattern, repl = sub_args
        replacer = self._replacer(repl)

        get_logger().debug(f"SUBEX #{self._sub_expr_count}: '{pattern}' -> '{repl}'")
        try:
            return re.sub(pattern, replacer, rendered)
        except re.error as e:
            raise RuntimeError(f"Failed to apply substitute expression #{self._sub_expr_count}") from e

    def _replacer(self, repl: str) -> typing.Callable[[re.Match], str]:
        match_count = 0

        def _internal(m: re.Match) -> str:
            nonlocal match_count
            match_count += 1
            label = f"Match #{match_count} as {len(m.groups())} groups at {m.span()}"
            get_logger().trace(m.group(0), label=label)
            return m.expand(repl)
        return _internal

    def _print(self, postprocessed: str):
        if not get_stdout().io.isatty():
            get_stdout().echo(postprocessed, nl=False)
            return

        tmp_file = open(tempfile.mkstemp()[1], 'w')
        tmp_file.write(postprocessed)
        tmp_file.flush()
        max_line_len = max(map(len, pt.SgrStringReplacer().apply(postprocessed).splitlines()))
        Pager(max_line_len).open(tmp_file.name)
