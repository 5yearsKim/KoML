from .abstracts import Node
from .leafs import *
from .errors import TagError

class Set(Node):
    def __init__(self, child: list[Tag], attr: dict[str, str]={}) -> None:
        self.key: str = '' 
        super().__init__(child, attr=attr)
    
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

class Think(Node):
    def __init__(self, child: list[Tag], attr: dict[str, str]={}) -> None:
        super().__init__(child, attr=attr)

    def _decode_attr(self) -> None:
        for k, v in self.attr.items():
            raise TagError(f'Think attribute {k}={v} not supported')
    
    def _check(self) -> None:
        pass
    
    
