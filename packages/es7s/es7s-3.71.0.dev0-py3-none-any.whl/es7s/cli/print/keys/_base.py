# ------------------------------------------------------------------------------
#  es7s/core (G2)
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
"""
Get a list of current tmux bindings, format it and display. Intended to run as
a tmux popup, but can be invoked directly as well.
"""
from __future__ import annotations
import pytermor as pt
import itertools
import re
import sys
import typing as t
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import total_ordering, cached_property
from re import Pattern, Match
from typing import Callable, ClassVar, Dict, List, OrderedDict, Sized

from pytermor import (
    DEFAULT_COLOR,
    Fragment,
    IRenderable,
    IRenderer,
    NOOP_STYLE,
    Style,
    Text,
    char_range,
    cv,
    flatten1,
    get_terminal_width,
    ljust_sgr,
    pad,
    rjust_sgr,
)

from es7s.shared import FrozenStyle, get_stdout


class IBindCollector(metaclass=ABCMeta):
    """
    Set of bindings grouped by key table.
    """

    def __init__(self, invoker_map: dict[str, KeyCombo | None], details: bool) -> None:
        super().__init__()
        self._key_tables: dict[str, BindKeyTable] | None = None
        self._invoker_map: dict[str, KeyCombo | None] = invoker_map
        self._used_mods: set[Modifier] = set()
        self._used_traits_key_chars: set[str] = set()
        self._used_mouse_button = False
        self._details: bool = details

        self._key_combo_factory = KeyComboFactory(self.is_invoker)
        self._bind_factory = BindFactory(self._key_combo_factory)

    def is_invoker(self, key_combo: KeyCombo) -> bool:
        for inv in self._invoker_map.values():
            if inv is None:
                continue
            if hash(inv) == hash(key_combo):
                return True
        return False

    def get_key_tables(self) -> list[BindKeyTable]:
        return [*self._key_tables.values()]

    def get_key_table_names(self) -> list[str]:
        return [*self._invoker_map.keys()]

    def get_invoker(self, key_table_name: str) -> KeyCombo | None:
        return self._invoker_map.get(key_table_name)

    def get_used_mods(self) -> set[Modifier]:
        return self._used_mods

    def get_used_mouse_button(self) -> bool:
        return self._used_mouse_button

    def get_used_traits(self) -> list[BindTrait]:
        return [BindTraitRegistry.TRAIT_MAP.get(k) for k in self._used_traits_key_chars]

    @abstractmethod
    def collect(self) -> None:
        ...

    def render_extras(self) -> Iterable[str]:
        ...

    def _add_bind(self, key_table: BindKeyTable, bind: Bind):
        key_table.append(bind)
        for c in bind.sequence.combos:
            if c.key.is_mouse_key:
                self._used_mouse_button = True
            for m in c.mods:
                self._used_mods.add(m)
        if not bind.traits:
            return
        for t in bind.traits:
            self._used_traits_key_chars.add(t.key_char)

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"[{', '.join(self.get_key_table_names())}]"


