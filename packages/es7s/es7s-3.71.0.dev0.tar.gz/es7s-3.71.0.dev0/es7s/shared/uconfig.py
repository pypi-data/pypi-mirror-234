# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import configparser
import os
import typing as t
from abc import abstractmethod
from collections import deque, OrderedDict
from configparser import ConfigParser as BaseConfigParser
from dataclasses import dataclass
from functools import cached_property
from importlib import resources
from os import makedirs, path
from os.path import dirname, isfile

import pytermor as pt

from .log import get_logger
from ..commons.pt_ import format_attrs, format_path
from .path import RESOURCE_PACKAGE, get_user_data_dir, get_user_config_dir

_merged_uconfig: UserConfig | None = None
_default_uconfig: UserConfig | None = None


@dataclass
class UserConfigParams:
    default: bool = False


class UserConfig(BaseConfigParser):
    _init_hooks: t.ClassVar[deque[t.Callable[[], None]]] = deque()

    @classmethod
    def add_init_hook(cls, fn: t.Callable[[UserConfig], None]) -> None:
        cls._init_hooks.append(fn)

    @classmethod
    def trigger_init_hooks(cls, instance):
        while len(cls._init_hooks):
            cls._init_hooks.popleft()(uconfig_instance=instance)

    def __init__(self, params: UserConfigParams = None):
        self.params = params or UserConfigParams()
        super().__init__(interpolation=None)

        self._invalid: RuntimeError | None = None
        # @TODO сделать общим для логгера
        self._already_logged_options: OrderedDict = OrderedDict[t.Tuple[str, str, str], int]()

    # def read(self, *args) -> list[str]:
    #     if not (read_ok := super().read(*args)):
    #         return read_ok
    #     self._sectproxy = SectionProxy(self._sections)
    #     return read_ok

    def get(self, section: str, option: str, *args, **kwargs) -> t.Any:
        self.ensure_validity()
        log_msg = f"Getting config value: {section}.{option}"
        result = None
        try:
            result = super().get(section, option, *args, **kwargs)
        except Exception:
            raise
        finally:
            if (key := (section, option, result)) not in self._already_logged_options:
                self._already_logged_options.update({key: 0})
                log_msg += f" = " + (
                    '"' + str(result).replace("\n", " ") + '"' if result else str(result)
                )
                get_logger().debug(log_msg)
            self._already_logged_options.update({key: self._already_logged_options.get(key) + 1})
        return result

    def get_section(self, section: str) -> UserConfigSection:
        if not self.has_section(section):
            raise ValueError("No such section: %s" % section)
        return UserConfigSection(section, self)

    def get_module_section(self, origin: any) -> UserConfigSection:
        parts = [p.strip("_") for p in origin.__module__.split(".") if not p.startswith('.')]
        start_idx = 1
        if len(parts) > 2:
            start_idx = 2
        section = ".".join(parts[start_idx:]).replace("_", "-")
        # es7s.cli.exec_.autoterm -> exec.autoterm
        # es7s.shared.log -> log
        return self.get_section(section)

    def get_subsections(self, section: str) -> list[str]:
        return [*filter(lambda s: s.startswith(section + "."), self.sections())]

    def get_monitor_debug_mode(self) -> bool:
        return CascadeVarSelector(
            EnvVarLoader("ES7S_MONITOR_DEBUG"),
            BoolVarLoader(lambda _: get_logger().setup.display_monitor_debugging_markup),
            ConfigVarLoader(self.get_section("monitor"), "debug"),
            target=bool,
        ).invoke()

    @cached_property
    def indicator_debug_mode(self) -> bool:
        return CascadeVarSelector(
            EnvVarLoader("ES7S_INDICATOR_DEBUG"),
            ConfigVarLoader(self.get_section("indicator"), "debug"),
            target=bool,
        ).invoke()

    @cached_property
    def indicator_single_mode(self) -> str:
        return CascadeVarSelector(
            EnvVarLoader("ES7S_INDICATOR_SINGLE"),
            ConfigVarLoader(self.get_section("indicator"), "single"),
        ).invoke()

    def get_cli_debug_io_mode(self) -> bool:
        with get_logger(require=True).silencio():
            return CascadeVarSelector(
                EnvVarLoader("ES7S_CLI_DEBUG_IO"),
                ConfigVarLoader(self.get_section("cli"), "debug-io"),
                target=bool,
            ).invoke()

    def invalidate(self):
        self._invalid = True

    def ensure_validity(self):
        if self._invalid:
            raise RuntimeError(
                "Config can be outdated. Do not cache config instances (at most "
                "-- store as local variables in the scope of the single function), "
                "call get_config() to get the fresh one instead."
            )

    def set(self, section: str, option: str, value: str | None = ...) -> None:
        raise RuntimeError(
            "Do not call set() directly, use rewrite_user_value(). "
            "Setting config values directly can lead to writing default "
            "values into user's config even if they weren't there at "
            "the first place."
        )

    def _set(self, section: str, option: str, value: str | None = ...) -> None:
        self.ensure_validity()
        log_msg = f'Setting config value: {section}.{option} = "{value}"'
        get_logger().info(log_msg)

        super().set(section, option, value)


