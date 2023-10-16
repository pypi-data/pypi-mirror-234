import re
from collections import deque

from es7s.cli._base import CliCommand
from es7s.cli._decorators import cli_command, catch_and_log_and_exit

raw = r""" 
${-}:⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤                         ┌───────┬──────┬─────┐ ┌───────┬───────┬─────┐
${-} ⣿░░░░░░░░░░░░░░░░░░░░░░░░░⣿_                        │ S7C1T │ ACS6 │ ... │ │ DECSC │ DECRC │ ... │
${-} ⣿░░░░░░=ANSI=ESCAPE ░░░░░░⣿_                        └───────┴──────┴─────┘ └───────┴───────┴─────┘
${-} ⣿░░=SEQUENCES=BREAKDOWN ░░⣿_                                  ^                       ^      
${-} ⣿░░░░░░░░░░░░░░░░░░░░░░░░░⣿_                                  ╵                       ╵      
${-} ⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛_                        ┌─────────┴──────────┐  ┌─────────┴──────────┐
${-}                                                     │@nF^class           │  │@Fp^class           │
${-}                                                     │(ANSI/ISO switching)│  │(private use)       │
   ^c┌─────────────────────────────────┐c$               │                    │  │                    │
  ^c╭│   _ASCII _C0 _CONTROL _CODES    │╮c$              │        1b [20-2f]..│  │        1b [30-3f]..│
  ^c│└─────────────────────────────────┘│c$             ╔══════════════════════════════════════════════╗
  ^c│ 00 NUL │ 08  BS │ 11 DC1 │ 1a SUB │c$          ╭─────╮                                           ║
  ^c│────────│ 09  HT │ 12 DC2 │ 1b=ESC ├─────────>c$│_ESC │      _GENERIC _ESCAPE _SEQUENCES          ║
  ^c│ 01 SOH │ 0a  LF │ 13 DC3 │ 1c  FS │c$          ╰─────╯                                           ║
  ^c│ 02 STX │ 0b  VT │ 14 DC4 │ 1d  GS │c$             ╚══════════════════════════════════════════════╝
  ^c│ 03 ETX │ 0c  FF │ 15 NAK │ 1e  RS │c$              │@Fe^class           │  │@Fs^class           │
  ^c│ 04 EOT │ 0d  CR │ 16 SYN │ 1f  US │c$              │(C1 set)            │  │(independent func.) │
  ^c│ 05 ENQ │ 0e  SO │ 17 ETB │ 20  SP │c$              │                    │  │                    │
  ^c│ 06 ACK │ 0f  SI │ 18 CAN │────────│c$              │        1b [40-5f]..│  │        1b [60-7e]..│
  ^c│ 07 BEL │ 10 DLE │ 19  EM │ 7f DEL │c$              └┬┬┬──────────────┬──┘  └─────────────────┬──┘
  ^c╰───────────────────────────────────╯c$               ╷╵╷              V                       V
${-}                                                      ╷╵╷  ┌─────┬─────┬────┬─────┬─────┐   ┌─────┐    
  ^C╭───────────────────────────────────╮C$               ╷╵╷  │ CUP │ QCP │ ED │ DSR │ ... │   │ RID │
  ^C│ 80 PAD │ 88 HTS │ 90 DCS │ 98 SOS │C$               ╷╵╷  └─────┴─────┴────┴─────┴─────┘   ├─────┤
  ^C│ 81 HOP │ 89 HTJ │ 91 PU1 │ 99 SGC │C$               ╷╵╷  ┌───────────────┬────────────┐   │ ··· │     
  ^C│ 82 BPH │ 8a VTS │ 92 PU2 │ 9a SCI │C$               ╷╵╷ ` │`! Control       │? Select     │   ├─────┤ 
  ^C│ 83 NBH │ 8b PLD │ 93 STS │ 9b+CSI ├──────────────C$`─╵┴╴->│`! Sequence      │? Graphic    │   │ ··· │ 
  ^C│ 84 IND │ 8c PLU │ 94 CCH │ 9c +ST ├───────┐C$       ╵╵  ` │`! Introducer    │? Rendetion  │   └─────┘ 
  ^C│ 85 NEL │ 8d  RI │ 95  MW │ 9d+OSC ├───┐   │C$       ╵╵   │               └────────────│   
  ^C│ 86 SSA │ 8e SS2 │ 96 SPA │ 9e  PM │C$  '│   │'      ╵╵   └──────────1b─5b─xx───|ESC[*|┘    
  ^C│ 87 ESA │ 8f SS3 │ 97 EPA │ 9f APC │C$   ^C│C$   ^C└───────C$╵┴`╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴┐`    
  ^C│┌─────────────────────────────────┐│C$  '│          '╵    ┌────────────────┐'╷' ┌────────────────┐
  ^C╰│   _ASCII _C1 _CONTROL _CODES    │╯C$  '│          '╵    `│`! Operating      │ ╷  `│`! Sequence       │
   ^C└─────────────────────────────────┘C$   '└───────────└`╴╴╴>│`! System         │ `└ >│`! Terminator     │'
                                                           `│`! Command        │    │                │
${-}".-------------------."                                    │       1b 5d(xx)│    │          1b 5c │
${-}"|"_G0 "SET  | 21-7e |"                                    └─────────|ESC]*|┘    └──────────|ESC\|┘
${-} |-----------|-------|    
${-}'|'_G1 'SET  | a0-ff |'
${-}'`-------------------´'
${-}  
${-} &#######################  
${-}@TODO(:=swap^Fe^and^Fs``?  
"""

