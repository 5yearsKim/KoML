from __future__ import annotations
from typing import TYPE_CHECKING
from .abstracts import Tag
from .leafs import *
from .errors import TagError
if TYPE_CHECKING:
    from .tem_candidate import TemCandidate

class Set(Tag):
    def __init__(self, child: list[Tag], attr: dict[str, str]={}) -> None:
        self.key: str = '' 
        self.child: list[Tag] = child
        super().__init__(attr=attr)


    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 
    
    def _check(self) -> None:
        if not self.key:
            raise TagError(f'key attribute for <Set> is required')
        for item in self.child:
            if type(item) not in [Text, WildCard, Blank]:
                raise TagError(f'{item} is not supported for child of Set')
    
    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'key':
                self.key = v
            else:
                raise TagError(f'Set attribute {k}={v} not supported')

class Think(Tag):
    def __init__(self, child: list[Tag], attr: dict[str, str]={}) -> None:
        self.child: list[Tag] = child
        super().__init__(attr=attr)


    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Think attribute {k}={v} not supported')
    
    def _check(self) -> None:
        pass
    
class Arg(Tag):
    def __init__(self, child: list[Tag], attr: dict[str, str]={}) -> None:
        self.child: list[Tag] = child
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Func attribute {k}={v} not supported')
    
    def _check(self) -> None:
        if not self.child:
            raise TagError(f'Arg child should\'n be empty')

class Func(Tag):
    def __init__(self, child: list[Arg], attr: dict[str, str]={}) -> None:
        self.child: list[Arg] = child
        self.name: str =''
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'name':
                self.name = v
            else:
                raise TagError(f'Func attribute {k}={v} not supported')
    
    def _check(self) -> None:
        if not self.name:
            raise TagError(f'Func must have attribute name')
        if any([not isinstance(x, Arg) for x in self.child]):
            raise TagError(f'Func can only have Arg Tag for child')


class Ri(Tag):
    def __init__(self, child: TemCandidate, attr: dict[str, str] = {}) -> None:
        self.weight: float = 1.
        self.child:TemCandidate = child
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 
    
    def _check(self) -> None:
        # if not isinstance(self.child, TemCandidate):
        #     raise TagError(f'child of Ri shoud be TemCandidate, not {self.child}')
        pass

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            if k == 'weight':
                try:
                    self.weight = float(v)
                    if (self.weight < 0):
                        raise ValueError('')
                except ValueError:
                    raise TagError(f'Ri attribute weight={v} should be positive number')
            else:
                raise TagError(f'Ri attribute {k}={v} not supported')

    
class Random(Tag):
    def __init__(self, child: list[Ri], attr: dict[str, str]={}) -> None:
        self.child: list[Ri] = child
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 

    def _check(self) -> None:
        if any(not isinstance(x, Ri) for x in self.child):
            raise TagError(f'all children in Random should be <ri>')

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Random attribute {k}={v} not supported')


