from collections.abc import Generator
from enum import IntEnum, auto
from string import ascii_letters, digits

__all__ = ["Kind", "Token", "tokenise"]


class Kind(IntEnum):
    IDENTIFIER = auto()
    INT_LITERAL = auto()

    KWD_IF = auto()
    KWD_ELSE = auto()

    COLON = auto()
    LPAR = auto()
    RPAR = auto()

    NEWLINE = auto()
    EOF = auto()
    ILLEGAL = auto()

    _INDENT = auto()
    _DEDENT = auto()


SYMBOLS = {":": Kind.COLON, "(": Kind.LPAR, ")": Kind.RPAR}
KEYWORDS = {"if": Kind.KWD_IF, "else": Kind.KWD_ELSE}


class Token:
    __slots__ = ("kind", "value", "line", "col")

    def __init__(self, kind: Kind, value: str | None, line: int, col: int) -> None:
        self.kind = kind
        self.value = value
        self.line = line
        self.col = col

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Token):
            return False

        return self.kind == value.kind and self.value == value.value and self.line == value.line and self.col == value.col

    def __str__(self) -> str:
        line = f"{self.line:02d}:{self.col:02d}\t{self.kind.name:11}"

        if self.value is None:
            return line

        line += f"\t{self.value}"

        return line

    def __repr__(self) -> str:
        return f"Token(kind={repr(self.kind)}, value={repr(self.value)}, line={self.line}, col={self.col})"


def tokenise(source: str) -> Generator[Token]:
    level = 0
    col = 1
    line = 1
    levels: list[int] = []

    position = 0

    while position < len(source):
        char = source[position]

        if char == "\n":
            yield Token(Kind.NEWLINE, "\\n", line, col)

            lvl = 0
            col = 1

            line += 1

            position += 1
            while position < len(source) and source[position] == " ":
                lvl += 1
                position += 1

            col += lvl

            if lvl > level:
                yield Token(Kind._INDENT, None, line, col-lvl)
                levels.append(lvl)

                level = lvl

            while lvl < level:
                yield Token(Kind._DEDENT, None, line, col)
                levels.pop()
                level = 0 if len(levels) == 0 else levels[-1]

                if level < lvl:
                    raise IndentationError(f"{line:02d}:{col:02d}")

            continue

        if char in ascii_letters:
            start = position

            position += 1
            while position < len(source) and source[position] in (ascii_letters + digits + "_"):
                position += 1

            kind = KEYWORDS.get(source[start:position], Kind.IDENTIFIER)

            yield Token(kind, source[start:position], line, col)
            col += (position - start)

        elif char in digits:
            start = position

            position += 1
            while position < len(source) and source[position] in (digits + "_"):
                position += 1

            yield Token(Kind.INT_LITERAL, source[start:position], line, col)
            col += (position - start)

        elif (symbol := SYMBOLS.get(char)) is not None:
            position += 1
            yield Token(symbol, char, line, col)
            col += 1

        elif char == " ":
            position += 1
            col += 1

        else:
            yield Token(Kind.ILLEGAL, char, line, col)
            position += 1
            col += 1

    yield Token(Kind.EOF, None, line, col)


if __name__ == "__main__":
    with open("examples/test1.txt") as f:
        for token in tokenise(f.read()):
            print(token)
