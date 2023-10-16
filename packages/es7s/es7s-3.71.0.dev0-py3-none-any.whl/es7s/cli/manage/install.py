# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import importlib.resources
import os
import shutil
import tempfile
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import ClassVar, cast

import pytermor as pt
from click import pass_context

from es7s.shared import ProgressBar, get_user_data_dir
from es7s.shared import RESOURCE_PACKAGE, USER_ES7S_BIN_DIR
from es7s.shared import (
    Styles,
    get_logger,
    get_stdout,
    run_detached,
    with_progress_bar,
)
from ...commons.pt_ import format_attrs
from es7s.shared import SubprocessExitCodeError
from ..exec_.switch_wspace import invoker as invoke_switch_wspace
from .rebuild import invoker as invoke_rebuild
from .._base import Context
from .._decorators import catch_and_log_and_exit, cli_command, cli_option
from ... import APP_NAME


@cli_command(__file__)
@cli_option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Don't actually do anything, just pretend to.",
)
@cli_option(
    "-s",
    "--symlinks",
    is_flag=True,
    default=False,
    help="Make symlinks to core files instead of copying them. "
    "Useful for es7s development, otherwise unnecessary.",
)
@pass_context
@catch_and_log_and_exit
@with_progress_bar
class invoker:
    """Install es7s system."""

    pbar: ClassVar[ProgressBar]

    def __init__(
        self,
        pbar: ProgressBar,
        ctx: Context,
        dry_run: bool,
        symlinks: bool,
        **kwargs,
    ):
        self._stages: OrderedDict[callable, str] = OrderedDict(
            {
                self._run_prepare: "Preparing",
                self._run_copy_core: "Copying core files",
                self._run_inject_bashrc: "Injecting into shell",
                self._run_inject_gitconfig: "Injecting git config",
                CopyDataRunner(dry_run, symlinks)._run: "Copying data",
                CopyBinariesRunner(dry_run, symlinks)._run: "Copying executables",
                self._run_install_with_apt: "Installing apt packages",
                self._run_install_with_pip: "Installing pip packages",
                self._run_install_x11: "Installing X11 packages",
                self._run_dload_install: "Downloading packages directly",
                TmuxBuildInstallRunner(dry_run, symlinks)._run: "Building tmux",
                self._run_build_install_less: "Building less",
                self._run_build_install_htop: "Building htop",
                self._run_build_install_bat: "Building bat",
                self._run_install_es7s_exts: "Installing es7s extensions",
                self._run_install_daemon: "Installing es7s/daemon",
                self._run_install_shocks_service: "Installing es7s/shocks",
                self._run_setup_cron: "Setting up cron",
                self._run_make_switch_wspace: "Installing switch-wspace",
                self._run_manage_rebuild: "Reconstructing resources",
            }
        )
        self._stages_results: OrderedDict[callable, tuple[bool, str]] = OrderedDict()
        self._current_stage: str | None = None
        invoker.pbar = pbar
        self._dry_run = dry_run
        self._symlinks = symlinks
        self._run(ctx)

    def _run(self, ctx: Context):
        invoker.pbar.init_tasks(len(self._stages))
        for stage_fn, stage_desc in self._stages.items():
            self._current_stage = stage_fn.__qualname__.split(".")[1].lstrip("_")
            self._log(f"Starting stage: {self._current_stage}")
            invoker.pbar.next_task(stage_desc)
            try:
                result_msg = stage_fn(ctx)
            except StageFailedError as e:
                self._echo_failure(stage_desc, str(e))
                self._stages_results.update({stage_fn: (False, str(e))})
                continue
            except Exception as e:
                raise RuntimeError(self._current_stage + " failed") from e
            else:
                self._echo_success(stage_desc, result_msg)
                self._stages_results.update({stage_fn: (True, result_msg)})

    def _run_prepare(self, ctx: Context):
        # install docker
        # sudo xargs -n1 <<< "docker syslog adm sudo" adduser $(id -nu)
        # ln -s /usr/bin/python3 ~/.local/bin/python
        pass

    def _run_copy_core(self, ctx: Context):
        # install i -cp -v
        # git+ssh://git@github.com/delameter/pytermor@2.1.0-dev9
        pass

    def _run_inject_bashrc(self, ctx: Context):
        pass

    def _run_inject_gitconfig(self, ctx: Context):
        pass

    def _run_install_with_apt(self, ctx: Context):
        pass

    def _run_install_with_pip(self, ctx: Context):
        pass

    def _run_install_x11(self, ctx: Context):
        pass

    def _run_dload_install(self, ctx: Context):
        # ginstall exa
        # ginstall bat
        pass

    def _run_build_install_tmux(self, ctx: Context) -> str:
        # sudo apt install automake autotools-dev bison build-essential byacc gcc iproute2 iputils-ping libevent-dev ncurses-dev pkg-config -y
        logger = get_logger()
        invoker.pbar.init_steps(5)

        try:
            temp_dir_path = self._make_temp_dir("tmux")

            invoker.pbar.next_step(step_label="Cloning primary repo")
            self._clone_git_repo("ssh://git@github.com/dl-forks/tmux", temp_dir_path)

            invoker.pbar.next_step(step_label="Building from sources")
            self._run_assert_zero_code(["sh", "autogen.sh"], cwd=temp_dir_path)
            self._run_assert_zero_code(["./configure && make"], cwd=temp_dir_path)
            self._run_assert_zero_code(["sudo make install"], cwd=temp_dir_path)
            self._remove_file_or_dir(temp_dir_path)

            # ln -s `pwd`/tmux ~/bin/es7s/tmux

            tpm_dir_path = os.path.expanduser("~/.tmux/plugins/tpm")
            self._make_dir(tpm_dir_path)

            invoker.pbar.next_step(step_label="Cloning tpm repo")
            self._clone_git_repo("ssh://git@github.com:tmux-plugins/tpm", tpm_dir_path)

            invoker.pbar.next_step(step_label="Installing tpm")
            self._run_assert_zero_code(
                ["tmux", "run-shell", "./bindings/install_plugins"], cwd=tpm_dir_path
            )

        except Exception as e:
            logger.exception(e)
            raise StageFailedError("Unable to continue")
        return "donee"

    def _run_build_install_less(self, ctx: Context):
        # install less deps
        # build_less
        pass

    def _run_build_install_htop(self, ctx: Context):
        pass

    def _run_build_install_bat(self, ctx: Context):
        pass

    def _run_build_install_qcachegrind(self, ctx: Context):
        ...  # @temp on demand?

    def _run_build_install_bashdb(self, ctx: Context):
        ...  # @temp on demand?

    def _run_install_es7s_exts(self, ctx: Context):
        # install i -i -v

        # colors
        # fonts?
        # > pipx install kolombos
        # leo
        # > pipx install macedon
        # watson
        # nalog
        pass

    def _run_install_daemon(self, ctx: Context):
        # copy es7s.service to /etc/systemd/system
        # replace USER placeholders
        # enable es7s, reload systemd
        pass

    def _run_install_shocks_service(self, ctx: Context):
        # copy es7s-shocks.service to /etc/systemd/system
        # replace USER placeholders
        # enable shocks, reload systemd
        pass

    def _run_setup_cron(self, ctx: Context):
        pass

    def _run_make_switch_wspace(self, ctx: Context):
        ctx.invoke(invoke_switch_wspace, shell=True)

    def _run_manage_rebuild(self, ctx: Context):
        ctx.invoke(invoke_rebuild, shell=True)

    def _log(self, msg: str):
        prefix = ""
        if self._dry_run:
            prefix += "DRY-RUN|"
        prefix += self._current_stage
        get_logger().info(f"[{prefix}] {msg}")

    def _echo_failure(self, stage_desc: str, msg: str):
        self._log(msg)

        stdout = get_stdout()
        text = pt.Text(
            pt.Fragment(" × ", Styles.MSG_FAILURE_LABEL),
            pt.Fragment(" " + stage_desc, Styles.MSG_FAILURE),
        )
        if msg:
            text += pt.Fragment(f": {msg}", Styles.MSG_FAILURE_DETAILS)
        stdout.echo_rendered(text)

    def _echo_success(self, stage_desc: str, msg: str = None):
        if msg:
            if self._dry_run:
                msg += " [NOT REALLY]"
            self._log(msg)

        stdout = get_stdout()
        text = pt.Text(
            pt.Fragment(" ⏺ ", Styles.MSG_SUCCESS_LABEL) + " " + stage_desc + "...",
        )
        if not msg:
            msg = "done"
        if msg:
            text += stdout.render(" " + msg.strip(), Styles.MSG_SUCCESS)

        stdout.echo_rendered(text)


