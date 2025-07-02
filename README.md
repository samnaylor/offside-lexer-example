# Indent sensitive lexer

An implementation of an indent sensitive for a Python-like grammar.

```python
if 0:
    print(1)
else:
    print(0)
```

Outputs

```bash
$ python tokenise.py

01:01   KWD_IF          if
01:04   INT_LITERAL     0
01:05   COLON           :
01:06   NEWLINE         \n
02:01   _INDENT
02:05   IDENTIFIER      print
02:10   LPAR            (
02:11   INT_LITERAL     1
02:12   RPAR            )
02:13   NEWLINE         \n
03:01   _DEDENT
03:01   KWD_ELSE        else
03:05   COLON           :
03:06   NEWLINE         \n
04:01   _INDENT
04:05   IDENTIFIER      print
04:10   LPAR            (
04:11   INT_LITERAL     0
04:12   RPAR            )
04:13   NEWLINE         \n
05:01   _DEDENT
05:01   EOF
```
