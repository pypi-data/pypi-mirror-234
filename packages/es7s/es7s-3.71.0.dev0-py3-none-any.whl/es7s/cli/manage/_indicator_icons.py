# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import copy
import itertools
import re
import typing as t
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from importlib import resources

import pytermor as pt
from bs4 import BeautifulSoup

from es7s.shared import (
    get_logger,
    RESOURCE_PACKAGE,
    ProgressBar,
)


class IndicatorColor(pt.ExtendedEnum):
    NOOP = pt.NOOP_COLOR
    BACKGROUND = pt.ColorRGB(0x4D4D4D)
    DEFAULT = pt.ColorRGB(0x989FA6)
    ACTIVE = pt.ColorRGB(0xFFFFFF)
    FULL_DARK = pt.ColorRGB(0x687E47)
    WARN_DARK = pt.ColorRGB(0xB76E32)
    ERROR_DARK = pt.ColorRGB(0xCC2B26)
    FULL = pt.ColorRGB(0xD2FF8F)
    WARN = pt.ColorRGB(0xD18E58)
    ERROR = pt.ColorRGB(0xFF5B56)
    VPN_FOREIGN = pt.ColorRGB(0x929AC4)
    VPN_FOREIGN_ACCENT = pt.ColorRGB(0x3767FF)

    def format_value(self) -> str:
        return self.value.format_value("#")

    def __bool__(self) -> bool:
        return bool(self.value)


@dataclass(frozen=True)
class IndicatorStyle:
    fill: IndicatorColor = IndicatorColor.NOOP
    stroke: IndicatorColor = IndicatorColor.NOOP
    fill_opacity: float = None
    stroke_width: float = None

    def compose(self, base: dict[str, str] = None) -> str:
        if self.fill:
            base.update({"fill": self.fill.format_value()})
        if self.fill_opacity is not None and self.fill_opacity != 1.0:
            base.update({"fill-opacity": f"{self.fill_opacity:.2f}"})
        if self.stroke:
            base.update({"stroke": self.stroke.format_value()})
        if self.stroke_width is not None and self.stroke_width != 1.0:
            base.update({"stroke-width": f"{self.stroke_width:.2f}"})
        return ";".join(f"{k}:{v}" for k, v in base.items())

    def __repr__(self):
        return f"<{pt.get_qname(self)}>[{self.compose()}]"


class IndicatorStyles:
    WARN = IndicatorStyle(IndicatorColor.WARN, IndicatorColor.WARN_DARK)
    ERROR = IndicatorStyle(IndicatorColor.ERROR, IndicatorColor.ERROR_DARK)
    FULL = IndicatorStyle(IndicatorColor.FULL, IndicatorColor.FULL_DARK)


class GenericSvgAction(metaclass=ABCMeta):
    def __init__(self, tag: str, key: str = "id", *query: str | re.Pattern):
        self._tag = tag
        self._key = key
        self._queries = [*query]

    def invoke(self, template: BeautifulSoup):
        for query in self._queries:
            if isinstance(query, str):
                el = template.find(self._tag, {self._key: query})
                self._invoke_or_die(el, query)
                continue

            matched = False
            for el in template.find_all(self._tag):
                if query.match(el.attrs.get(self._key)):
                    self._invoke(el)
                    matched = True
            if not matched:
                self._fail(f"No matches for", query)

    def _invoke_or_die(self, el: BeautifulSoup, query: str | re.Pattern):
        if not el:
            self._fail(f"Not found", query)
        self._invoke(el)

    @abstractmethod
    def _invoke(self, el: BeautifulSoup):
        ...

    def __repr__(self):
        return f'<{pt.get_qname(self)}>[{", ".join(map(repr, self._repr_attrs()))}]'

    def _repr_attrs(self) -> t.Iterable[any]:
        yield from self._queries

    def _fail(self, msg: str, query: str | re.Pattern):
        query_str = query.pattern if isinstance(query, re.Pattern) else query
        raise RuntimeError(f"{msg}: {self._tag}[{self._key}={query_str!r}]")


