from .abstracts import Tag
from .errors import TagError
from .leafs import *
from .nodes import *

class PatItem(Tag):
    def __init__(self, child: list[Tag]):
        self.child: list[Tag] = child
        super().__init__(attr={})
    
    def __repr__(self) -> str:
        return f'PatItem({self.child})'
    
    def _check(self) -> None:
        for item in self.child:
            if type(item) not in [Text, WildCard, PatBlank]:
                raise TagError(f'{type(item)} is not allowed in Pattern')

    def _decode_attr(self) -> None:
        pass

class TemItem(Tag):
    def __init__(self, child: list[Tag]):
        self.child: list[Tag] = child
        super().__init__(attr={})

    def __repr__(self) -> str:
        return f'TemItem({self.child})'

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        pass


    