class StyleRegistry:
    """
    Source of truth in `Style` context.
    """

    PAGE_HEADER_STYLE = Style(fg=cv.GRAY_35, bg=cv.GRAY_7)
    TABLE_HEADER_STYLE = Style(bold=True)
    KEY_TABLE_NAME_STYLE = Style(TABLE_HEADER_STYLE, fg=cv.YELLOW)
    KEY_STYLE = Style(bg=cv.GRAY_3)
    MOUSE_KEY_STYLE = Style(bg=cv.GRAY_3, fg=cv.LIGHT_YELLOW_3, italic=True)
    INVOKER_KEY_STYLE = Style(KEY_STYLE, fg=cv.RED)

    DOMAIN_TO_DOMAIN_STYLE_MAP: Dict[Pattern, Style] = {
        re.compile("^$"): NOOP_STYLE,
        re.compile("^mode$"): Style(fg=cv.YELLOW),
        re.compile("^es7s$"): Style(fg=cv.BLUE),
        re.compile("^w/a$"): Style(fg=cv.GRAY_50),
        re.compile("^xbindkeys$"): Style(fg=cv.MAGENTA),
        re.compile("^xdotool$"): Style(fg=cv.HI_MAGENTA),
        re.compile("^.+$"): Style(fg=cv.CYAN),
    }
    DOMAIN_TO_DESC_STYLE_MAP: Dict[Pattern, Style] = {
        re.compile("^(w/a)$"): Style(dim=True),
    }

    CONFIRMATION_REQ_STYLE = Style(fg=cv.HI_YELLOW)
    NO_CONFIRMATION_STYLE = Style(fg=cv.HI_RED)
    TUNNELABLE_STYLE = Style(fg=cv.HI_CYAN)

    MODIFIER_ALT_STYLE = Style(fg=cv.HI_GREEN, bg=cv.DARK_GREEN)
    MODIFIER_CTRL_STYLE = Style(fg=cv.HI_RED, bg=cv.DARK_RED_2)
    MODIFIER_SHIFT_STYLE = Style(fg=cv.HI_CYAN, bg=cv.DEEP_SKY_BLUE_7)
    MODIFIER_WIN_STYLE = Style(fg=cv.HI_BLUE, bg=cv.PURPLE_4)
    MODIFIER_SEPARATOR_STYLE = Style(KEY_STYLE, fg=cv.GRAY_35)

    DETAILS_STYLE = Style(fg=cv.GRAY_66)
    DETAILS_AUX_STYLE = Style(fg=cv.GRAY_35)
    COMMAND_PROG_STYLE = Style(fg=cv.BLUE, bold=True)
    REPEATABLE_STYLE = Style(fg=cv.HI_BLUE, bold=True)
    RAW_SEQ_STYLE = Style(fg=cv.YELLOW, bold=True)

    @classmethod
    def get_column_style(cls, column_attr: str, domain: str) -> Style:
        if column_attr == "sequence":
            return NOOP_STYLE
        if column_attr == "combo":
            return cls.KEY_STYLE
        if column_attr == "desc":
            return cls._match_map(domain, cls.DOMAIN_TO_DESC_STYLE_MAP)
        if column_attr == "desc_dot":
            return cls.get_domain_style(domain)
        if column_attr == "domain":
            return Style(cls.get_domain_style(domain), dim=True)
        raise KeyError(f"Invalid column attribute {column_attr}")

    @classmethod
    def get_domain_style(cls, domain: str) -> Style:
        return cls._match_map(domain, cls.DOMAIN_TO_DOMAIN_STYLE_MAP)

    @classmethod
    def _match_map(cls, subject: str | None, style_map: Dict[Pattern, Style]) -> Style:
        for regex, style in style_map.items():
            if regex.fullmatch(subject or ""):
                return style
        return NOOP_STYLE


@dataclass(frozen=True)
class BindTrait:
    key_char: str
    name: str
    style: Style


class BindTraitRegistry:
    TRAIT_LIST = [
        BindTrait("?", "Confirm before", StyleRegistry.CONFIRMATION_REQ_STYLE),
        BindTrait("!", "No confirm", StyleRegistry.NO_CONFIRMATION_STYLE),
        BindTrait("↡", "Tunnels down", StyleRegistry.TUNNELABLE_STYLE),
    ]

    TRAIT_MAP = {trait.key_char: trait for trait in TRAIT_LIST}