VarValue = str | int | float | bool


class CascadeVarSelector:
    def __init__(
        self, *loaders: IVarLoader, target: VarValue|type[VarValue] = str
    ):
        self._loaders = [*loaders]
        self._fallback: VarValue = target() if isinstance(target, type) else target
        self._rtype: type[VarValue] = target if isinstance(target, type) else type(self._fallback)

    def __call__(self) -> VarValue | None:
        return self.invoke()

    def invoke(self) -> VarValue | None:
        for loader in self._loaders:
            if not loader.is_set:
                continue
            return self._convert(loader.value)
        return self._convert(self._fallback)

    def _convert(self, val: VarValue | None) -> VarValue | None:
        result = UserConfigSection.convert(val, self._rtype)
        get_logger(require=False).debug(f"{self!r}: {val} -> {result}")
        return result

    def __repr__(self):
        name = '<static>' if not self._loaders else self._loaders[0]._name
        return f'{pt.get_qname(self)}[{name}, {len(self._loaders)}, {self._fallback}]'


class IVarLoader:
    def __init__(self, name: str, treat_empty_as_set=True):
        self._name = name
        self._treat_empty_as_set = not treat_empty_as_set

    @cached_property
    def is_set(self) -> bool:
        if self.is_unset:
            return False
        if self.is_empty:
            return self._treat_empty_as_set
        return True

    @cached_property
    @abstractmethod
    def is_unset(self) -> bool:
        ...

    @cached_property
    def is_empty(self) -> bool:
        return self.value == ""

    @cached_property
    def value(self) -> str:
        get_logger(require=False).debug(f"Invoking {self!r}")
        if (val := self._load()) is None:
            raise ValueError(f"Var {self._name} cannot be loaded because it is unset")
        if isinstance(val, str):
            self._check_trimmable(val)
        return val

    @abstractmethod
    def _load(self) -> str:
        ...

    def _check_trimmable(self, val: str):
        if val != val.strip():
            get_logger(require=False).warning(f"Leading/trailing spaces in {self._name}: {val!r}")

    def __repr__(self):
        return f"{pt.get_qname(self)}[{self._name}, EMPTY_IS_{['UN', ''][self._treat_empty_as_set]}SET]"


class EnvVarLoader(IVarLoader):
    @property
    def is_unset(self) -> bool:
        return os.getenv(self._name, default=None) is None

    def _load(self) -> str:
        return os.getenv(self._name)


class ConfigVarLoader(IVarLoader):
    def __init__(self, config: UserConfigSection, name: str, treat_empty_as_set=True):
        self._config = config
        super().__init__(name, treat_empty_as_set)

    @property
    def is_unset(self) -> bool:
        return self._config.get(self._name, fallback=None) is None

    def _load(self) -> str:
        return self._config.get(self._name)


class BoolVarLoader(IVarLoader):
    def __init__(
        self,
        load_fn: t.Callable[[BoolVarLoader], bool],
        is_unset_fn: t.Callable[[BoolVarLoader], bool] = None,
        treat_empty_as_set=True,
    ):
        self._load_fn = load_fn
        self._is_unset_fn = is_unset_fn or (lambda _: load_fn(_) is None)
        super().__init__(f"({repr(load_fn)})", treat_empty_as_set)

    @property
    def is_unset(self) -> bool:
        return self._is_unset_fn(self)

    def _load(self) -> str:
        return ["false", "true"][self._load_fn(self)]


