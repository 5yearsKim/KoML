from .abstracts import Tag, TemCandidate
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
        prev_item: Tag|None = None
        for item in self.child:
            if type(item) not in [Text, WildCard, PatBlank]:
                raise TagError(f'{type(item)} is not allowed in Pattern')
            if isinstance(prev_item, PatBlank) and isinstance(item, WildCard):
                raise TagError(f'Wildcard({item.val}) is not allowed to follow <blank>.. use pos/npos instead')
            
            prev_item = item

    def _decode_attr(self) -> None:
        pass



class TemItem(TemCandidate):
    def __init__(self, child: list[Tag]):
        self.child: list[Tag] = child
        super().__init__(attr={})

    def __repr__(self) -> str:
        return f'TemItem({self.child})'

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        pass
    

