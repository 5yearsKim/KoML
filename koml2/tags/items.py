from .abstracts import Tag

class PatItem(Tag):
    def __init__(self, child: list[Tag]):
        self.child: list[Tag] = child
        super().__init__(attr={})
    
    def __repr__(self) -> str:
        return f'PatItem({self.child})'
    
    def _check(self) -> None:
        pass
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


    

