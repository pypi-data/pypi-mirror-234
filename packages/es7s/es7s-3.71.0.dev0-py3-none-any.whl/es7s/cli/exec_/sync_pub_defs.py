# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import re
from collections.abc import Iterable
from pathlib import Path

import click

from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11, CMDTRAIT_NONE
from es7s.cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit
from es7s.shared import get_logger


class _ImportLine:
    def __init__(self, pkg: str, name: str, alias: str = None):
        self.pkg: str = pkg
        self.name: str = name
        self.alias: str = alias or name

    def __str__(self):
        return f"from {self.pkg} import {self.name} as {self.alias}\n"

    def __repr__(self) -> str:
        result = f"({self.pkg}) {self.name!r}"
        if self.alias != self.name:
            result += f" -> {self.alias!r}"
        return result

    def is_equal(self, m: re.Match, ignore_alias=True) -> bool:
        return (
            self.pkg == m.group("pkg")
            and self.name == m.group("name")
            and (self.alias == m.group("alias") or ignore_alias)
        )


ImportsList = Iterable[tuple[str, list[str]]]
ImportsMap = dict[str, list[str]]


@cli_command(
    name=__file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="find all public defs and compose an import __init__ file",
)
@cli_argument(
    "target",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True, path_type=Path),
    required=True,
    nargs=-1,
)
@cli_option(
    "-u",
    "--update",
    is_flag=True,
    help="Update __init__.py file in each TARGET's root folder, make a copy of the original "
         "file beforehands.",
)
@cli_option(
    "-B",
    "--no-backup",
    is_flag=True,
    help="Do not make a copy of the original __init__.py (implies '-u').",
)
@catch_and_log_and_exit
class invoker:
    """
    Find all Python files in TARGET folder and subfolders, and compose an import
    __init__ file contents out of all public definitions found. Print the
    contents to stdout or replace the original __init__.py file with '-u'.\n\n

    If update mode is enabled, also merge the imports from the original file
    with generated ones, skipping aliased imports (i.e. keep them untouched).
    Note that in this mode the final imports are unsorted -- first there are
    original imports from the existing file, and then new ones are added (the
    ones that are missing).
    """

    # language=regexp
    DEF_NAME = R"[A-Za-z][\w_]*"

    DEF_RE = re.compile(
        Rf"""
            ^({DEF_NAME})(?=\s*=) 
            |
            ^def\s+({DEF_NAME})(?=\()
            |
            ^class\s+({DEF_NAME})(?=[(:])
        """,
        flags=re.VERBOSE,
    )

    IMPORT_RE = re.compile(
        R"""
            ^ from \s+ (?P<pkg>[.\w_]+) \s+
            import \s+ (?P<name>[\w_]+) \s*
            (?: as \s+ (?P<alias>[\w_]+) )?
        """,
        flags=re.VERBOSE,
    )

    def __init__(self, target: tuple[Path, ...], update: bool, no_backup: bool, **kwargs):
        self._update = update
        self._backup = not no_backup

        for t in target:
            self._run(t)

    def _run(self, target: Path):
        logger = get_logger()

        imports = dict(self._find_defs_recursive(target))
        if imports:
            total_matches = sum(len(line) for line in imports.values())
            logger.info(f"{total_matches:4d} matches total for '{target}'")

        import_lines = [*self._compose_import_lines(imports)]
        print("".join(map(str, import_lines)))

        if self._update:
            self._update_init_file(target, import_lines)

    def _find_defs_recursive(self, target: Path, subdir: Path = None) -> ImportsList:
        logger = get_logger()
        dirmatches = 0

        for file in sorted((subdir or target).iterdir()):
            if file.name.startswith((".", "_")):
                continue

            if file.is_dir():
                yield from self._find_defs_recursive(target, file)
                continue

            if not file.name.endswith(".py"):
                continue

            defnames = list[str]()
            relpath = os.path.relpath(file, target)
            pkg = os.path.splitext(relpath)[0].replace(os.path.sep, ".")

            skip_next = False
            with open(file, "rt") as fsrc:
                for lineno, line in enumerate(fsrc.readlines()):
                    if line.startswith("@overload"):
                        skip_next = True
                        continue
                    if skip_next:
                        skip_next = False
                        continue

                    if not (m := self.DEF_RE.match(line)):
                        continue
                    if (defname := m.group(m.lastindex)) in ["try"]:
                        continue

                    defnames.append(defname)

                    msg = f"Matched line {lineno:>4d} in {relpath}: {m.group()!r}"
                    logger.debug(msg)

            dirmatches += len(defnames)
            yield "." + pkg, defnames

        if dirmatches and subdir != target:
            logger.info(f"{dirmatches:4d} matches in '{(subdir or target)}'")

    def _compose_import_lines(self, imports: ImportsMap) -> Iterable[_ImportLine]:
        logger = get_logger()
        used_names = set()

        for pkg in sorted(imports.keys()):
            for name in sorted(imports.get(pkg)):
                pkgparts = pkg.split(".")

                alias = name
                while alias in used_names and pkgparts:
                    alias = pkgparts.pop() + "_" + alias
                if alias in used_names:
                    logger.warning(f"Conflict: unable to import {pkg}.{name}")
                    continue

                used_names.add(alias)
                yield (import_line := _ImportLine(pkg, name, alias))  # noqa
                if alias != name:
                    logger.debug(f"Renamed {import_line!r}")

    def _update_init_file(self, target: Path, generated_lines: list[_ImportLine]):
        logger = get_logger()

        target_file = target.joinpath("__init__.py")
        if not target_file.exists():
            logger.warning(f"Target {target} does not contain '__init__.py' file, skipping")
            return

        origin_lines = []
        origin_import_end_lineno = 0
        with open(target_file, "rt") as fsrc:
            for idx, oline in enumerate(fsrc.readlines()):
                msg = f"%20s {(idx+1):4d}: {oline.strip()!r}"

                m = self.IMPORT_RE.match(oline)
                if not m:  # всрато, но я заебался. @TODO переделать
                    origin_lines.append(oline)
                    logger.debug(msg % "Keeping non-import")
                    continue

                msgact = "Keeping unique"
                for genline in generated_lines:
                    if genline.is_equal(m):
                        generated_lines.remove(genline)
                        msgact = "Reusing duplicate"
                        break

                origin_import_end_lineno = len(origin_lines)
                origin_lines.append(oline)
                logger.debug(msg % msgact)

        if self._backup:
            target_file.rename(target_file.name + ".bak")

        new_target_file = target.joinpath("__init__.py")
        with open(new_target_file, "wt") as fdest:
            for idx, line in enumerate(origin_lines):
                if generated_lines and idx >= origin_import_end_lineno:
                    while generated_lines:
                        genline = str(generated_lines.pop())
                        fdest.write(genline)
                        logger.debug(f"Appending new import line: {genline.strip()!r}")
                fdest.write(line)