class UpdatePathStyleAction(GenericSvgAction):
    def __init__(self, style: IndicatorStyle|IndicatorColor, *query: str | re.Pattern):
        super().__init__("path", "id", *query)

        if isinstance(style, IndicatorColor):
            self._style = IndicatorStyle(fill=style)
        else:
            self._style = style

    def _invoke(self, el: BeautifulSoup | None):
        base_style = dict()
        if (el_style := el.get("style")):
            base_style = el_style.split(";")
        base = {k: v for k, v in (bs.split(":") for bs in base_style)}
        attrs = {"style": self._style.compose(base=base)}
        el.attrs.update(attrs)

    def _repr_attrs(self) -> t.Iterable[any]:
        yield self._style
        yield from super()._repr_attrs()


class GenericRemoveAction(GenericSvgAction):
    def _invoke(self, el: BeautifulSoup):
        get_logger().debug(f"Removing element {el!r}")
        el.decompose()


class RemovePathAction(GenericRemoveAction):
    def __init__(self, *query: str | re.Pattern):
        super().__init__("path", "id", *query)


class RemoveGroupAction(GenericRemoveAction):
    def __init__(self, *query: str | re.Pattern):
        super().__init__("g", "id", *query)


class Variation:
    def __init__(self, id: str = None, *acts: GenericSvgAction):
        self._id = id
        self._acts = acts

    @property
    def id(self) -> str:
        return self._id or ""

    def invoke(self, template: BeautifulSoup):
        for act in self._acts:
            try:
                act.invoke(template)
            except RuntimeError as e:
                raise RuntimeError(f"{pt.get_qname(act)} failure: {e}")

    def __repr__(self):
        attrs = [
            self._id,
            *self._acts,
        ]
        return f'<{pt.get_qname(self)}>[{", ".join(map(repr, attrs))}]'


class IndicatorIconBuilder(metaclass=ABCMeta):
    _TYPE: t.ClassVar[str]

    def __init__(self, pbar: ProgressBar):
        self.pbar: ProgressBar = pbar
        self._last_label: str | None = None

    @abstractmethod
    def _get_type(self) -> str:
        ...

    @abstractmethod
    def _get_base_actions(self) -> t.Iterable[GenericSvgAction]:
        ...

    @abstractmethod
    def _get_variation_lists(self) -> t.Iterable[t.Iterable[Variation]]:
        ...

    def run(self, dry_run: bool) -> tuple[int, int]:
        logger = get_logger()
        success, total = 0, 0

        combinations = [*itertools.product(*self._get_variation_lists())]
        fid_tpl_parts = []
        for vl in self._get_variation_lists():
            max_vid = max(len(v.id) for v in vl)
            fid_tpl_parts.append(f"%{max_vid}s")
        fid_tpl = ' '.join(fid_tpl_parts)

        origin_template = get_icon_template(self._get_type())
        base_template = copy.copy(origin_template)
        for m in self._get_base_actions():
            m.invoke(base_template)

        total = len(combinations)
        self.pbar.init_steps(steps_amount=total)
        for idx, comb in enumerate(combinations):
            dpath = resources.files("es7s").joinpath(f"data/icons/{self._TYPE}/")
            fid = "-".join(pt.filterf(v.id for v in comb))
            fid_fw = fid_tpl % (*[v.id for v in comb],)
            idstr = f"[{idx:{len(str(total))}d}/{total}][{fid_fw}]"
            fpath = str(dpath.joinpath(f"{fid}.svg"))

            self.pbar.next_step(step_label=fpath)

            result = copy.copy(base_template)

            try:
                for v in comb:
                    v.invoke(result)
            except RuntimeError as e:
                logger.warning(f"{idstr} {e}")
                continue

            if dry_run:
                pass
            else:
                with open(fpath, "wt") as f:
                    f.write(str(result))

            logger.debug(f"{idstr} Wrote {fpath!r}")
            success += 1

        return success, total


def get_icon_template(name: str) -> BeautifulSoup:
    from bs4 import BeautifulSoup

    pkg = f"{RESOURCE_PACKAGE}.icons._sources"
    res = f"{name}.svg"
    f = resources.open_text(pkg, res)
    return BeautifulSoup(f, "xml")
