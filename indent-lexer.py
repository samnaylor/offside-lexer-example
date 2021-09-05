"""\
if 1:
    print(1)
else:
    print(0)
"""

from enum import Enum
from string import ascii_letters, digits
from typing import Optional
from dataclasses import dataclass


class Kind(Enum):
    IDENTIFIER = 0x00
    INT_LITERAL = 0x01

    IF_KWD = 0x10
    ELSE_KWD = 0x11

    COLON = 0x20
    LPAR = 0x21
    RPAR = 0x22

    INDENT = 0xFD
    DEDENT = 0xFE
    EOF = 0xFF

    def __str__(self) -> str:
        return self.name


@dataclass
class Token:
    kind: Kind
    value: Optional[str]
    lineno: int
    colno: int


def tokenise(code: str) -> list[Token]:
    level = 0
    colno = 1
    lineno = 1
    levels: list[int] = []
    tokens: list[Token] = []

    ptr = 0

    MISC = {
        ":": Kind.COLON,
        "(": Kind.LPAR,
        ")": Kind.RPAR,
    }

    while ptr < len(code):
        char = code[ptr]
        if char == "\n":
            lvl, colno = 0, 1
            lineno += 1

            while (ptr := ptr + 1) < len(code) and code[ptr] == " ":
                lvl += 1
                colno += 1

            if lvl > level:
                tokens.append(Token(Kind.INDENT, None, lineno, colno))
                levels.append(level := lvl)

            while lvl < level:
                tokens.append(Token(Kind.DEDENT, None, lineno, colno))
                levels.pop(-1)

                try:
                    level = levels[-1]
                except IndexError:
                    level = 0

                if level < lvl:
                    raise IndentationError()

            continue

        if char in ascii_letters:
            identifier = char
            start = colno

            while ((ptr := ptr + 1) < len(code)) and (code[ptr] in ascii_letters + "_"):
                identifier += code[ptr]
                colno += 1

            tokens.append(Token(Kind.IDENTIFIER, identifier, lineno, start))

        elif char in digits + ".":
            number = char
            start = colno

            while ((ptr := ptr + 1) < len(code)) and (code[ptr] in digits + "."):
                number += code[ptr]
                colno += 1

            tokens.append(Token(Kind.INT_LITERAL, number, lineno, start))

        elif char in ":()":
            tokens.append(Token(MISC[char], char, lineno, colno))
            ptr += 1
            colno += 1

        elif char == " ":
            ptr += 1
            colno += 1

        else:
            raise ValueError(f"Unknown character: {char}")

    tokens.append(Token(Kind.EOF, None, lineno, colno))

    return tokens


if __name__ == "__main__":
    for token in tokenise(__doc__):
        print(token)
