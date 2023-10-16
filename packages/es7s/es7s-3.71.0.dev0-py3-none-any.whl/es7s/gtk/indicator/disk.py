# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from functools import cached_property

from pytermor import format_auto_float, formatter_bytes_human, StaticFormatter

from es7s.commons import SocketMessage
from es7s.shared import DiskUsageInfo, DiskInfo, DiskIoInfo
from ._base import _BaseIndicator
from ._icon_selector import ThresholdIconSelector, IconEnum, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class DiskIconEnum(IconEnum):
    WAIT = "wait.svg"


class DiskIconPartBusyEnum(IconEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAX = "max"


_busy_threshold_map = ThresholdMap(
    **{
        DiskIconPartBusyEnum.MAX.value: 95,
        DiskIconPartBusyEnum.HIGH.value: 75,
        DiskIconPartBusyEnum.MEDIUM.value: 25,
        DiskIconPartBusyEnum.LOW.value: 0,
    },
    caution=75,
    alert=95,
)


class DiskIconSelector(ThresholdIconSelector):
    @cached_property
    def icon_names_set(self) -> set[str]:
        return {*DiskIconEnum, *super().icon_names_set}


class IndicatorDisk(_BaseIndicator[DiskInfo, DiskIconSelector]):
    def __init__(self):
        self.config_section = "indicator.disk"

        self._show_perc = _BoolState(
            config_var=(self.config_section, "label-used"),
            gconfig=CheckMenuItemConfig("Show used space (%)", sep_before=True),
        )
        self._show_bytes = _BoolState(
            config_var=(self.config_section, "label-free"),
            gconfig=CheckMenuItemConfig("Show free space (GB/TB)"),
        )

        self._show_busy = _BoolState(
            config_var=(self.config_section, "label-busy"),
            gconfig=CheckMenuItemConfig("Show busy ratio (%)", sep_before=True),
        )

        self._show_io_off = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No IO speed", sep_before=True, group=self.config_section),
        )
        self._show_io_read = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="read",
            gconfig=RadioMenuItemConfig("Show read speed (bytes/s)", group=self.config_section),
        )
        self._show_io_write = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="write",
            gconfig=RadioMenuItemConfig("Show write speed (bytes/s)", group=self.config_section),
        )
        self._show_io_both = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="both",
            gconfig=RadioMenuItemConfig("Show both speeds (bytes/s)", group=self.config_section),
        )
        self._show_io_total = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="total",
            gconfig=RadioMenuItemConfig("Show total speed (sum, bytes/s)", group=self.config_section),
        )

        self._used_warn_ratio: float | None = self.uconfig().get("used-warn-level-ratio", float)
        self._busy_warn_ratio: float | None = self.uconfig().get("busy-warn-level-ratio", float)
        self._formatter_io = StaticFormatter(
            formatter_bytes_human,
            max_value_len=4,
            discrete_input=False,
            prefix_refpoint_shift=2,
        )

        super().__init__(
            indicator_name="disk",
            socket_topic=["disk-usage", "disk-io"],
            icon_selector=DiskIconSelector(
                _busy_threshold_map,
                ThresholdMap(100, 99, 98, 95, 92, *range(90, -10, -10)),
                subpath="disk",
                path_dynamic_tpl="%s-%s.svg",
                name_default=DiskIconEnum.WAIT,
            ),
            title="Storage",
            states=[
                self._show_perc,
                self._show_bytes,
                self._show_busy,
                self._show_io_off,
                self._show_io_read,
                self._show_io_write,
                self._show_io_both,
                self._show_io_total,
            ],
        )

    #
    def _render(self, msg: SocketMessage[DiskInfo]):
        usage_dto = self._get_last_dto(DiskUsageInfo)
        io_dto = self._get_last_dto(DiskIoInfo)

        if isinstance(msg.data, DiskUsageInfo):
            usage_dto = msg.data
        elif isinstance(msg.data, DiskIoInfo):
            io_dto = msg.data

        details = []
        used_perc = None
        used_ratio = None
        usage_free = None

        if usage_dto:
            used_perc = usage_dto.used_perc
            used_ratio = used_perc / 100
            usage_free = usage_dto.free
            details.append(
                " / ".join(
                    [
                        self._format_used_value(used_ratio) + " used",
                        "".join(self._format_free_value(round(usage_dto.free))) + " free",
                    ]
                )
            )

        io_read_mbps = None
        io_write_mbps = None
        io_busy_ratio = None
        io_busy_perc = None

        if io_dto:
            io_read_mbps = io_dto.read.mbps
            io_write_mbps = io_dto.write.mbps
            io_busy_perc = 100 * io_dto.busy_ratio
            io_busy_ratio = io_dto.busy_ratio
            details.extend(
                [
                    self._format_details_busy_ratio(io_busy_ratio),
                    self._format_io_value("R↑", io_dto.read.mbps)
                    + " / "
                    + self._format_io_value("W↓", io_dto.write.mbps),
                ]
            )

        self._update_details(" · ".join(details))
        self._render_result(
            self._format_result(used_ratio, usage_free, io_busy_perc, io_read_mbps, io_write_mbps),
            self._format_result(100, 1e10, 100, io_read_mbps, io_write_mbps),
            self._is_warning(used_ratio, io_busy_ratio),  # warning,
            self._icon_selector.select(io_busy_perc, used_perc),
        )

    def _is_warning(self, used_ratio: float | None, busy_ratio: float | None) -> bool:
        used_warn = self._used_warn_ratio and used_ratio and used_ratio >= self._used_warn_ratio
        busy_warn = self._busy_warn_ratio and busy_ratio and busy_ratio >= self._busy_warn_ratio
        return used_warn or busy_warn

    def _format_result(
        self,
        used_ratio: float = None,
        free: float = None,
        io_busy_perc: float = None,
        read_mbps: float = None,
        write_mbps: float = None,
    ) -> str:
        parts = []
        if used_ratio is not None and self._show_perc:
            parts += [self._format_used_value(used_ratio)]
        if free is not None and self._show_bytes:
            parts += ["".join(self._format_free_value(round(free)))]

        if io_busy_perc is not None and self._show_busy:
            parts += [self._format_busy_ratio(io_busy_perc)]

        if self._show_io_total:
            if read_mbps is not None and write_mbps is not None:
                parts.append(self._format_io_value("", read_mbps + write_mbps))
        else:
            if read_mbps is not None and (self._show_io_read or self._show_io_both):
                parts.append(self._format_io_value("↑", read_mbps))
            if write_mbps is not None and (self._show_io_write or self._show_io_both):
                parts.append(self._format_io_value("↓", write_mbps))

        return " ".join(parts).rstrip()

    def _format_used_value(self, used_ratio: float) -> str:
        return f"{100 * used_ratio:3.0f}%"

    def _format_free_value(self, free: int) -> tuple[str, str]:
        free_gb = free / 1000**3
        free_tb = free / 1000**4
        if free_gb < 1:
            return "< 1G", ""
        if free_gb < 1000:
            return format_auto_float(free_gb, 3, False), "G"
        return format_auto_float(free_tb, 3, False), "T"

    def _format_io_value(self, type: str, mbps: float) -> str:
        return f"{type}{self._formatter_io.format(mbps)}"

    def _format_busy_ratio(self, io_busy_perc: float | None) -> str:
        return f"{io_busy_perc:3.0f}%"

    def _format_details_busy_ratio(self, io_busy_ratio: float | None) -> str:
        busy_str = "---"
        if io_busy_ratio is not None:
            busy_str = f"{100 * io_busy_ratio:.0f}%"
        return f"{busy_str} busy"
