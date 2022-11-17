from __future__ import annotations


class BlankArg:
    def __init__(self, val: str|None=None, key: str|None=None) -> None:
        self.val: str|None = val 
        self.key: str|None = key 

    def __repr__(self) -> str:
        if self.key:
            return f'Arg({self.val}, key:{self.key})'
        else:
            return f'Arg({self.val})'