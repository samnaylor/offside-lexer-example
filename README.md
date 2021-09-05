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
Token(kind=IF, value='if', lineno=2, colno=1)
Token(kind=INT_LITERAL, value='0', lineno=2, colno=3)
Token(kind=COLON, value=':', lineno=2, colno=3)
Token(kind=INDENT, value=None, lineno=3, colno=5)
Token(kind=IDENTIFIER, value='print', lineno=3, colno=5)
Token(kind=LPAR, value='(', lineno=3, colno=9)
Token(kind=INT_LITERAL, value='1', lineno=3, colno=10)
Token(kind=RPAR, value=')', lineno=3, colno=10)
Token(kind=DEDENT, value=None, lineno=4, colno=1)
Token(kind=ELSE, value='else', lineno=4, colno=1)
Token(kind=COLON, value=':', lineno=4, colno=4)
Token(kind=INDENT, value=None, lineno=5, colno=5)
Token(kind=IDENTIFIER, value='print', lineno=5, colno=5)
Token(kind=LPAR, value='(', lineno=5, colno=9)
Token(kind=INT_LITERAL, value='0', lineno=5, colno=10)
Token(kind=RPAR, value=')', lineno=5, colno=10)
Token(kind=DEDENT, value=None, lineno=6, colno=1)
Token(kind=EOF, value=None, lineno=6, colno=1)
```
