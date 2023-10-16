# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from typing import re

# fmt: off
__all__ = [
    "add",        "and_",      "basename",     "chr_",      "dirname",   "div",       "escape_if_branch", "exec_",
    "fmt",        "fnmatch",   "hexcolor",     "if_",       "literal",   "mod",       "mul",              "numcmp_eq",
    "numcmp_ge",  "numcmp_gt", "numcmp_le",    "numcmp_lt", "numcmp_ne", "or_",       "rematch",          "replace",
    "sessexists", "strcmp_eq", "strcmp_ge",    "strcmp_gt", "strcmp_le", "strcmp_lt", "strcmp_ne",        "strlen",
    "strlim",     "strlimr",   "strpad",       "strpadr",   "strptime",  "strwidth",  "sub",              "usrvar",
    "usrvarx",    "var",       "var_or_empty", "varx",      "winexists",
]
# fmt: on


def fmt(*attrs: str) -> str:
    """ define a style and apply it """
    return "#[" + " ".join(attrs) + "]"


def exec_(*cmd: str) -> str:
    """ run command in shell, display last line """
    return "#(" + " ".join(cmd) + ")"


def var(name: str) -> str:
    """ default tmux variable """
    return "#{" + name + "}"


def varx(name: str) -> str:
    """ default tmux variable expansion """
    return "#{E:" + name + "}"


def usrvar(name: str) -> str:
    """ user variable """
    return "#{@" + name + "}"


def usrvarx(name: str) -> str:
    """ user variable expansion """
    return "#{E:@" + name + "}"


def replace(src: str, dst: str, s: str, igncase=False) -> str:
    return "#{s/" + src + "/" + dst + "/" + ("i" if igncase else "") + ":" + s + "}"


def escape_if_branch(s: str) -> str:
    if s.startswith("#{?"):
        # if nested condition, escape "," and "}", except last symbol,
        # which is part of condition definition itself
        return re.sub("([,}])(?!$)", r"#\1", s)
    return s


def if_(expr: str, *, then_: str = None, else_: str = None) -> str:
    return "#{?" + expr + "," + (then_ or "") + "," + (else_ or "") + "}"


def var_or_empty(name: str) -> str:
    """ if var exists, print its value, otherwise empty string """
    return if_(var(name), then_=var(name))


# string comparators:

def _strcmp(op: str, s1: str, s2: str) -> str:
    return "#{" + op + ":" + s1 + "," + s2 + "}"


def strcmp_eq(s1: str, s2: str) -> str:
    return _strcmp("==", s1, s2)


def strcmp_ne(s1: str, s2: str) -> str:
    return _strcmp("!=", s1, s2)


def strcmp_lt(s1: str, s2: str) -> str:
    return _strcmp("<", s1, s2)


def strcmp_le(s1: str, s2: str) -> str:
    return _strcmp("<=", s1, s2)


def strcmp_gt(s1: str, s2: str) -> str:
    return _strcmp(">", s1, s2)


def strcmp_ge(s1: str, s2: str) -> str:
    return _strcmp(">=", s1, s2)


def strlim(s: str, *, n: str, sfx: str = None) -> str:
    """ limit the maximum string length, truncate right part """
    if sfx:
        return "#{=/" + n + "/" + sfx + ":" + s + "}"
    return "#{=" + n + ":" + s + "}"


def strlimr(s: str, *, n: str, pfx: str = None) -> str:
    """ limit the maximum string length from the right, truncate left part """
    return strlim(s, n="-" + n.lstrip("-"), sfx=pfx)


def strpad(s: str, n: str) -> str:
    """ append spaces to a string until its' length is `n` """
    return "#{p" + n + ":" + s + "}"


def strpadr(s: str, n: str) -> str:
    """ prepend string with spaces until its' length is `n` """
    return strpad(s, "-" + n.lstrip("-"))


def strlen(s: str) -> str:
    """ return string length (control characters are also counted) """
    return "#{n:" + s + "}"


def strwidth(s: str) -> str:
    """ return string width (number of visible characters in the output; ignores CC) """
    return "#{w:" + s + "}"


def strptime(s: str, short: bool = False, customf: str = None) -> str:
    """ expand date format using (the current system)? datetime """
    if customf:
        return "#{t:f/" + customf + ":" + s + "}"
    if short:
        return "#{t:p/" + s + "}"
    return "#{t:" + s + "}"


def and_(expr1: str, expr2: str) -> str:
    """ logical AND """
    return "#{&&:" + expr1 + "," + expr2 + "}"


def or_(expr1: str, expr2: str) -> str:
    """ logical OR """
    return "#{||:" + expr1 + "," + expr2 + "}"


def fnmatch(pattern: str, s: str) -> str:
    """ return 1 if `s` matches fnmatch `pattern`, 0 otherwise """
    return "#{m:" + pattern + "," + s + "}"


def rematch(regex: str, s: str, igncase=False) -> str:
    """ return 1 if `s` matches `regex`, 0 otherwise  """
    return "#{m/r" + ("i" if igncase else "") + ":" + regex + "," + s + "}"


# number basic operators and comparators:

def _numoper(op: str, num1: str, num2: str, floatp=0):
    pfx = "e|" + op
    if floatp:
        pfx += "|f|" + str(floatp)
    return "#{" + pfx + ":" + num1 + "," + num2 + "}"


def add(num1: str, num2: str, floatp=0) -> str:
    return _numoper("+", num1, num2, floatp)


def sub(num1: str, num2: str, floatp=0) -> str:
    return _numoper("-", num1, num2, floatp)


def mul(num1: str, num2: str, floatp=0) -> str:
    return _numoper("*", num1, num2, floatp)


def div(num1: str, num2: str, floatp=0) -> str:
    return _numoper("/", num1, num2, floatp)


def mod(num1: str, num2: str, floatp=0) -> str:
    return _numoper("m", num1, num2, floatp)


def numcmp_eq(num1: str, num2: str, floatp=0) -> str:
    return _numoper("==", num1, num2, floatp)


def numcmp_ne(num1: str, num2: str, floatp=0) -> str:
    return _numoper("!=", num1, num2, floatp)


def numcmp_lt(num1: str, num2: str, floatp=0) -> str:
    return _numoper("<", num1, num2, floatp)


def numcmp_le(num1: str, num2: str, floatp=0) -> str:
    return _numoper("<=", num1, num2, floatp)


def numcmp_gt(num1: str, num2: str, floatp=0) -> str:
    return _numoper(">", num1, num2, floatp)


def numcmp_ge(num1: str, num2: str, floatp=0) -> str:
    return _numoper(">=", num1, num2, floatp)


def chr_(code: str) -> str:
    """ replace hex code to unicode  """
    return "#{a:" + code + "}"


def hexcolor(name: str) -> str:
    """ replace color name with hex code """
    return "#{c:" + name + "}"


def basename(name: str) -> str:
    """ print path tp file with any preceding dir names removed """
    return "#{b:" + name + "}"


def dirname(name: str) -> str:
    """ print path to file'ss parent directory with any
        preceding dir names removed """
    return "#{d:" + name + "}"


def winexists(name: str) -> str:
    """ print window name if it exists, empty string otherwise """
    return "#{N/w:" + name + "}"


def sessexists(name: str) -> str:
    """ print session name it it exists, empty string otherwise """
    return "#{N/s:" + name + "}"


def literal(s: str) -> str:
    """ prinnt `s` as is, without postprocessors """
    return "#{l:" + s + "}"
