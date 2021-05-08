"""
a
    b
    c
        d
    e
f
    g
    h
        i
            j
"""

from typing import Optional


class CustomIter:
    def __init__(self, source: str):
        self.source: list[str] = list(source)

    def peek(self) -> Optional[str]:
        if len(self.source):
            return self.source[0]
        else:
            return None

    def __next__(self) -> str:
        if len(self.source):
            return self.source.pop(0)
        else:
            raise StopIteration()


source = CustomIter(__doc__)

level = 0
levels: list[int] = []
tokens: list[str] = []

while True:
    try:
        char = next(source)
        if char == "\n":
            lvl = 0
            
            while (source.peek() == " "):
                lvl += 1
                next(source)
            
            if lvl > level:
                tokens.append("indent")
                levels.append(lvl)
                level = lvl

            while lvl < level:
                tokens.append("dedent")
                levels.pop(-1)
                if len(levels):
                    level = levels[-1]
                else:
                    level = 0

                if level < lvl:
                    raise Exception("Invalid indentation level")
        else:
            tokens.append(char)
    except StopIteration:
        break


print(tokens)
