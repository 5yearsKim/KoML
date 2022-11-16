from .abstracts import Tag
from ..config import WILDCARDS
from .errors import TagError
from .utils import csv2list

class Text(Tag):
    def __init__(self, val: str) -> None:
        super().__init__(attr={})
        self.val: str = val

class WildCard(Tag):
    def __init__(self, val: str) -> None:
        super().__init__(attr={})
        self.val: str = val
        self._check()
    
    def _check(self) -> None:
        if not self.val:
            raise TagError('wildcard value not initialized')
        if self.val not in WILDCARDS:
            raise TagError(f'wildcard value {self.val} is not supported')

class PatBlank(Tag):
    def __init__(self, attr: dict[str, str]={}) -> None:
        super().__init__(attr=attr)
        self.idx: int = 0 
        self.key: str|None = None
        self.pos: list[str] = []
        self.npos: list[str] = []
        self._decode_attr()
        self._check()
    
    def _decode_attr(self):
        for k, v in self.attr:
            if k == 'key':
                self.key = v
            if k == 'idx':
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
        super().__init(attr=attr)
        self.idx: int = 0
        self.key : str|None = None
        self._check()
    
    def _decode_attr(self):
        for k, v in self.attr:
            if k == 'key':
                self.key = v
            if k == 'idx':
                self.idx = int(v)
            else:
                raise TagError(f'Blank attribute {k}={v} not supported')
    
    def _check(self) -> None:
        pass



    

# class WildCard(Tag):
    