class AbstractRunner(metaclass=ABCMeta):
    def __init__(self, dry_run: bool, symlinks: bool, **kwargs):
        self._dry_run = dry_run
        self._symlinks = symlinks

    @abstractmethod
    def _run(self, ctx: Context):
        ...

    # -------------------------------------------------
    # Execution

    def _run_assert_zero_code(self, args: any, cwd: str = None):
        self._log_io("Running", format_attrs(args))
        if self._dry_run:
            return True

        exit_code = run_detached(args, cwd=cwd)
        if exit_code != 0:
            raise SubprocessExitCodeError(exit_code, args)

    # -------------------------------------------------
    # Git

    def _clone_git_repo(self, remote_url: str, path: str) -> bool:
        self._log_io("Cloning", path, remote_url)
        if self._dry_run:
            return True

        run_detached(["git", "clone", remote_url, "--progress"], cwd=path)
        return True

    # -------------------------------------------------
    # Filesystem

    def _make_dir(self, user_path: str | Path) -> bool:
        self._log_io("Creating", user_path)
        if self._dry_run:
            return True

        try:
            os.makedirs(user_path)
            self._log_io("Created", user_path)
        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to create dir: %s", user_path)
            return False

        return os.path.exists(user_path)

    def _remake_dir(self, user_path: Path) -> bool:
        if user_path.is_dir():
            self._remove_file_or_dir(user_path)
        return self._make_dir(user_path)

    def _make_temp_dir(self, name: str) -> str:
        now = datetime.now().timestamp()
        return tempfile.mkdtemp(str(now), f"es7s-core.install.{name}")

    def _remove_file_or_dir(self, user_path: str | Path) -> bool:
        self._log_io("Removing", user_path)
        if self._dry_run:
            return True

        try:
            if user_path.is_file() or user_path.is_symlink():
                os.unlink(user_path)
                self._log_io("Removed", user_path)

            elif os.path.isdir(user_path):
                shutil.rmtree(user_path)
                self._log_io("Removed", user_path)

            else:
                self._log_io("Not found", user_path)

        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to remove dir: %s", user_path)
            return False

        return not user_path.exists()

    def _copy_or_symlink(self, dist_path: Path, user_path: Path, overwrite=True) -> bool:
        action = "Linking" if self._symlinks else "Copying"

        self._log_io(action, user_path, dist_path)
        if self._dry_run:
            return True

        if dist_path.is_dir():
            self._remake_dir(user_path)
            results = [
                self._copy_or_symlink(item.absolute(), user_path / item.name, overwrite)
                for item in dist_path.iterdir()
            ]
            return all(results)

        if user_path.exists() or user_path.is_symlink():  # may be broken link
            if not overwrite:
                raise FileExistsError(user_path)
            self._remove_file_or_dir(user_path)

        try:
            if self._symlinks:
                os.symlink(dist_path, user_path)
                self._log_io("Linked", user_path, dist_path)
            else:
                shutil.copy(dist_path, user_path)
                self._log_io("Copied", user_path, dist_path)

        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to copy file: %s -> %s", dist_path, user_path)
            return False

        return True

    # -------------------------------------------------
    # Output

    def _log(self, msg: str):
        prefix = ""
        if self._dry_run:
            prefix += "DRY-RUN|"
        get_logger().info(f"[{prefix}] {msg}")

    def _log_io(self, action: str, target: str | Path, source: str | Path = None):
        prefix = ""
        target = str(target)
        source = str(source)
        path = f'"{target}"'
        if source:
            path = f'"{source}" -> {path}'
        self._log(f"{prefix}{action+':':<9s} {path}")


