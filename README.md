# Indent sensitive lexer

An implementation of an indent sensitive for a Python-like grammar.

```python
if 0:
    print(1)
else:
    print(0)
```

Becomes

```python
Token(kind=<Kind.IDENTIFIER: 0>, value='if', lineno=1, colno=1)
Token(kind=<Kind.INT_LITERAL: 1>, value='1', lineno=1, colno=3)
Token(kind=<Kind.COLON: 32>, value=':', lineno=1, colno=3)
Token(kind=<Kind.INDENT: 253>, value=None, lineno=2, colno=5)
Token(kind=<Kind.IDENTIFIER: 0>, value='print', lineno=2, colno=5)
Token(kind=<Kind.LPAR: 33>, value='(', lineno=2, colno=9)
Token(kind=<Kind.INT_LITERAL: 1>, value='1', lineno=2, colno=10)
Token(kind=<Kind.RPAR: 34>, value=')', lineno=2, colno=10)
Token(kind=<Kind.DEDENT: 254>, value=None, lineno=3, colno=1)
Token(kind=<Kind.IDENTIFIER: 0>, value='else', lineno=3, colno=1)
Token(kind=<Kind.COLON: 32>, value=':', lineno=3, colno=4)
Token(kind=<Kind.INDENT: 253>, value=None, lineno=4, colno=5)
Token(kind=<Kind.IDENTIFIER: 0>, value='print', lineno=4, colno=5)
Token(kind=<Kind.LPAR: 33>, value='(', lineno=4, colno=9)
Token(kind=<Kind.INT_LITERAL: 1>, value='0', lineno=4, colno=10)
Token(kind=<Kind.RPAR: 34>, value=')', lineno=4, colno=10)
Token(kind=<Kind.DEDENT: 254>, value=None, lineno=5, colno=1)
Token(kind=<Kind.EOF: 255>, value=None, lineno=5, colno=1)
```