@total_ordering
@dataclass(repr=False)
class Sequence(Fragment):
    """
    Set of keystrokes.
    That's what tmux returns with `list-keys` command:
        <Keystrokes>      <Action>
    Example: "C-a C-z" (Ctrl+A, Ctrl+Z) -- default tmux sequence to suspend current client.
    """

    COMBO_PAD = " " * 1

    combos: List[KeyCombo]

    def __post_init__(self):
        if fakes := pt.others(KeyCombo, self.combos):
            raise TypeError(f"Expected KeyCombo instance, got:\n" + "\n".join(map(repr, fakes)))

    def render(self, _=None) -> str:
        return get_stdout().render(self.COMBO_PAD.join([c.render() for c in self.combos]))

    def __len__(self) -> int:
        return len(self.COMBO_PAD.join("c" * len(c) for c in self.combos))

    def __repr__(self) -> str:
        combos = [f"{c!r}" for c in self.combos]
        return self.__class__.__name__ + "[" + ",".join(combos) + "]"

    def __hash__(self) -> int:
        return sum(map(hash, self.combos))

    def __lt__(self, other: Sequence) -> bool:
        return self._compare(other) == -1

    def __eq__(self, other: Sequence) -> bool:
        return self._compare(other) == 0

    def _compare(self, other: Sequence) -> int:
        max_i = max(len(self.combos), len(other.combos))
        for i in range(0, max_i):
            if i >= len(self.combos):
                return 1
            if i >= len(other.combos):
                return -1
            if self.combos[i] > other.combos[i]:
                return 1
            if self.combos[i] < other.combos[i]:
                return -1
        return 0


@dataclass
class KeyCombo(Fragment, Sized):
    """
    Combination of *one* key and zero/one/more modifiers.
    Example: "C-b" (Ctrl+B), default prefix key binding.
    """

    MODIFIER_SEPARATOR = "-"
    KEY_PAD = " " * 1

    key: Key
    mods: List[Modifier]
    is_invoker: bool

    def __post_init__(self):
        self._string = self.key.label + "".join([mod.label for mod in self.mods])

    def render(self, renderer: IRenderer | t.Type[IRenderer] = None) -> str:
        rendered = ""
        key_style = StyleRegistry.KEY_STYLE
        mod_sep_style = StyleRegistry.MODIFIER_SEPARATOR_STYLE

        override_key_style = None
        if self.is_invoker:
            override_key_style = StyleRegistry.INVOKER_KEY_STYLE

        for mod in self.mods:
            rendered += mod.render()
            rendered += get_stdout().render(self.MODIFIER_SEPARATOR, mod_sep_style)

        if len(rendered) == 0:
            rendered += get_stdout().render(self.KEY_PAD, key_style)

        rendered += self.key.render(override_key_style)
        rendered += get_stdout().render(self.KEY_PAD, key_style)
        return rendered

    def __add__(self, other):
        return self.render() + other

    def __len__(self) -> int:
        result = 0
        for mod in self.mods:
            result += len(mod) + len(self.MODIFIER_SEPARATOR)
        if result == 0:
            result += len(self.KEY_PAD)
        return result + len(self.key) + len(self.KEY_PAD)

    def __repr__(self) -> str:
        mods = [f"{m.codes[0]}-" for m in self.mods]
        return self.__class__.__name__ + "[" + "".join(mods) + self.key.label + "]"

    def __hash__(self) -> int:
        return hash((self.key, *self.mods))

    def __lt__(self, other: KeyCombo) -> bool:
        return self._compare(other) < 0

    def __eq__(self, other: KeyCombo) -> bool:
        return self._compare(other) == 0

    def _compare(self, other: KeyCombo) -> int:
        result = 0
        if self.is_invoker:
            result += 10
        if other.is_invoker:
            result -= 10

        max_i = max(len(self.mods), len(other.mods))
        for i in range(0, max_i):
            if i >= len(self.mods):
                return result + 1
            if i >= len(other.mods):
                return result - 1
            if self.mods[i] > other.mods[i]:
                return result + 1
            if self.mods[i] < other.mods[i]:
                return result - 1

        if self.key > other.key:
            return result - 1
        if self.key < other.key:
            return result + 1
        return result