class CopyDataRunner(AbstractRunner):
    def _run(self, ctx: Context) -> str:
        count = 0

        if not self._remake_dir(get_user_data_dir()):
            raise StageFailedError("Unable to start")

        dist_dir = importlib.resources.files(RESOURCE_PACKAGE)
        dist_files: list[Path] = [
            *(f for f in dist_dir.iterdir() if f.is_file()),
            dist_dir / "conf.d",
            dist_dir / "xdotool",
        ]
        total = len(dist_files)
        invoker.pbar.init_steps(steps_amount=total)

        for idx, dist_relpath in enumerate(dist_files):
            invoker.pbar.next_step(step_label=str(dist_relpath))

            dist_abspath = dist_relpath.absolute()

            user_relpath = dist_relpath
            if user_relpath.is_dir():  # to keep es7s.conf.d
                user_relpath = str(user_relpath).removesuffix('.d')
            user_abspath = get_user_data_dir() / os.path.basename(user_relpath)

            if self._copy_or_symlink(dist_abspath, user_abspath):
                count += 1

        if count != total:
            raise StageFailedError(f"Copied {count} out of {total} data files")
        return f"({count}/{total} files)"


class CopyBinariesRunner(AbstractRunner):
    def _run(self, ctx: Context):
        count = 0

        if not self._remake_dir(USER_ES7S_BIN_DIR):
            raise StageFailedError("Unable to start")

        dist_dir = importlib.resources.files(f"{APP_NAME}.cli.exec_")
        dist_files: list[Path] = [
            cast(Path, f)
            for f in dist_dir.iterdir() if f.name.endswith(".sh")
        ]
        total = len(dist_files)
        invoker.pbar.init_steps(steps_amount=total)

        for idx, dist_relpath in enumerate(dist_files):
            invoker.pbar.next_step(step_label=str(dist_relpath))

            dist_abspath = dist_relpath.absolute()
            user_abspath = USER_ES7S_BIN_DIR / os.path.basename(dist_relpath).removesuffix(".sh")

            if self._copy_or_symlink(dist_abspath, user_abspath):
                count += 1

        if count != total:
            raise StageFailedError(f"Installed {count} out of {total} executables")
        return f"({count} files)"


