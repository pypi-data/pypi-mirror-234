# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import json
import logging
import os
from os import getcwd
from pathlib import Path
from subprocess import CalledProcessError

from pytermor import get_qname

from es7s.shared.sub import run_subprocess
from es7s.shared.path import GIT_LSTAT_DIR, GIT_PATH


class GitRepo:
    def __init__(self, path: str | Path = getcwd()):
        self._logger = logging.getLogger(__package__)

        if isinstance(path, Path):
            if not path.is_dir():
                path = path.parent

        self._path: Path = self._get_toplevel_dir(path)
        if not self._path:
            raise ValueError(f"Not a git repo: '{path}'")
        self._logger.debug(f"{self}: Initializing git repo model: '{self.path!s}'")

        self._head_commit_hash: str = self.get_head_commit_hash()
        if not self._head_commit_hash:
            raise ValueError(f"Repo has no HEAD: '{path}'")

    @property
    def path(self) -> Path:
        return self._path

    def _get_toplevel_dir(self, path: str | Path) -> Path | None:
        args = [
            GIT_PATH,
            "rev-parse",
            "--show-toplevel",
        ]
        cp = run_subprocess(*args, check=False, cwd=path)
        if cp.returncode == 0:
            return Path(cp.stdout).resolve()
        return None

    def _invoke_git(self, *args):
        return run_subprocess(GIT_PATH, *args, cwd=str(self._path))

    def get_remote_names(self) -> list[str]:
        cp = self._invoke_git("remote")
        return [*map(str.strip, cp.stdout.splitlines())]

    def get_primary_remote_name(self) -> str | None:
        def _get():
            remote_names = self.get_remote_names()
            if not remote_names:
                return None
            if "origin" in remote_names:
                return "origin"
            return remote_names.pop()

        prim_remote_name = _get()
        self._logger.debug(f"{self}: Primary remote name: '{prim_remote_name}'")
        return prim_remote_name

    def get_repo_name(self) -> str | None:
        if not (prim_remote_name := self.get_primary_remote_name()):
            return None

        cp = self._invoke_git("config", "--get", f"remote.{prim_remote_name}.url")
        try:
            remote_url = (cp.stdout or " ").splitlines().pop(0).removesuffix(".git")
        except IndexError:
            return None

        self._logger.debug(f"{self}: Primary remote URL (raw): '{remote_url}'")
        if remote_url.startswith("git@github"):
            return remote_url.partition(":")[2]
        return '/'.join(remote_url.rsplit("/", 2)[1:])

    def get_head_commit_hash(self) -> str|None:
        self._logger.debug(f"{self}: Determining HEAD commit hash")
        try:
            cp = self._invoke_git("log", "-1", "--format=%H")
        except CalledProcessError as e:
            return None
        try:
            return (cp.stdout or " ").splitlines().pop(0).strip()
        except IndexError:
            return None

    def update_cached_stats(self, data: dict, commit_hash: str = None) -> None:
        commit_hash = commit_hash or self._head_commit_hash
        filepath = self._get_stats_filepath(commit_hash)
        if not os.path.exists(dirname := os.path.dirname(filepath)):
            os.makedirs(dirname)
        self._logger.debug(f"{self}: Writing cached stats to: '{filepath}'")
        with open(filepath, 'wt') as f:
            json.dump(data, f)

    def get_cached_stats(self, commit_hash: str = None) -> dict|None:
        commit_hash = commit_hash or self._head_commit_hash
        filepath = self._get_stats_filepath(commit_hash)
        if not os.path.isfile(filepath):
            self._logger.debug(f"{self}: No cached stats for '{commit_hash}'")
            return None
        self._logger.debug(f"{self}: Reading cached stats from: '{filepath}'")
        with open(filepath, 'rt') as f:
            return json.load(f)

    def _get_stats_filepath(self, commit_hash: str) -> str:
        return os.path.join(self.path, '.git', GIT_LSTAT_DIR, commit_hash)

    def __repr__(self):
        return f"{get_qname(self)}[{self.path.name}]"
