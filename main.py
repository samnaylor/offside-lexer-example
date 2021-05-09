"""
if 0:
    print(1)
else:
    print(0)
"""

import string

from enum import IntEnum
from typing import Optional, Iterator, Iterable
from itertools import chain
from dataclasses import dataclass


class Kind(IntEnum):
    IDENTIFIER = 0
    INT_LITERAL = 1
    IF = 2
    ELSE = 3
    COLON = 4
    LPAR = 5
    RPAR = 6
    EOF = 7
    INDENT = 8
    DEDENT = 9

    def __repr__(self) -> str:
        return self.name


@dataclass
class Token:
    kind: Kind
    value: Optional[str]
    lineno: int
    colno: int


class PeekableStringIter(Iterator):
    def __init__(self, i: Iterable[str]):
        self.it: Iterator[str] = iter(i)

    def peek(self) -> Optional[str]:
        try:
            val = next(self.it)
            self.it = chain([val], self.it)
            return val
        except StopIteration:
            return None

    def __next__(self) -> str:
        return next(self.it)


def tokenise(code: str) -> list[Token]:
    it = PeekableStringIter(code)

    symbols = {
        "if": Kind.IF,
        "else": Kind.ELSE,
    }

    level = 0
    levels: list[int] = []
    tokens: list[Token] = []

    lineno, colno = 1, 1

    while True:
        try:
            char = next(it)
            if char == "\n":
                lvl = 0
                lineno += 1
                colno = 1

                while it.peek() == " ":
                    lvl += 1
                    colno += 1
                    next(it)

                if lvl > level:
                    tokens.append(Token(
                        Kind.INDENT,
                        None,
                        lineno,
                        colno
                    ))
                    levels.append(lvl)
                    level = lvl

                while lvl < level:
                    tokens.append(Token(
                        Kind.DEDENT,
                        None,
                        lineno,
                        colno
                    ))
                    levels.pop(-1)

                    if len(levels):
                        level = levels[-1]
                    else:
                        level = 0

                    if level < lvl:
                        raise Exception("Invalid indentation level")
            else:
                if char in string.ascii_letters:
                    identifier = char
                    start = colno
                    while (char := it.peek()) is not None and char in string.ascii_letters + "_":
                        identifier += char
                        colno += 1
                        next(it)

                    tokens.append(Token(
                        symbols.get(identifier, Kind.IDENTIFIER),
                        identifier,
                        lineno,
                        start
                    ))

                elif char in string.digits:
                    number = char
                    start = colno
                    while (char := it.peek()) is not None and char in string.digits:
                        number += char
                        colno += 1
                        next(it)

                    tokens.append(Token(
                        Kind.INT_LITERAL,
                        number,
                        lineno,
                        start
                    ))

                elif char == ":":
                    tokens.append(Token(
                        Kind.COLON,
                        ":",
                        lineno,
                        colno
                    ))
                    colno += 1

                elif char == "(":
                    tokens.append(Token(
                        Kind.LPAR,
                        "(",
                        lineno,
                        colno
                    ))
                    colno += 1

                elif char == ")":
                    tokens.append(Token(
                        Kind.RPAR,
                        ")",
                        lineno,
                        colno
                    ))
                    colno += 1

                elif char == " ":
                    colno += 1

                else:
                    raise Exception(
                        f"Unrecognised character '{char}' @ {lineno}:{colno}"
                    )
        except StopIteration:
            break

    tokens.append(Token(Kind.EOF, None, lineno, colno))
    return tokens


if __name__ == "__main__":
    for token in tokenise(__doc__):
        print(token)