class TmuxBuildInstallRunner(AbstractRunner):
    def _run(self, ctx: Context) -> str:
        # sudo apt install automake autotools-dev bison build-essential byacc gcc iproute2 iputils-ping libevent-dev ncurses-dev pkg-config -y
        logger = get_logger()
        idx, total = 0, 5
        invoker.pbar.init_steps(steps_amount=total)

        try:
            temp_dir_path = self._make_temp_dir("tmux")

            invoker.pbar.next_step(step_label="Cloning primary repo")
            self._clone_git_repo("ssh://git@github.com/dl-forks/tmux", temp_dir_path)

            invoker.pbar.next_step(step_label="Building from sources")
            self._run_assert_zero_code(["sh", "autogen.sh"], cwd=temp_dir_path)
            self._run_assert_zero_code(["./configure && make"], cwd=temp_dir_path)
            self._run_assert_zero_code(["sudo make install"], cwd=temp_dir_path)
            self._remove_file_or_dir(temp_dir_path)

            # ln -s `pwd`/tmux ~/bin/es7s/tmux

            tpm_dir_path = os.path.expanduser("~/.tmux/plugins/tpm")
            self._make_dir(tpm_dir_path)

            invoker.pbar.next_step(step_label="Cloning tpm repo")
            self._clone_git_repo("ssh://git@github.com:tmux-plugins/tpm", tpm_dir_path)

            invoker.pbar.next_step(step_label="Installing tpm")
            self._run_assert_zero_code(
                ["tmux", "run-shell", "./bindings/install_plugins"], cwd=tpm_dir_path
            )

        except Exception as e:
            logger.exception(e)
            raise StageFailedError("Unable to continue")
        return "donee"


class StageFailedError(RuntimeError):
    pass
