from __future__ import annotations
from typing import TYPE_CHECKING
from .abstracts import Tag
from .items import TemItem
if TYPE_CHECKING:
    from .nodes import Random

class TemCandidate(Tag):
    def __init__(self, child: TemItem|Random):
        self.child : TemItem|Random = child
        super().__init__()

    def __repr__(self) -> str:
        return f'{self.child}' 

    def _check(self) -> None:
        pass

    def _decode_attr(self) -> None:
        pass