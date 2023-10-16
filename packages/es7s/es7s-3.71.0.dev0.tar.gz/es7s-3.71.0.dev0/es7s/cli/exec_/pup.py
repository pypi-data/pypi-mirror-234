# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import shutil
from pathlib import Path
from typing import Iterable

import click
from click import pass_context

from .._base import Context
from .._base_opts_params import HelpPart
from ...cli._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_NONE
from ...cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="&pack/&un&pack, unified interface for several archive formats",
    prolog=[
        HelpPart(
            "Default operation to run when no other is specified is *pack-copy*; which "
            "effectively makes ''-a|--add|-p|--pack'' optional and (most of the time) "
            "redundant; also note that when there are several operation select options, "
            "the only working one will always be the last one."
        ),
        HelpPart(
            "Archive format is determined automatically out of ARCHIVE extension. If there "
            "is none, the file will not have it either; in this case the app will search "
            "through PATH for any available archiver from the list below (left -> right), "
            "and stop the search right after any of them was found:"
        ),
        HelpPart("++zip++, ++rar++, ++gzip++, ++tar++, ++7z++", indent_shift=1),
        HelpPart(
            "¯*pack-copy*¯ ('-a') adds FILEs to ARCHIVE,",
            group="pack",
        ),
        HelpPart(
            "¯*pack-move*¯ ('-m') adds FILEs to ARCHIVE and deletes FILEs that "
            "were successfully packed.",
            group="pack",
        ),
        HelpPart(
            "⏺ If ARCHIVE already exists, new files will be appended to it, otherwise it will "
            "be created.",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ If the archive has a file with given name, there will be a warning "
            "regardless of conflicting files\\' equality or inequality. Such files will NOT "
            "be deleted in *pack-move* mode.",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ At least one FILE argument is required.",
            indent_shift=1,
        ),
        HelpPart(
            '⏺ Hyphen ""-"" can be specified as an argument and will be interpreted as standard '
            "input stream if used in place of FILE, or as standard output stream when used "
            "as ARCHIVE.",
            indent_shift=1,
        ),
        HelpPart(
            'Note that specifying ""-"" as ARCHIVE automatically switches *pack-move* to *pack-copy*, '
            'as in general writing binary data to a tty and deleting the originals is risky, as it '
            'could lead to a data loss. Furthermore, there is no way to verify that all FILEs were '
            'successfully archived when the output it a stream, so no checks will be performed whatsoever.',
            indent_shift=3,
        ),
        HelpPart(
            "⏺ A symlink will be dereferenced if its target is at the same physical device "
            "as the link itself, or archived \\'as is\\' otherwise.",
            indent_shift=1,
        ),
        HelpPart(
            "¯*unpack*¯ ('-u') extracts the ARCHIVE contents to specified FILE (actually a directory).",
            indent_shift=0,
            group="unpack",
        ),
        HelpPart(
            "⏺ Only one FILE is allowed and it is optional; if omitted, current working directory will be "
            "used. This is equivalent to specifying ''.'' as FILE.",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ FILE is treated as a directory to extract the archive contents into. No overwrites will be performed, "
            "instead a warning about name conflict will be printed to standard error stream.",
            indent_shift=1,
        ),
        HelpPart(
            '⏺ Hyphen ""-"" can be specified as an argument and will be interpreted as standard '
            "output stream if used in place of FILE, or as standard input stream when used "
            "as ARCHIVE (inversion of the logic used by *pack* operations).",
            indent_shift=1,
        ),
        HelpPart(
            "¯*list*¯ ('-l') read list of files/directories inside of ARCHIVE and display or write it to FILE.",
            indent_shift=0,
            group="list",
        ),
        HelpPart(
            "⏺ Only one FILE is allowed and it is optional; if omitted, standard output stream will be "
            "used. This is equivalent to specifying ''-'' as FILE.",
            indent_shift=1,
        ),
        HelpPart(
            'Hyphen ""-"" can be specified as an argument and will be interpreted as '
            'one of the standard streams, depending on place (as ARCHIVE or as FILE) and '
            'data flow direction of current operation (see below). Also note that it\'s '
            'perfrectly fine to specify more than one hyphen ""-"", if there is a necessity '
            'to do that.',
            title='Standard streams'
        ),
        HelpPart(
            text="""
 ╔══════════════════╦═════════════════╗\n\n
 ║ Active operation ║     P A C K     ╠════════╦════════╗\n\n
 ║━━━━━━━━┓    mode ║  copy     move  ║ unpack ║  list  ║\n\n
 ║ Data   ┗━━━━━━━━━║────────║────────║────────║────────║\n\n
 ║   flow direction ║ A <- T ║ A << T ║ A -> T ║ A -> T ║\n\n
 ╚══════════════════╩════════╩════════╩════════╩════════╝\n\n
   ║ ""-"" as ARCHIVE ║´stdout´│  OFF¯*¯  │  <stdin> │  <stdin> │\n\n
   ║────────────────║────────┘────────┘────────┘────────┘\n\n
   ║ ""-"" as FILE    ║  <stdin> │  <stdin> │´stdout´│´stdout´│\n\n
   ╚════════════════╝────────┘────────┘────────┘────────┘
"""),
        HelpPart(
            "¯*¯ /*disabled for safety, as you should never combine destructive operations",
            group="safety",
            indent_shift=2,
        ),
        HelpPart(
            "(e.g., file deleting) and writing to devices that can easily corrupt or lose your data",
            group="safety",
        ),
        HelpPart(
            "(e.g., tty reading binary data and trying to display it as text)*/",
            group="safety",
        ),
    ],
    command_examples=[
        "1. pack all python files in the current directory to ZIP archive:",
        "     %s [-a] python.zip *.py",
        "",
        "2. move log file to 7z archive:",
        "     %s -m logs.7z errors.log",
        "",
        "3. extract the archive contents into current working directory:",
        "     %s -e archive.tar [.]",
        "",
        "4. extract the archive contents into specified subdirectory:",
        "     %s -e archive.rar subdir",
        "",
        "5. display archive contents:",
        "     %s -l archive.zip [-]",
    ],
)
@cli_argument(
    "archive",
    type=click.Path(dir_okay=False, allow_dash=True, resolve_path=True, path_type=Path),
    required=True,
    nargs=1,
)
@cli_argument(
    "file",
    type=click.Path(allow_dash=True, resolve_path=True, path_type=Path),
    required=False,
    nargs=-1,
)
@cli_option(
    "-a",
    "--add",
    "-p",
    "--pack",
    is_flag=True,
    help="*pack-copy*: Recursively add FILEs to an archive named ARCHIVE.",
)
@cli_option(
    "-m",
    "--move",
    is_flag=True,
    help="*pack-move*: Same as *pack-copy*, but also ¯delete¯ successfully packed ones. ",
)
@cli_option(
    "-e",
    "-u",
    "--extract",
    "--unpack",
    is_flag=True,
    help="*unpack*: Extract file(s) from ARCHIVE to FILE (here it should be a directory).",
)
@cli_option(
    "-l",
    "-i",
    "--list",
    "--index",
    is_flag=True,
    help="*list*: print ARCHIVE contents to stdout or to FILE (must not exist).",
)
@catch_and_log_and_exit
@pass_context
class invoker:
    """"""
    FORMATS = ["zip", "rar", "gzip", "tar", "7z"]
    EXECUTABLES = {}

    def __init__(self, ctx: Context, archive: Path, file: Iterable[Path],  add: bool, move: bool, extract: bool, list: bool,  **kwargs):
        self._archive = archive
        self._files = [*file]
        self.run()

    def run(self):
        print(self._files)
        [print(self._get_archiver(fmt)) for fmt in self.FORMATS]

    def _find_executables(self):
        for fmt in self.FORMATS:
            if path := shutil.which(fmt):
                self.EXECUTABLES[fmt] = path

    def _get_archiver(self, fmt: str) -> str | None:
        if len(self.EXECUTABLES) == 0:
            self._find_executables()
        return self.EXECUTABLES.get(fmt, None)