class KeyComboFactory:
    """
    Class that breaks down string key description into key definition and modifiers
    as a separate list, e.g: "M-S-Right" will become {Sequence} consisting
    of: {Key} "Right", {Modifier} "Alt", {Modifier} "Shift".
    """

    MODIFIER_REGEX = re.compile(r"^([MCSW])-")

    def __init__(self, invoker_callback: t.Callable):
        self._invoker_callback = invoker_callback

    def make(self, key: str | Key, *mods: Modifier) -> KeyCombo:
        if not isinstance(key, Key):
            key = Key(key)
        key_combo = KeyCombo(key, [*mods], False)
        if self._invoker_callback(key_combo):
            key_combo.is_invoker = True
        return key_combo

    def from_tmux(self, raw_combo: str) -> KeyCombo:
        if raw_combo.startswith('"') and raw_combo.endswith('"'):
            raw_combo = raw_combo.strip('"')
        if raw_combo.startswith("\\") and len(raw_combo) > 1:
            # because of parsing two different commands' results we can encounter single-escaped
            # form like '\\' as well as double-escaped form like '\\\\'; we are interested in
            # first character only though, so "unescaping" is fairly straightforward:
            raw_combo = raw_combo.removeprefix("\\")
        mods = []
        while mod_match := self.MODIFIER_REGEX.match(raw_combo):
            mods += [ModifierRegistry.find_by_code(mod_match.group(1))]
            raw_combo = raw_combo[mod_match.end(0):]
        return self.make(raw_combo, *mods)


@total_ordering
@dataclass(unsafe_hash=True)
class Key(Fragment, Sized):
    """
    Definition of a key.
    Examples: 'q', '1', 'Space', 'Enter'.
    """

    MOUSE_KEYS = [
        "lbtn",
        "rbtn",
        *(f"mb{n}" for n in range(3, 10)),
    ]

    LABEL_LEFT = "←"
    LABEL_RIGHT = "→"
    LABEL_UP = "↑"
    LABEL_DOWN = "↓"
    LABEL_UP_DOWN = "⇅"

    LABEL_OVERRIDE = {
        "Left": LABEL_LEFT,
        "Right": LABEL_RIGHT,
        "Up": LABEL_UP,
        "Down": LABEL_DOWN,
        "Arrows": LABEL_LEFT + LABEL_UP_DOWN + LABEL_RIGHT,
    }

    LABEL_TO_SORTER_MAP: ClassVar[OrderedDict[str, int]] = {
        char: idx
        for idx, char in enumerate(
            [
                *flatten1([c, c.upper()] for c in char_range("a", "z")),
                *"~`!@#$%^&*()-_=+[]{}\\|;:'\",.<>/?",
                *char_range("0", "9"),
                *['F'+str(n) for n in range(1, 25)],
                *LABEL_OVERRIDE.values(),
            ]
        )
    }

    label: str
    _sorter: int = field(default=len(LABEL_TO_SORTER_MAP), init=False)

    def __post_init__(self):
        for pattern, replace in self.LABEL_OVERRIDE.items():
            self.label = re.sub(pattern, replace, self.label)

        if len(self.label) == 1:
            self._sorter = self.LABEL_TO_SORTER_MAP.get(self.label[0], 0)
        elif num := re.search(r'(\d+)', self.label):  # e.g. F1-F12
            self._sorter = len(self.LABEL_TO_SORTER_MAP) + int(num.group(1))

        # else sort by a label (as string)

    @property
    def _style(self) -> Style:
        if self.is_mouse_key:
            return StyleRegistry.MOUSE_KEY_STYLE
        return StyleRegistry.KEY_STYLE

    @property
    def is_mouse_key(self) -> bool:
        return self.label.lower() in self.MOUSE_KEYS

    def render(self, override_style: Style = None) -> str:
        return get_stdout().render(self.label, (override_style or self._style))

    def __len__(self) -> int:
        return len(self.label)

    def __lt__(self, other: Key) -> bool:
        return self._compare(other) < 0

    def __eq__(self, other: Key) -> bool:
        return self._compare(other) == 0

    def _compare(self, other: Key) -> int:
        result = self._sorter - other._sorter

        if result == 0:
            if self.label > other.label:
                return result + 1
            if self.label < other.label:
                return result - 1
        return result


