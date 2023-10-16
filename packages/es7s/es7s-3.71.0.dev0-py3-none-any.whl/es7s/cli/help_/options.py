# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import click

from .._base import (
    CliCommand,
    Context,
    HelpFormatter,
)
from .._base_opts_params import IntRange, OptionScope, CommonOption, HelpPart
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_command


class OptionsCliCommand(CliCommand):
    COMMON_OPTIONS = [
        CommonOption(
            param_decls=["-v", "--verbose"],
            count=True,
            type=IntRange(0, 3, clamp=True, show_range=False),
            default=0,
            help="Increase the amount of details: '-v' for more verbose info "
            "and exception stack traces, '-vv' for even more info, and '-vvv' for data "
            "dumps. The logging level also depends on this option; see the table below.",
        ),
        CommonOption(
            param_decls=["-Q", "--quiet"],
            is_flag=True,
            default=False,
            help="Disables printing messages to a standard error stream, which includes "
            "warnings, errors, debugging information and tracing. Note that silencing the "
            "application does not affect the logging system behaviour in the slightest.",
        ),
        CommonOption(
            param_decls=["-c", "--color"],
            is_flag=True,
            default=None,
            help="Explicitly enable output formatting using escape sequences.",
        ),
        CommonOption(
            param_decls=["-C", "--no-color"],
            is_flag=True,
            default=None,
            help="Explicitly disable output formatting.",
        ),
        CommonOption(
            param_decls=["--tmux"],
            is_flag=True,
            default=False,
            help="Transform output SGRs to tmux markup (respecting '-c|-C').",
        ),
        CommonOption(
            param_decls=["--default"],
            is_flag=True,
            default=False,
            help="Ignore user configuration file (if it exists), so that the "
            "default values are loaded.",
        ),
        CommonOption(
            param_decls=["--trace"],
            is_flag=True,
            default=False,
            help="Alias for '-vvv'.",
        ),
    ]

    EPILOG_INTRO = [
        HelpPart(
            title="introduction",
            text="There are three different option scopes:",
        ),
        HelpPart(
            "(1) Command-specific      (2) Group-specific       (3) Common",
        ),
        HelpPart(
            "The first scope is referenced simply as *Options* and represents a set of "
            "local options for a defined command (e.g., '--recursive' for 'es7s exec "
            "ls' command)."
        ),
        HelpPart(
            "The options in the second scope do not refer to a single command, but "
            "to a group of commands (e.g., '--demo' for 'es7s monitor' group) and belong "
            "to all the commands of that group."
        ),
        HelpPart(
            "The third scope is application-wide -- all the options listed below can be "
            "added to any 'es7s' command whatsoever. Their descriptions were moved into "
            "a dedicated command to avoid useless repetitions and save some screen space."
        ),
        HelpPart(
            title="Options order",
            text="Unlike the regular approach, common options (3) can be placed anywhere "
            "in the command and they `will` be correctly recognized, e.g.: "
            "''es7s -c exec -v ls'' is the equivalent of ''es7s exec ls -cv''.",
        ),
        HelpPart(
            "On the contrary, command-specific (1) and group-specific (2) options should "
            "always be placed *after* the command (as groups themselves are not actual commands "
            "and do not have arguments). To summarize:"
        ),
        HelpPart("'es7s' @(3)@ 'group' @(3)@ 'command' @(1)@ @(2)@ @(3)@"),
        HelpPart(
            title="Passing arguments through",
            text="As [[integrated]] and [[external]] commands invoke another executable(s) under "
            "the hood, there should be a way to separate 'es7s' arguments from child process "
            "arguments, and there is a separator just for that: \"'--'\". Also note that unique "
            "options can be specified without a separator, as 'es7s' transfers options unknown to "
            "him down to an external executable and doesn't panic (this applies to aforementioned "
            "command types only).",
        ),
        HelpPart("  'es7s exec watson --help'", group="pat2"),
        HelpPart("        will result in es7s command help message", group="pat2"),
        HelpPart("  'es7s exec watson -- --help'", group="pat3"),
        HelpPart("        will result in watson help message", group="pat3"),
        HelpPart("  'watson --help'", group="pat4"),
        HelpPart(
            "        same as previous, but direct invocation is implemented "
            "for [[external]] commands only",
            group="pat4",
        ),
        HelpPart("  'es7s print colors --mode=rgb'", group="pat5"),
        HelpPart(
            "        there is no option '--mode' for a print command, so it can be specified as is",
            group="pat5",
        ),
    ]

    EPILOG = [
        HelpPart(
            title="forcing/prohibiting the colors",
            text="/*(this part was written in the middle stage of es7s development, when the "
            "application ignored options in question in case no actual command was invoked, "
            "and the output consisted of help text only; later that was fixed, but I didn't "
            "find the strength to just purge these sections, as they can be still useful; "
            "therefore they were kept)*/",
        ),
        HelpPart(
            "If neither of '--color' and '--no-color' is set, the output mode "
            "will be set depending on the output device (i.e. if the app "
            "sees a terminal, the colors will be enabled, and the opposite "
            "otherwise). This approach is common, but some applications do not implement "
            "options to forcefully enable or disable colors, and always rely on auto-"
            "detection instead. However, there are several ways to bypass this:",
        ),
        HelpPart(
            "⏺ To forcefully disable SGRs simply redirect or pipe the output stream "
            "somewhere, even a rudimentary 'cat' will work: 'es7s help options | cat'. "
            "The application will see that the output is not an interactive terminal "
            'and thus will switch to ""no formatting allowed"" mode.',
            indent_shift=1,
        ),
        HelpPart(
            "⏺ Enabling SGRs by force is a bit trickier and requires some preparations, "
            "as well as Linux OS or similar. Install the 'unbuffer' small utility and "
            "launch the needed command like this: 'unbuffer es7s help options'. It will "
            "work for almost any CLI application, not just for 'es7s', so personally I "
            "find it very handy. It doesn't matter if the output is redirected or not; "
            "the behaviour of the applications will be as if there *is* a terminal on "
            "the receiving side. To test it, run 'unbuffer es7s help options | cat' -- "
            "the formatting should be present.",
            indent_shift=1,
        ),
        HelpPart(
            "  'unbuffer' homepage: https://core.tcl-lang.org/expect/home",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ Some commands has an option '--raw' and (even more rarely) an option "
            "'--no-raw'. In general, their effects are similar to the ones of '--no-color' and "
            "'--color' options respectively, but with some extra logic on top of that. "
            "In other words, effects of '--color' option form a set which is also a subset "
            "of '--raw' effects and therefore it is redundant to use them both at the same "
            "time. If the goal is to “disable” as much formatting as possible, use '--raw' "
            "alone (adding '--no-color' will make no difference at all). On the other "
            "hand, “enabling” as much formatting as possible needs different approach in "
            "term of the command options. Key difference is that '--no-raw' just disables "
            "auto-application of rules specific to a command in question, but SGR renderer "
            'setup is done based on presence (or absence) of"--[no-]color"options '
            "(roughly speaking), so in order to get minimum restrictions one shall use "
            "both options '--no-raw' and '--color' at the same time.",
            indent_shift=1,
        ),
        HelpPart(
            title="verbosity",
            text="""
Filled (░░) cells indicate that the setting does not affect the subject.\n\n\n

╔══════════════════╦════════╦════════╦════════╦════════╦══════════╗\n\n
║{ES7S_VERBOSITY}  ║^unset,^║ `1` or   ║ `2` or   ║ `3` or   ║ ░░░░░░░░ ║\n\n
║ environment var. ║ ^empty^║ `VERBOSE`║  `DEBUG` ║  `TRACE` ║ ░░░░░░░░ ║\n\n
║──────────────────║────────║────────║────────║────────║──────────║\n\n
║ Cmd line options ║ ^none^ ║  "-v"  ║ "-vv"  ║ "-vvv" ║   "-q"   ║\n\n
╚══════════════════╩════════╩════════╩════════╩════════╩══════════╝\n\n
    ║ Stderr level ║´WARN+´ │´INFO+´ │´DEBUG+´│´TRACE+´│   None   │\n\n
    ║ Syslog level ║´INFO+´ │´DEBUG+´│´DEBUG+´│´DEBUG+´│ ░░░░░░░░ │\n\n
    ║ Logfile¯*¯ lvl ║´INFO+´ │´INFO+´ │´DEBUG+´│´TRACE+´│ ░░░░░░░░ │\n\n
    ║──────────────║────────╵────────│────────╵────────│──────────│\n\n
    ║ CLI monitors ║`OFF` unless set in│ `ON` unless set in│ ░░░░░░░░ │\n\n
    ║ debug markup ║ environ./config │ environ./config │ ░░░░░░░░ │\n\n
    ╚═/^effects^/══╝─────────────────┘─────────────────┘──────────┘\n\n

      ¯*¯ /*if enabled with corresponding environment var*/ 
    """,
        ),
    ]
    ENVIRONMENT_PROLOG = """As a rule of a thumb, a variable defined in the config has 
lower priority than *the* *same* variable set up in the environment, and both has lower 
priority than a corresponding command line option (if it exists). To sum up:\n\n

    COMMAND LINE OPTION  >  ENVIRONMENT VARIABLE  >  CONFIG VARIABLE\n\n

The only exception is how '--verbose' command line option interacts with monitor
debugging markup setup: because the main purpose of the option is different, it
affects the markup if and only if config variable and environment variable both
are empty, and is ignored in this context otherwise (see below).  
"""
    ENVIRONMENT_RO = [
        (
            "{ES7S_CLI}",
            "Contains path to CLI entrypoint of 'es7s' system.",
        ),
        ("",),
        (
            "{ES7S_SHELL_COMMONS}",
            "Contains path to es7s/commons legacy shared library for G1/G2 shell components.",
        ),
        ("",),
        (
            "{ES7S_THEME_COLOR_SGR}",
            "Contains SGR params defining current theme color (config var <general.theme-color>).",
        ),
        ("",),
        (
            "{ES7S_USER_REPOS_PATH}",
            "Corresponds to config value <general.user-repos-path>. Contains "
            "path to user git repositories dir for various purposes: making "
            "backups, auto-fetching, synchronizing etc. All these background "
            "processes are disabled by default and shall be turned on in the "
            "configuration file.",
        ),
    ]
    ENVIRONMENT_WO = [
        (
            "{ES7S_VERBOSITY}",
            "Non-empty string determines detail level of the logs (for valid "
            "values see the table above). If the verbosity is set to max level, "
            "extended output of 'pytermor' formatting library is enabled as well (by "
            "setting @PYTERMOR_TRACE_RENDERS@). Works in [CLI] and [GTK] domains, "
            "whereas '-v' or '--trace' options are recognized by CLI entrypoint only. "
            "Note that command line option has a higher priority than an environment "
            "variable.",
        ),
        ("",),
        (
            "{ES7S_LOGFILE}",
            "Non-empty string with a path to a file for log writing. No file logging is "
            "performed if the variable is missing or empty. Corresponding config "
            "variable: ¯@TODO <<general.logfile>>¯.",
        ),
        ("",),
        (
            "{ES7S_DAEMON_DEBUG}",
            "Non-empty string: ",
        ),
        *[
            ("", s)
            for s in (
                " - makes clients and daemon use different socket server address "
                "for IPC, which helps to avoid conflicts with installed and running "
                "system 'es7s' daemon instance; ",
                " - allows the python debugger to stay connected by keeping "
                "the daemon process attached.",
            )
        ],
        ("", "(Cannot be set via config)"),
        ("",),
        (
            "{ES7S_MONITOR_DEBUG}",
            "Non-empty string enables CLI monitor output debugging markup. Corresponding "
            "config variable: <monitor.debug>. Is set by tmux, but can also be set "
            "manually, as a regular env var. When both configuration and environment "
            "variable are *unset*, the system uses the current verbosity level to see "
            "if the mode should be enabled, and will do so on `DEBUG` and `TRACE` "
            "verbosity levels.",
        ),
        ("",),
        (
            "{ES7S_INDICATOR_DEBUG}",
            "Non-empty string enables indicator output debugging markup. Corresponding "
            "config variable: <indicator.debug>.",
        ),
        ("",),
        (
            "{ES7S_CLI_DEBUG_IO}",
            "Non-empty string enables mirroring all data sent to stdout and stderr to temp files "
            "'/tmp/es7s-stdout' and '/tmp/es7s-stderr'. Has the same effect as <cli.debug-io> config "
            "variable, but with higher priority.",
        ),
        ("",),
        (
            "{PYTERMOR_*}",
            "These variables configure *pytermor*, the library which is used internally for "
            "displaying the formatted text to the terminal. The basic usage and details can "
            "be found in official docs: https://pypi.org/project/pytermor. Any of these "
            "can be set as 'es7s' environment var and will be processed as expected:"
        ),
        ("",),
        *[
            ("", s)
            for s in (
                "⏺ {PYTERMOR_DEFAULT_OUTPUT_MODE}",
                "⏺ {PYTERMOR_FORCE_OUTPUT_MODE}",
                "⏺ {PYTERMOR_PREFER_RGB}",
                "⏺ {PYTERMOR_RENDERER_CLASS}",
                "⏺ {PYTERMOR_TRACE_RENDERS}",
            )
        ],
        ("",),
    ]

    option_scopes: list[OptionScope] = [
        OptionScope.COMMON,
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._include_common_options_epilog = False

    def _make_short_help(self, **kwargs) -> str:
        return kwargs.get("short_help")

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        pass

    def format_own_type(self, ctx: Context, formatter: HelpFormatter):
        pass

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, self.EPILOG_INTRO)
        formatter.write_paragraph()

        formatter.write_heading("Common options list", newline=False, colon=False)
        with formatter.indentation():
            formatter.write_dl([p.get_help_record(ctx) for p in self.COMMON_OPTIONS])

        self._format_help_parts(formatter, self.EPILOG)

        formatter.write_paragraph()
        formatter.write_heading("Environment", newline=False, colon=False)
        with formatter.indentation():
            formatter.write_text(self.ENVIRONMENT_PROLOG)

            formatter.write_paragraph()
            formatter.write_heading("Variables set by app", newline=False, colon=False)
            with formatter.indentation():
                formatter.write_dl(self.ENVIRONMENT_RO)

            formatter.write_paragraph()
            formatter.write_heading("Variables set by user", newline=False, colon=False)
            with formatter.indentation():
                formatter.write_dl(self.ENVIRONMENT_WO)


@cli_command(
    name=__file__,
    cls=OptionsCliCommand,
    short_help="common options and environment vars",
)
@cli_pass_context
@catch_and_log_and_exit
def invoker(ctx: click.Context, **kwargs):
    click.echo(ctx.get_help())