import random


def genc(l, c0):
    r = ""
    while len(r) < l:
        r += c(c0)
    return r[:l]


q = deque()


def c(c0):
    global q
    byterange = (0, 0x20)
    if not c0:
        byterange = (0x80, 0x9F)
    while len(q) < 10:
        el = "".join("{:02x}".format(random.randint(*byterange)) for _ in range(0, random.randint(1, 4)))
        q.append(el)
    return q.popleft()


def head(m):
    label = m.group(2)
    hl = m.group(3)

    match m.group(1):
        case "_":
            return f" \x1b[97;1m{m.group(2)}\x1b[22;39m" + (m.group(5) or "")
        case "=":
            return (
                f" \x1b[1;{'36' if 'ESC' in m.group(2) else '97':s}m{m.group(2)}\x1b[48;5;16m{m.group(5) or ''}\x1b[m"
            )
        case "+":
            return f" \x1b[1;34m{m.group(2)}\x1b[22;48;5;16m{m.group(5) or ''}\x1b[m"
        case "^":
            return f" \x1b[3m{hl}{m.group(4)}\x1b[23m" + (m.group(5) or "")
        case "!" | "?":
            return (
                f"\x1b[7;{'34' if m.group(1) == '!' else '97'};1m{hl}\x1b[;3;27m"
                + (m.group(4) or "")
                + (m.group(5) or "▋")
                + "\x1b[m"
            )
        case "&":
            return "\x1b[4m" + (m.group(1) or "").replace("&", " ") + (m.group(4) or "").replace("#", " ") + "\x1b[m"
        case "@":
            return f" \x1b[1;33m{label}\x1b[m"
    return m.group(0)


def apply(s, *fn):
    for f in fn:
        s = f(s)
    return s