@total_ordering
@dataclass
class Modifier(Fragment, Sized):
    """
    Definition of supplementary key that doesn't have any actions bound, but
    instead alternates the action bound to other key.

    Default modifiers:
        C       Control
        M       Meta/Alt
        S       Shift
        W       Win/Super (x11 extension)
    """

    codes: list[str]
    out: str
    label: str
    style: Style = NOOP_STYLE

    def render(self, renderer: IRenderer | t.Type[IRenderer] = None) -> str:
        return get_stdout().render(self.out, self.style)

    def __hash__(self) -> int:
        return hash("".join(self.codes))

    def format_legend(self) -> Text:
        label_style = FrozenStyle(self.style, fg=DEFAULT_COLOR)
        first_ch_style = FrozenStyle(self.style, bold=True)
        return Fragment(KeyCombo.KEY_PAD + self.label[0], first_ch_style) + Fragment(
            f"{self.label[1:]}{KeyCombo.KEY_PAD}", label_style
        )

    def __len__(self) -> int:
        return len(self.out)

    def __lt__(self, other: Modifier) -> bool:
        return self._sorter < other._sorter

    def __eq__(self, other: Modifier) -> bool:
        return self._sorter == other._sorter

    @cached_property
    def _sorter(self):
        return -list(ModifierRegistry.MODIFIER_CODES_MAP.keys()).index(self.codes[0])


class ModifierRegistry:
    """
    Modifier defaults.
    """

    MODIFIER_CTRL = Modifier(
        ["C", "Primary"],
        out="C",
        label="Control",
        style=StyleRegistry.MODIFIER_CTRL_STYLE,
    )
    MODIFIER_ALT = Modifier(
        ["M", "Alt", "Meta"],
        out="M",
        label="Meta/Alt",
        style=StyleRegistry.MODIFIER_ALT_STYLE,
    )
    MODIFIER_SHIFT = Modifier(
        ["S", "Shift"],
        out="S",
        label="Shift",
        style=StyleRegistry.MODIFIER_SHIFT_STYLE,
    )
    MODIFIER_WIN = Modifier(
        ["W", "Super"],
        out="W",
        label="Win/Super",
        style=StyleRegistry.MODIFIER_WIN_STYLE,
    )

    MODIFIER_CODES_MAP: Dict[str, Modifier] = {
        k: v
        for k, v in flatten1(
            [
                *itertools.starmap(
                    lambda k, v: [(vv, k) for vv in v],
                    {
                        M: M.codes
                        for M in [
                            MODIFIER_CTRL,
                            MODIFIER_ALT,
                            MODIFIER_SHIFT,
                            MODIFIER_WIN,
                        ]
                    }.items(),
                )
            ]
        )
    }

    @classmethod
    def find_by_code(cls, code: str) -> Modifier:
        if code not in cls.MODIFIER_CODES_MAP.keys():
            raise KeyError(f'No modifier with combo "{code}" is registered')
        return cls.MODIFIER_CODES_MAP.get(code)


@total_ordering
@dataclass
class Bind:
    """
    Instance that defines binding some action with some key sequence.
    Example: "S-Up" sequence <-> "create new window" action.
    """

    DOMAIN_TO_SORTER_MAP = {
        "xbindkeys": -10,
        "xdotool": -20,
        "w/a": -30,
        "org/gnome/desktop/wm/keybindings": -40,
        "org/gnome/settings-daemon/plugins/media-keys": -50,
    }

    parent_table: BindKeyTable
    sequence: Sequence
    desc: Text
    domain: str = None
    command: BindCommand = None
    traits: list[BindTrait] = None

    @staticmethod
    def get_renderable_attrs() -> List[str]:
        return ["sequence", "desc_dot", "desc", "domain"]

    def pad_attr(self, attr: str) -> bool:
        return attr in ["sequence", "desc_dot", "desc"]

    def align_fn(self, attr: str) -> Callable[[str, int], str]:
        return rjust_sgr if attr in ["domain"] else ljust_sgr

    @property
    def desc_dot(self):
        return "·" if self.domain else " "

    def render_column(self, attr: str, col_style: Style) -> str:
        raw_val = getattr(self, attr) or ""
        max_len = self.parent_table.get_attr_max_len(attr)

        if isinstance(raw_val, IRenderable):
            if raw_val.allows_width_setup:  # @FIXME reduce manually if not
                raw_val.set_width(max_len)
            rendered = raw_val.render()
        else:
            rendered = get_stdout().render(raw_val[:max_len], col_style)

        return self.align_fn(attr)(rendered, max_len)

    def __repr__(self) -> str:
        attrs = map(
            str,
            [
                self.parent_table.name,
                repr(self.sequence),
                self.desc.render(),
                self.domain,
            ],
        )
        return self.__class__.__name__ + "[" + ", ".join(attrs) + "+]"

    def __lt__(self, other: Bind) -> bool:
        return self._compare(other) > 0

    def __eq__(self, other: Bind) -> bool:
        return self._compare(other) == 0

    @property
    def _sorter(self) -> int:
        return self.DOMAIN_TO_SORTER_MAP.get(self.domain, 0)

    def _compare(self, other: Bind) -> int:
        result = self._sorter - other._sorter

        if self.sequence > other.sequence:
            return result + 1
        if self.sequence < other.sequence:
            return result - 1
        return result


