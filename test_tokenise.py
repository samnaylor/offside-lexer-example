from tokenise import Kind, Token, tokenise


class Case:
    __slots__ = ("source", "expected")

    def __init__(self, source: str, expected: list[Token]) -> None:
        self.source = source
        self.expected = expected


# TODO: Test errorenous cases


tests = [
    Case("", [Token(Kind.EOF, None, 1, 1)]),
    Case("if 0:\n    print(1)\nelse:\n    print(0)\n", [
        Token(Kind.KWD_IF, "if", 1, 1),
        Token(Kind.INT_LITERAL, "0", 1, 4),
        Token(Kind.COLON, ":", 1, 5),
        Token(Kind.NEWLINE, "\\n", 1, 6),
        Token(Kind._INDENT, None, 2, 1),
        Token(Kind.IDENTIFIER, "print", 2, 5),
        Token(Kind.LPAR, "(", 2, 10),
        Token(Kind.INT_LITERAL, "1", 2, 11),
        Token(Kind.RPAR, ")", 2, 12),
        Token(Kind.NEWLINE, "\\n", 2, 13),
        Token(Kind._DEDENT, None, 3, 1),
        Token(Kind.KWD_ELSE, "else", 3, 1),
        Token(Kind.COLON, ":", 3, 5),
        Token(Kind.NEWLINE, "\\n", 3, 6),
        Token(Kind._INDENT, None, 4, 1),
        Token(Kind.IDENTIFIER, "print", 4, 5),
        Token(Kind.LPAR, "(", 4, 10),
        Token(Kind.INT_LITERAL, "0", 4, 11),
        Token(Kind.RPAR, ")", 4, 12),
        Token(Kind.NEWLINE, "\\n", 4, 13),
        Token(Kind._DEDENT, None, 5, 1),
        Token(Kind.EOF, None, 5, 1),
    ])
]


def test_tokenise() -> None:
    for i, test in enumerate(tests):
        assert list(tokenise(test.source)) == test.expected, f"Case {i} has failed"
