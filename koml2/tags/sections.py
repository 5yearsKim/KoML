from .abstracts import Tag
from .items import PatItem, TemItem

# class Follow(Tag):
#     def __init__(self, child: ):
#         super().__init__(attr=)

class Pattern(Tag):
    def __init__(self, children: list[PatItem], attr: dict[str, str]={}) -> None:
        super().__init__(attr=attr)
        self.children: list[PatItem] = children


class Template(Tag):
    def __init__(self, child: TemItem, attr: dict[str, str]={}) -> None :
        super().__init__(attr=attr)
        self.child: TemItem = child