class BindKeyTable:
    def __init__(self, name: str, invoker: KeyCombo = None, label: str = None):
        self.name = name
        self.binds: List[Bind] = []
        self.invoker: KeyCombo | None = invoker
        self.label: str = (label or "").upper() + "  /"

        self._attrs_col_width_map: Dict[str, int] = dict(
            {k: 0 for k in Bind.get_renderable_attrs()}
        )

    def append(self, bind: Bind):
        self.binds.append(bind)

    def sort(self):
        self.binds.sort()

    def update_attrs_col_width(self):
        for bind in self.binds:
            for attr in Bind.get_renderable_attrs():
                cur_len = len(getattr(bind, attr) or "")
                max_len = self._attrs_col_width_map.get(attr)
                if max_len < cur_len:
                    self.set_attr_max_len(attr, cur_len)

    def get_attr_max_len(self, attr: str) -> int:
        return self._attrs_col_width_map.get(attr)

    def set_attr_max_len(self, attr: str, max_len: int):
        self._attrs_col_width_map[attr] = max(0, max_len)

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"[{len(self.binds)}]"


class MultipartInputError(RuntimeError):
    def __init__(self, split_idx: int):
        super().__init__("More granular splitting required")
        self.idx = split_idx


@dataclass(frozen=True)
class BindCommand:
    REPEATABLE_MARK = "(R) "

    command: str
    repeatable: bool
    raw_sequence: str = None

    def render(self, padding: int) -> Text:
        cur_width = 0
        max_width = get_terminal_width()
        result = Text()

        if self.command:
            cur_padding = padding + 2
            cur_width += cur_padding
            result += pad(cur_padding)

            if self.repeatable:
                cur_width += len(self.REPEATABLE_MARK)
                result += Fragment(self.REPEATABLE_MARK, StyleRegistry.REPEATABLE_STYLE)

            fragdefs = []
            for idx, part in enumerate(re.finditer(r"\S*|\s*", self.command)):
                part_str = part.group()
                try:
                    fragdefs.append((part_str, self.get_command_part_style(part_str, idx)))
                except MultipartInputError as e:
                    for subpart in [part_str[: e.idx], part_str[e.idx :]]:
                        fragdefs.append((subpart, self.get_command_part_style(subpart, idx)))

            for part_str, part_st in fragdefs:
                total_width = cur_width + len(part_str)

                if (diff := total_width - max_width) > 0:  # cant fit all
                    result += Fragment(
                        part_str[:-diff], part_st
                    )  # render left part on current line
                    part_str = part_str[-diff:]  # and right part on the next
                    cur_padding += 1
                    cur_width = cur_padding
                    result += "\n" + pad(cur_padding)

                cur_width += len(part_str)
                result += Fragment(part_str, part_st)

        if self.command and self.raw_sequence:
            result += "\n"

        if self.raw_sequence:
            cur_padding = padding + 2
            result += pad(cur_padding)
            for idx, part in enumerate(re.finditer(r"\w+|\W+", self.raw_sequence)):
                part_str = part.group()
                result += Fragment(part_str, self.get_raw_seq_part_style(part_str, idx))
        return result

    def get_command_part_style(self, co: str, idx: int) -> Style:
        if co.isspace():
            return NOOP_STYLE
        return StyleRegistry.DETAILS_STYLE

    def get_raw_seq_part_style(self, rc: str, idx: int) -> Style:
        return StyleRegistry.DETAILS_STYLE


