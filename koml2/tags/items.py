from .abstracts import Node 
from .errors import TagError
from .leafs import *
from .nodes import *

class PatItem(Node):
    def __init__(self, child: list[Tag]):
        super().__init__(child, attr={})
    
    def __repr__(self) -> str:
        return f'PatItem({self.child})'
    
    def _check(self) -> None:
        for item in self.child:
            if type(item) not in [Text, WildCard, PatBlank]:
                raise TagError(f'{type(item)} is not allowed in Pattern')

    def _decode_attr(self) -> None:
        pass

class TemItem(Node):
    def __init__(self, child: list[Tag]):
        super().__init__(child, attr={})

    def __repr__(self) -> str:
        return f'TemItem({self.child})'

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        pass


    