class UserConfigSection:
    _UNSET = object()

    def __init__(self, section_name: str, user_config: UserConfig):
        self._section_name = section_name
        self._user_config = user_config

    def get(
        self,
        option: str,
        rtype: type = str,
        eltype: type = None,
        fallback=_UNSET,
        *args,
        **kwargs,
    ) -> t.Any:
        """
        Throws an exception if the value is unset and no `fallback` provided.

        :param option: option name
        :param rtype: result type (str|int|float|bool|list|set)
        :param eltype: element type for iterable results (str|int|float|bool)
        :param fallback: default value
        """
        result = self._user_config.get(
            self._section_name, option, *args, fallback=fallback, **kwargs
        )
        return self.convert(result, rtype, eltype)

    @staticmethod
    def _convert_to_boolean(val) -> bool|None:
        return UserConfig.BOOLEAN_STATES.get(str(val).strip().lower(), None)

    @staticmethod
    def convert(val: any, rtype: type = str, eltype: type = None):
        if not rtype:
            return val
        if rtype == bool:
            if (bool_result := UserConfigSection._convert_to_boolean(val)) is not None:
                return bool_result
        if rtype != str and isinstance(rtype(), t.Iterable):
            return rtype(eltype(v) for v in val.splitlines() if v.strip())
        return rtype(val)


def get_default_filepath() -> str:
    filename = "es7s.conf.d"
    user_path = get_user_data_dir() / filename
    get_logger(require=False).debug(f"User config path:   {format_path(user_path)}")

    if user_path.is_file():
        if user_path.is_symlink():
            return os.readlink(user_path)
        return str(user_path)
    else:
        dc_filepath = str(resources.path(RESOURCE_PACKAGE, "es7s.conf.d"))
        if not os.environ.get("ES7S_TESTS", None):
            get_logger(require=False).warning(
                f"Dist(=default) config not found in user data dir, "
                f"loading from app data dir instead: {format_path(dc_filepath)}"
            )
        return str(dc_filepath)


def get_local_filepath() -> str:
    local_dir = get_user_config_dir()
    local_path = path.join(local_dir, "es7s.conf")

    get_logger(require=False).debug(f"Local config path:  {format_path(local_path)}")
    return local_path


def get_merged(require=True) -> UserConfig | None:
    if not _merged_uconfig:
        if require:
            raise pt.exception.NotInitializedError(UserConfig)
        return None
    return _merged_uconfig


def get_dist() -> UserConfig | None:
    return _default_uconfig


def get_for(origin: object, require=True) -> UserConfigSection | None:
    try:
        return get_merged(require).get_module_section(origin)
    except pt.exception.NotInitializedError:
        if require:
            raise
        return None


def init(params: UserConfigParams = None) -> UserConfig:
    for k, v in os.environ.items():
        if k.startswith("ES7S"):
            get_logger().debug(f"Environ: {k:30s}={format_attrs(v)}")

    global _default_uconfig, _merged_uconfig
    default_filepath = get_default_filepath()
    local_filepath = get_local_filepath()

    if _default_uconfig:
        _default_uconfig.invalidate()
    try:
        _default_uconfig = _make(default_filepath)
    except RuntimeError as e:
        raise RuntimeError("Failed to initialize default config, cannot proceed") from e

    if not isfile(local_filepath):
        reset(False)

    filepaths = [default_filepath]
    if params and not params.default:
        filepaths += [local_filepath]

    if _merged_uconfig:
        _merged_uconfig.invalidate()

    try:
        _merged_uconfig = _make(*filepaths, params=params)
    except RuntimeError as e:
        get_logger().warning(
            f"Failed to initialize user config, falling back to default @TODO: {e}"
        )
        raise e

    get_logger().info("Configs initialized")
    UserConfig.trigger_init_hooks(_merged_uconfig)
    return _merged_uconfig