@cli_command(
    name=__file__,
    cls=CliCommand,
    short_help="ansi escape sequences classification",
)
@catch_and_log_and_exit
def invoker():
    """
    // Early experiment (one of) in templating and functional programming (note the one and only print()).
    """
    print(
        apply(
            raw,
            # lambda s: re.sub(
            #    r"(^ )(░*)(\w+)?(░*?)?( {5,})",
            #    "\\1\x1b[36;2m\\2\x1b[96;22;4;1m\\3\x1b[36;22;2;24m\\4\x1b[22;96m\\5\x1b[m",
            #    s,
            # ),
            lambda s: re.sub(r"\$\{.*?\}", "", s),
            lambda s: re.sub(
                r"(?:(1b)|(5[bcd]|6d)|(?<![g-zG-Z[-])([0-9a-f]{2}(?=[  +])))(?=[^;m])",
                "\x1b[36m\\1\x1b[32m\\2\x1b[90m\\3\x1b[39m",
                s,
            ),
            lambda s: re.sub(
                r"(\[)([0-9a-f]{2})(-)([0-9a-f]{2})(\])",
                "\x1b[32m\x1b[2m\\1\x1b[22m\\2\x1b[2m\\3\x1b[22m\\4\x1b[2m\\5\x1b[22;39m",
                s,
            ),
            lambda s: re.sub(
                r"\([\w.-:]+\)|\([\w.-:]+|[\w.-:]+\)",
                lambda m: "\x1b[2m" + m.group().replace("(", " ").replace(")", " ") + "\x1b[22m",
                s,
            ),
            lambda s: re.sub(r"([_^@+=&!?])(( ?[a-zA-Z#])([a-zA-Z0-9/!-#]+))(\.? )?", lambda m: head(m), s),
            lambda s: re.sub(
                "([⠛⣤⣿▄]+)|([⠁⠈⡀⢀])|(_)",
                lambda m: "\x1b[48;5;16m"
                          + (m.group(2) or "")
                          + "\x1b[49;22;97m"
                          + (m.group(1) or "")
                          + "\x1b[48;5;16m"
                          + (len(m.group(3) or "") * " ")
                          + "\x1b[27;39;49m",
                s,
            ),
            lambda s: re.sub("(⠛)(⠛+)", "\\1\x1b[48;5;16m\\2\x1b[49m", s),
            lambda s: re.sub("([▓▒░]+)", "\x1b[48;5;16;34;2m\\1\x1b[22;94m", s),
            lambda s: re.sub(r":((?:\x1b\[[0-9;]*m)+)(⣤)", " \x1b[36m\\2\x1b[49;39m\\1", s),
            lambda s: "\n".join(
                (
                    "".join(
                        (
                            (f"\x1b[{31 if '^c' in l else 35:d};48;5;16m" if i % 2 == 1 else "")
                            + re.sub(
                                r"(\s+)|([A-Z]*[0-4]?(?=!+))|([─│╭╮╰╯┬┴╴╶├>╵╷┐ └┘]+)|([│└┯┘┐┤┌─]+)",
                                lambda q: (
                                              (
                                                      f"\x1b[38;5;{52 if '^c' in l else 53:d};2m"
                                                      + genc(len(q.group(1)), "^c" in l)
                                                      + f"\x1b[22;38;5;{52 if '^c' in l else 53:d}m"
                                              )
                                              if q.group(1)
                                              else ""
                                          )
                                          + "\x1b[97m"
                                          + (q.group(2) or "")
                                          + "\x1b[39m"
                                          + f"\x1b[{31 if '^c' in l else 35:d}m"
                                          + (q.group(3) or "")
                                          + f"\x1b[{31 if '^c' in l else 35:d}m"
                                          + (q.group(4) or "")
                                          + "\x1b[39m",
                                p,
                            )
                            + "\x1b[49m"
                            if (i % 2 == 1)
                            else p + ""
                        )
                        for i, p in enumerate(re.split(r"\^c|c\$", l, flags=re.IGNORECASE))
                    )
                    + "\x1b[39;49;22m".replace("^c", "  ").replace("c$", "").replace("^C", "  ").replace("C$", "")
                    if ("^c" in l or "^C" in l) and ("c$" in l or "C$" in l)
                    else l
                )
                for l in s.splitlines(False)
            ),
            lambda s: re.sub(
                r"( ?ESC)(?!APE|\x1b\[24)([^\s*─|\x1b0-9;]*)([0-9;]*)(m)?(\*)?( )?",
                "\x1b[48;5;16;36m\\1\x1b[32m\\2\x1b[93m\\5\\6\x1b[39m\\3\x1b[32m\\4\x1b[49;39;24m",
                s,
            ),
            lambda s: re.sub(r"(\")(.*?)(\")", "\x1b[31m \\2 \x1b[39;22m", s),
            lambda s: re.sub(r"(')(.*?)(')", "\x1b[35m \\2 \x1b[39;22m", s),
            lambda s: re.sub(
                r"(`)(.*?)(`)",
                lambda m: ("" if not m.group(2) == ("│") else "")
                          + "".join(
                    ("\x1b[35m" if (not p.isspace() and i % 4 == 1) else "")
                    + p
                    + ("\x1b[39m" if (not p.isspace() and i % 4 == 1) else "")
                    for i, p in enumerate(
                        re.split(r"(\S)", m.group(2).replace("│", ("┃" if m.group(2) == ("│") else "┃")))
                    )
                )
                          + (" " if not m.group(2).endswith("│") else "")
                          + "\x1b[39;22m",
                s,
            ),
            lambda s: re.sub(r"(│)(\s*)([A-Z0-9]+)(\s*)(?=│)", "\\1\x1b[1;7m\\2\\3\\4\x1b[22;27m", s),
        )
    )