class BindFactory:
    """
    tmux `list-keys` output parser.
    """

    def __init__(self, key_combo_factory: KeyComboFactory):
        self._key_combo_factory = key_combo_factory
        self._traits_buffer = []

    # def make(
    #     self,
    #     parent_table: BindKeyTable,
    #     domain: str,
    #     desc: Text,
    #     *combos: KeyCombo,
    #     command: BindCommand = None,
    #     traits: list[BindTrait] = None,
    # ) -> Bind:
    #     return Bind(parent_table, Sequence([*combos]), desc, domain, command, traits)

    def from_tmux(self, raw_bind: str, key_table: BindKeyTable) -> Bind:
        splitted = [s.strip() for s in re.split(r"\x1f|\s+", raw_bind)]

        combos = [self._key_combo_factory.from_tmux(splitted.pop(0))]
        if prefix := key_table.invoker:
            combos.insert(0, prefix)

        domain = None
        if splitted and (domain_match := re.fullmatch(r"^\[(.+)]$", splitted[0])):
            domain = domain_match.group(1)
            splitted.pop(0)

        desc_st = StyleRegistry.get_column_style("desc", domain)
        desc = Text(Fragment("", fmt=desc_st, close_this=False))
        self._traits_buffer.clear()
        while len(splitted) > 0:
            desc += self._apply_inline_trait_format(splitted.pop(0))
            if len(splitted):
                desc += " "

        return Bind(key_table, Sequence([*combos]), desc, domain, traits=self._traits_buffer)

    def from_dconf(self, opt: str, val: str, key_table: BindKeyTable) -> Bind:
        mods = []

        def add_mod(m: Match) -> str:
            modstr = m.group(1)
            mod = ModifierRegistry.find_by_code(modstr)
            mods.append(mod)
            return ""

        val = re.sub("<(Alt|Primary|Shift|Super)>", add_mod, val)
        key_combo = KeyCombo(Key(val), mods=mods, is_invoker=False)
        return Bind(key_table, Sequence([key_combo]), desc=Text(opt), domain='gnome')

    def _apply_inline_trait_format(self, word: str) -> Text | Fragment:
        for trait in BindTraitRegistry.TRAIT_LIST:
            if word.endswith(trait.key_char):
                self._traits_buffer.append(trait)
                return Fragment(word[:-1]) + Fragment(word[-1], trait.style)
        return Fragment(word)