def _make(*filepaths: str, params: UserConfigParams = None) -> UserConfig:
    uconfig = UserConfig(params)
    read_ok = []

    try:
        read_ok = uconfig.read(filepaths)
    except configparser.Error as e:
        get_logger().exception(e)

    get_logger().info("Merging config from " + format_attrs(map(format_path, filepaths)))

    if len(read_ok) != len(filepaths):
        read_failed = set(filepaths) - set(read_ok)
        get_logger().warning("Failed to read config(s): " + ", ".join(read_failed))
    if len(read_ok) == 0:
        raise RuntimeError(f"Failed to initialize config")
    return uconfig


def reset(backup: bool = True) -> str | None:
    """Return path to backup file, if any."""
    user_config_filepath = get_local_filepath()
    makedirs(dirname(user_config_filepath), exist_ok=True)
    get_logger().debug(f'Making default config in: "{user_config_filepath}"')

    user_backup_filepath = None
    if backup and os.path.exists(user_config_filepath):
        user_backup_filepath = user_config_filepath + ".bak"
        os.rename(user_config_filepath, user_backup_filepath)
        get_logger().info(f'Original file renamed to: "{user_backup_filepath}"')

    header = True
    with open(user_config_filepath, "wt") as user_cfg:
        with open(get_default_filepath(), "rt") as default_cfg:
            for idx, line in enumerate(default_cfg.readlines()):
                if header and line.startswith(("#", ";", "\n")):
                    continue  # remove default config header comments
                header = False

                if line.startswith(("#", "\n")):  # remove section separators
                    continue  # and empty lines
                elif line.startswith("["):  # keep section definitions, and
                    if user_cfg.tell():  # prepend the first one with a newline
                        line = "\n" + line
                elif line.startswith("syntax-version"):  # keep syntax-version
                    pass
                elif line.startswith(";"):  # keep examples, triple-comment out to distinguish
                    line = "###" + line.removeprefix(";")
                else:  # keep default values as commented out examples
                    line = "# " + line

                user_cfg.write(line)
                get_logger().trace(line.strip(), f"{idx+1}| ")

    return user_backup_filepath


def rewrite_value(section: str, option: str, value: str | None) -> None:
    local_filepath = get_local_filepath()
    source_uconfig = _make(local_filepath)

    if not source_uconfig.has_section(section):
        source_uconfig.add_section(section)
    source_uconfig._set(section, option, value)  # noqa

    get_logger().debug(f'Writing config to: "{local_filepath}"')
    with open(local_filepath, "wt") as user_cfg:
        source_uconfig.write(user_cfg)

    init(_merged_uconfig.params)


#
# class SectionProxy:
#     def upd(self, _k, _v):
#         if _k in self._attrs:
#             compose = [self._attrs.get(_k), _v]
#             self._attrs.update({_k: compose})
#             setattr(self, _k, compose)
#             return
#         self._attrs.update({_k: _v})
#         setattr(self, _k, _v)
#
#     def __init__(self, items):
#         self._attrs = dict()
#         for k, v in items.items():
#             k = k.replace('-', '_')
#             if isinstance(v, dict):
#                 if '.' in k:
#                     k, subk = k.split('.', 1)
#                     if not (prox := getattr(self, k, None)):
#                         self.upd(k, prox := SectionProxy({}))
#                     prox.upd(subk, SectionProxy(v))
#                     continue
#                 self.upd(k, SectionProxy(v))
#                 continue
#             self.upd(k, v)
#
#     lvl = 0
#     def __repr__(self):
#         SectionProxy.lvl += 1
#         def iter():
#             if isinstance(self, SectionProxy):
#                 i = self._attrs
#             elif isinstance(self, dict):
#                 i = self
#             elif isinstance(self, list):
#                 i = {idx: val for idx, val in enumerate(self)}
#             else:
#                 yield repr(self)
#                 return
#             for k, v in i.items():
#                 yield ("  "*SectionProxy.lvl) + str(k) +  (':\n' if  isinstance(v,( SectionProxy, dict, list)) else ' = ')  +  SectionProxy.__repr__(v)
#         result = '\n'.join(iter())
#         SectionProxy.lvl -= 1
#         return result
