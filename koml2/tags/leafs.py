from .abstracts import Tag
from ..config import WILDCARDS
from .errors import TagError
from .utils import csv2list

class Text(Tag):
    def __init__(self, val: str) -> None:
        self.val: str = val
        super().__init__(attr={})
    
    def __repr__(self) -> str:
        return f'T({self.val})'

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        pass


class WildCard(Tag):
    def __init__(self, val: str) -> None:
        self.val: str = val
        super().__init__(attr={})
    
    def __repr__(self) -> str:
        return f'WC({self.val})'

    def _check(self) -> None:
        if not self.val:
            raise TagError('wildcard value not initialized')
        if self.val not in WILDCARDS:
            raise TagError(f'wildcard value {self.val} is not supported')

    def _decode_attr(self) -> None:
        pass

class PatBlank(Tag):
    def __init__(self, attr: dict[str, str]={}) -> None:
        self.idx: int = 0 
        self.key: str|None = None
        self.pos: list[str] = []
        self.npos: list[str] = []
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'PatBlank({att_str})'

    
    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'key':
                self.key = v
            elif k == 'idx':
                self.idx = int(v)
            elif k == 'pos':
                self.pos = csv2list(v)
            elif k == 'npos':
                self.npos = csv2list(v)
            else:
                raise TagError(f'Blank attribute {k}={v} not supported')
    
    def _check(self) -> None:
        if self.pos and self.npos:
            raise TagError('Pattern <Blank> cannot have pos and npos together!')

class Blank(Tag):
    def __init__(self, attr: dict[str, str]) -> None:
        self.idx: int = 0
        self.key : str|None = None
        super().__init__(attr=attr)


    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'Blank({att_str})'
    
    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'key':
                self.key = v
            elif k == 'idx':
                self.idx = int(v)
            else:
                raise TagError(f'Blank attribute {k}={v} not supported')
    
    def _check(self) -> None:
        pass

class Get(Tag):
    def __init__(self, attr: dict[str, str]) -> None:
        self.key: str = ''
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'Get({att_str})'

    def _check(self) -> None:
        if not self.key:
            raise TagError(f'key attribute for <Get> is required')
    
    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'key':
                self.key = v
            else:
                raise TagError(f'Set attribute {k}={v} not supported')