class Formatter:
    OUT = sys.stdout

    PAGE_PAD: str = " " * 2
    COL_PAD = " " * 1
    SECT_PAD = " " * 4
    DOMAIN_DISPLAY_TERMW_THRESHOLD = 45

    def __init__(self, *bind_collector: IBindCollector):
        self._bind_collectors: list[IBindCollector] = [*bind_collector]

    def print(self):
        self._print_legend()

        for bind_collector in self._bind_collectors:
            self._print_binds(bind_collector)
            self._print_extras(bind_collector)

    def _print_legend(self):
        # @rewrite after pytermor 2.4+ is available
        defbg = StyleRegistry.PAGE_HEADER_STYLE.bg
        colpad = Fragment(self.COL_PAD, StyleRegistry.PAGE_HEADER_STYLE)
        sectpad = Fragment(self.SECT_PAD, StyleRegistry.PAGE_HEADER_STYLE)

        used_mouse_button = False
        used_mods = set()
        used_traits = []

        for collector in self._bind_collectors:
            used_mouse_button = used_mouse_button or collector.get_used_mouse_button()
            used_mods = used_mods.union(collector.get_used_mods())
            used_traits += collector.get_used_traits()

        def print_items():
            yield Fragment(self.PAGE_PAD + "LEGEND", StyleRegistry.PAGE_HEADER_STYLE)
            yield sectpad

            yield Fragment(" Key ", Style(StyleRegistry.KEY_STYLE, bg=cv.GRAY_0))
            if used_mouse_button:
                yield colpad
                yield Fragment(" MBtn ", Style(StyleRegistry.MOUSE_KEY_STYLE, bg=cv.GRAY_0))
            yield sectpad

            mods_to_print = used_mods.copy()
            for idx, mod in enumerate(ModifierRegistry.MODIFIER_CODES_MAP.values()):
                if mod not in mods_to_print:
                    continue
                mods_to_print.remove(mod)
                if idx > 0:
                    yield colpad
                yield mod.format_legend()
            yield sectpad

            for idx, trait in enumerate(BindTraitRegistry.TRAIT_LIST):
                if trait not in used_traits:
                    continue
                if idx > 0:
                    yield from [colpad] * 2
                yield Fragment(trait.key_char, Style(trait.style, bg=defbg))
                yield Fragment(f" {trait.name}", Style(bg=defbg))

        line = Text()
        for item in print_items():
            line += item

        blank = Text(
            self.PAGE_PAD + " " * max(get_terminal_width(), len(line.raw())),
            StyleRegistry.PAGE_HEADER_STYLE,
        )
        stdout = get_stdout()
        stdout.echo_rendered(blank)
        stdout.echo_rendered(
            line
            + Fragment(
                " " * (get_terminal_width() - len(line.raw())) + self.PAGE_PAD,
                StyleRegistry.PAGE_HEADER_STYLE,
            ),
        )
        stdout.echo_rendered(blank)
        stdout.echo()

    def _print_binds(self, bind_collector: IBindCollector):
        attrs_render_list = Bind.get_renderable_attrs()
        if (termw := get_terminal_width()) <= self.DOMAIN_DISPLAY_TERMW_THRESHOLD:
            attrs_render_list.remove("domain")
            for key_table in bind_collector.get_key_tables():
                key_table.set_attr_max_len("domain", 0)

        stdout = get_stdout()
        for key_table in bind_collector.get_key_tables():
                self._compute_max_desc_len(key_table, attrs_render_list)

                stdout.echo_rendered(
                    self.PAGE_PAD
                    + Fragment(key_table.label, StyleRegistry.TABLE_HEADER_STYLE)
                    + "  "
                    + Fragment(key_table.name, StyleRegistry.KEY_TABLE_NAME_STYLE)
                    + "  "
                    + Fragment(
                        " " * (termw - len(key_table.name) - len(key_table.label) - 5),
                        Style(fg=cv.GRAY_23, crosslined=True),
                    )
                    + " ",
                )
                stdout.echo()

                for bind in key_table.binds:
                    columns_rendered = self.PAGE_PAD + self.COL_PAD  # for leftmost pad
                    details_padding = len(columns_rendered)

                    for attr in attrs_render_list:
                        details_padding_part = attr in ("sequence", "desc_dot")
                        col_style = StyleRegistry.get_column_style(attr, bind.domain)

                        column_rendered = bind.render_column(attr, col_style)
                        if details_padding_part:
                            details_padding += bind.parent_table.get_attr_max_len(attr)

                        if bind.pad_attr(attr):
                            column_rendered += self.COL_PAD
                            if details_padding_part:
                                details_padding += len(self.COL_PAD)
                        columns_rendered += column_rendered

                    stdout.echo(columns_rendered)
                    if bind_collector._details:
                        details_rendered = [pad(details_padding)]
                        if bind.command:
                            details_rendered = bind.command.render(details_padding)
                        stdout.echo_rendered(details_rendered)

                stdout.echo()

    def _print_extras(self, bind_collector: IBindCollector):
        for l in (bind_collector.render_extras() or []):
            get_stdout().echo(l)


    @classmethod
    def _compute_max_desc_len(cls, key_table: BindKeyTable, attrs_render_list: List[str]):
        total_len = sum(key_table.get_attr_max_len(attr) for attr in attrs_render_list) + len(
            cls.COL_PAD
        ) * len(
            attrs_render_list
        )  # pads between columns + leftmost
        term_width = get_terminal_width()

        delta = term_width - total_len
        key_table.set_attr_max_len("desc", key_table.get_attr_max_len("desc") + delta)
