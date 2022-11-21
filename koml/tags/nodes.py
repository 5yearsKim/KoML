from __future__ import annotations
from .abstracts import Tag, TemCandidate, SwitchCandidate
from .leafs import *
from .errors import TagError

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
        self.child: TemCandidate = child
        super().__init__(attr=attr)

    def __repr__(self) -> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 
    
    def _check(self) -> None:
        if not self.child:
            raise TagError(f'Ri child should\'n be empty')

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

    
class Random(TemCandidate):
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


class Pivot( SwitchCandidate):
    def __init__(self, child: list[Tag], attr: dict[str, str]={}) -> None:
        self.child: list[Tag] = child
        super().__init__(attr=attr)

    def __repr__(self)-> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Random attribute {k}={v} not supported')

class Scase(SwitchCandidate):
    def __init__(self, child: TemCandidate, attr: dict[str, str]={}) -> None:
        self.pivot: str = ''
        self.child: TemCandidate = child
        super().__init__(attr=attr)

    def __repr__(self)-> str:
        att_str = ','.join([f'{k}: {v}' for k, v in self.attr.items()])
        return f'{self.__class__.__name__}({self.child} {att_str})' 

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        if 'pivot' not in self.attr:
            raise TagError('pivot is required for <si>')
        for k, v in self.attr.items():
            if k == 'pivot':
                self.pivot = v.strip()
            else:
                raise TagError(f'Si attribute {k}={v} not supported')

class Default(Scase):
    def __init__(self, child: TemCandidate, attr: dict[str, str]={}) -> None:
        super().__init__(child, attr=attr)
    
    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Default attribute {k}={v} not supported')



class Switch(TemCandidate):
    def __init__(self, pivot: Pivot, scases: list[Scase], default: Default, attr: dict[str, str]={}):
        self.pivot: Pivot = pivot
        self.scases: list[Scase] = scases
        self.default: Default = default
        super().__init__(attr=attr)

    def __repr__(self)-> str:
        return f'Switch \n pivot: {self.pivot}\n si: {self.scases}\n default: {self.default}'

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Default attribute {k}={v} not supported')

    def _check(self) -> None:
        pass

    def pick(self, pivot: str) -> Scase:
        for scase in self.scases:
            if scase.pivot == pivot:
                return scase
        return self.default

    @staticmethod 
    def from_children(children: list[Tag]) -> Switch:
        for x in children:
            if not isinstance(x, SwitchCandidate):
                raise TagError(f'tag {x} is not supported inside Switch')
        pivot_list = [x for x in children if isinstance(x, Pivot)]
        if len(pivot_list) != 1:
            raise TagError('Switch should have one pivot')
        default_list = [x for x in children if isinstance(x, Default)]
        if len(default_list) != 1:
            raise TagError('Switch should have one default')
        si_list = [x for x in children if isinstance(x, Scase)]
        return Switch(pivot_list[0], si_list, default_list[0])


