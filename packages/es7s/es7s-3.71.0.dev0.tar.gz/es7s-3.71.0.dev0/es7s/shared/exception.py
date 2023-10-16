# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing


class ExecutableNotFoundError(RuntimeError):
    def __init__(self, path: str) -> None:
        self._path = path
        super().__init__(f"Executable not found: '{path}'")


class ArgCountError(Exception):
    def __init__(self, actual: int, *expected: int) -> None:
        expected_str = ", ".join(str(e) for e in expected)
        msg = f"Invalid arguments amount, expected one of: ({expected_str}), got: {actual}"
        super().__init__(msg)


class DataCollectionError(Exception):
    def __init__(self, msg: str = "Data collection failed"):
        self._msg = msg

    @property
    def msg(self) -> str:
        return self._msg


class SubprocessExitCodeError(RuntimeError):
    def __init__(self, exit_code: int, args: typing.Iterable) -> None:
        from es7s.commons import format_attrs
        super().__init__(f"Subprocess terminated with exit code {exit_code}. Command was {format_attrs(args)}")
