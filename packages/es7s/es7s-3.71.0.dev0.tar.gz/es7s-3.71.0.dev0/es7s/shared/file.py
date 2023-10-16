# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
import typing


from pytermor import ESCAPE_SEQ_REGEX


@dataclass
class IFile:
    inode: str
    perm: str
    hlinks: str
    owner: str
    group: str
    size: str
    timestamp: str
    name_prefix: str = field(init=False, default=" ")
    name: str
    name_extra: str
    cls_char: str = field(init=False, default=" ")

    is_invalid: bool = field(init=False, default=False)
    is_special: bool = field(init=False, default=False)

    is_dir: bool = field(init=False, default=False)
    is_exec: bool = field(init=False, default=False)
    is_link: bool = field(init=False, default=False)
    is_block: bool = field(init=False, default=False)
    is_char: bool = field(init=False, default=False)
    is_socket: bool = field(init=False, default=False)
    is_pipe: bool = field(init=False, default=False)

    def get_name_sanitized(self):
        return ESCAPE_SEQ_REGEX.sub("", self.name).strip("'\"")


class _AbstractMatch(metaclass=ABCMeta):
    def __init__(self, *vals: str):
        self.vals: list[re.Pattern] = [re.compile(v) for v in vals]

    @abstractmethod
    def matches(self, target_name: str) -> bool:
        raise NotImplementedError


class PartMatch(_AbstractMatch):
    def matches(self, target_name: str) -> bool:
        return any(v.search(target_name) for v in self.vals)


class FullMatch(_AbstractMatch):
    def matches(self, target_name: str) -> bool:
        return any(v.fullmatch(target_name) for v in self.vals)


class IFileIconRenderer(metaclass=ABCMeta):
    @abstractmethod
    def render(self, target: IFile) -> str:
        ...


class FileIconRendererFactory:
    @classmethod
    def make(cls, unicode: bool = False):
        if unicode:
            return FileIconRendererUnicode()
        return FileIconRendererNF()


class FileIconRendererUnicode(IFileIconRenderer):
    def render(self, target: IFile) -> str:
        if target.is_link:
            if target.is_dir:
                return "\uf482"  # 
            return "\uf481"  # 
        if target.is_dir:
            return "\uf115"  # 
        if "." in target.name:
            return "\uf15b"  # 
        return "\uf016"  # 


class FileIconRendererNF(IFileIconRenderer):
    FILE_REGEX_MAP = {
        PartMatch(r"\.(conf|ini)$"): "\ue615",  # 
        FullMatch(".editorconfig", "Makefile"): "\ue615",  # 
        FullMatch(".gitconfig"): "\uf1d3",  # 
        PartMatch(r"\.lock$"): "",  #          PartMatch(r"\.(diff|patch)$"): "\uf440",  # 
        PartMatch(r"\.(js)$"): "",  # 
        PartMatch(r"\.(py)$"): "\ue606",  # 
        PartMatch(r"\.(sh|zsh)$"): "\uf489",  # 
        PartMatch(r"\.(php)$"): "󰌟",  # 󰌟 |  
        PartMatch(r"\.(phar)$"): "",
        PartMatch(r"\.(txt)$"): "\uf15c",  # 
        PartMatch(r"\.(1)$"): "\uf02d",  # 
        PartMatch(r"\.(jar)$"): "\ue204",  # 
        PartMatch(r"\.(so)$"): "\ue624",  # 
        PartMatch(r"\.(pdf)$"): "\uf1c1",  # 
        PartMatch(r"\.(psd)$"): "\ue7b8",  # 
        PartMatch(r"\.(svg|png|jpe?g|gif|webp|xcf)$"): "\uf1c5",  #   | 
        PartMatch(r"\.(mp3)$"): "\uf001",  # 
        PartMatch(r"\.(mp4|mpg|flv|mkv|avi)$"): " ",  # 
        PartMatch(r"\.(css)$"): "\ue749",  # 
        PartMatch(r"\.(html?)$"): "\uf13b",  # 
        PartMatch(r"\.(zip)$"): "\uf410",  # 
        PartMatch(r"\.(log)$"): "\uf18d",  # 
        PartMatch(r"\.(xlsx?)$"): "\uf1c3",  # 
        PartMatch(r"\.(json)$"): "\ue60b",  # 
        PartMatch(r"\.(md)$"): "\uf48a",  # 
        FullMatch("Dockerfile"): "\uf308",  # 
    }
    DIR_REGEX_MAP = {
        FullMatch("config"): "\ue5fc",  # 
        FullMatch(".git"): "\ue5fb",  # 
        FullMatch(".github"): "\ue5fd",  # 
        FullMatch("Downloads"): "\uf498",  # 
        FullMatch("Pictures"): "󰉏",  # 󰉏
    }

    def __init__(self):  # @TODO вынести в конфиг, поверх прикрутить как cval
        self.RESOLVERS: typing.List[callable[[IFile], str | None]] = [
            FileIconRendererNF.get_icon_by_class,
            FileIconRendererNF.get_icon_by_name,
            FileIconRendererNF.get_icon_default,
        ]

    def render(self, target: IFile) -> str:
        for resolver in self.RESOLVERS:
            if result := resolver(target):
                return result
        raise RuntimeError(f'Unable to pick an icon for "{target.name}"')

    @classmethod
    def get_icon_by_class(cls, target: IFile) -> str | None:
        if target.is_link:
            if target.is_dir:
                return "\uf482"  # 
            return "\uf481"  # 
        if target.is_block:
            return "\ufc29"  # ﰩ
        if target.is_char:
            return "\ue601"  # 
        if target.is_socket:
            return "\uf6a7"  # 
        if target.is_pipe:
            return "\uf731"  # 
        return None

    @classmethod
    def get_icon_by_name(cls, target: IFile) -> str | None:
        mmap = cls.FILE_REGEX_MAP
        if target.is_dir:
            mmap = cls.DIR_REGEX_MAP

        for cond, result in mmap.items():
            if cond.matches(target.get_name_sanitized()):
                return result
        return None

    @classmethod
    def get_icon_default(self, target: IFile) -> str | None:
        # if target.name.startswith('.'):
        #     if target.is_dir:
        #         return "\uf413"  #   |  
        #     else:
        #         return "\uf016"  #     | 

        if target.is_dir:
            return "\uf413"  # 
        return "\uf016"  # 
