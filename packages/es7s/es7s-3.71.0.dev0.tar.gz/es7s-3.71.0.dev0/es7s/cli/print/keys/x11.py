# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import configparser
import os.path
import re
from configparser import ConfigParser
from pytermor import NOOP_STYLE

from es7s.shared.path import DCONF_PATH
from ..._base_opts_params import CMDTRAIT_X11, CMDTYPE_BUILTIN
from ..._decorators import cli_option
from es7s.shared import USER_XBINDKEYS_RC_FILE, sub, get_logger
from ._base import (
    BindCommand,
    BindKeyTable,
    IBindCollector,
    Formatter,
    Style,
    StyleRegistry, Bind,
)
from ..._base import CliCommand
from ..._decorators import catch_and_log_and_exit, cli_command


class XBindKeysBindCommand(BindCommand):
    def get_command_part_style(self, co: str, idx) -> Style:
        if idx == 0:
            return StyleRegistry.COMMAND_PROG_STYLE
        return super().get_command_part_style(co, idx)

    def get_raw_seq_part_style(self, rc: str, idx: int) -> Style:
        if not rc:
            return NOOP_STYLE
        if rc.strip() in ('+', ":"):
            return StyleRegistry.RAW_SEQ_STYLE
        return super().get_raw_seq_part_style(rc, idx)


class GnomeDconfBindCommand(BindCommand):
    def get_command_part_style(self, co: str, idx) -> Style:
        return StyleRegistry.DETAILS_AUX_STYLE

    def get_raw_seq_part_style(self, rc: str, idx: int) -> Style:
        if not rc:
            return NOOP_STYLE
        if rc.strip() in ('<', ">"):
            return StyleRegistry.RAW_SEQ_STYLE
        return super().get_raw_seq_part_style(rc, idx)


class X11BindCollector(IBindCollector):
    def __init__(self, details: bool) -> None:
        super().__init__({}, details)
        self.collect()

    def collect(self):
        key_table = BindKeyTable("x11", label="SUPPLEMENTARY GLOBALS")
        self._key_tables = {key_table.name: key_table}

        self._collect_gnome_dconf(key_table)
        self._collect_xbindkeys(key_table)

        key_table.sort()
        key_table.update_attrs_col_width()

    def _collect_gnome_dconf(self, key_table: BindKeyTable):
        try:
            content = sub.run_subprocess(DCONF_PATH, 'dump', '/').stdout
            cfg = configparser.RawConfigParser()
            cfg.read_string(content)
            self._parse_gnome_dconf(cfg, key_table)
        except Exception as e:
            get_logger().non_fatal_exception(e)

    def _collect_xbindkeys(self, key_table: BindKeyTable):
        try:
            if os.path.isfile(USER_XBINDKEYS_RC_FILE):
                with open(USER_XBINDKEYS_RC_FILE) as f:
                    gdconf_cfg = f.read()
                self._parse_xbindkeys(gdconf_cfg, key_table)
        except Exception as e:
            get_logger().non_fatal_exception(e)

    def _parse_gnome_dconf(self, cfg: ConfigParser, key_table: BindKeyTable):
        for sect in cfg.sections():
            if 'key' not in sect or sect not in Bind.DOMAIN_TO_SORTER_MAP.keys():
                get_logger().debug(f"Skipping [{sect!s}]")
                continue
            for opt in cfg.options(sect):
                if not (vals := cfg.get(sect, opt)):
                    continue
                for val in re.findall(r"'(.+?)'", vals):
                    if val.startswith('/'):
                        get_logger().debug(f"Skipping [{sect!s}] {opt}: {val!r}")
                        continue
                    bind = self._bind_factory.from_dconf(opt, val, key_table)
                    bind.command = GnomeDconfBindCommand(sect, False, val)
                    self._add_bind(key_table, bind)

    def _parse_xbindkeys(self, table_data: str, key_table: BindKeyTable):
        #  (L#)_(start)______________(example)___________________.
        #  |1| '# @x11' |# @x11  W-x    [xbindkeys] Launch xterm'|
        #  |2| '"'      |"xbindkeys_show"                        |
        #  |3| ' '      |   Mod4 + slash                         |
        #  +-+----------+----------------------------------------+
        for record in table_data.split("@x11"):
            split = record.splitlines()
            if len(split) < 3:
                continue
            if not split[1].startswith('"') or not re.match(r"\s", split[2]):
                continue
            bind = self._bind_factory.from_tmux(split.pop(0).strip(), key_table)

            command_raw = re.sub(r'"|^\s+|\s+$', "", split.pop(0))
            seq_raw = split.pop(0).strip()
            bind.command = XBindKeysBindCommand(command_raw, False, seq_raw)

            self._add_bind(key_table, bind)


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="current X11/desktop bindings",
)
@cli_option(
    "-d",
    "--details",
    is_flag=True,
    default=False,
    help="Include bind commands and other details",
)
@catch_and_log_and_exit
class invoker:
    """
    a
    """

    def __init__(self, details: bool, **kwargs):
        self.run(details)

    def run(self, details: bool, **kwargs):
        collector = X11BindCollector(details)
        Formatter(collector).print()
