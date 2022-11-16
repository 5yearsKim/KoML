from ..tags import *
from .errors import KomlCheckError, FileLoc
from .koml_state import KomlState

class RawTag:
    def __init__(self, tag: str, attr: dict[str, str]={}):
        self.tag: str = tag
        self.attr: dict[str, str] = attr

class Resolver:
    def __init__(self, locator=None):
        self.stack: list[str|RawTag|Tag] = []
        self.used: bool = False
        self.locator = locator

    @property
    def location(self) -> FileLoc:
        locator = self._locator # type: ignore
        line, column = locator.getLineNumber(), locator.getColumnNumber()
        return FileLoc(line, column)


    def _raw_tag_at(self, tag: str) -> int:
        for i in range(len(self.stack) -1, 0, -1):
            item = self.stack[i]
            if isinstance(item, RawTag) and item.tag == tag:
                return i
        return -1

    
    def push_tag(self, tag: str, attr: dict[str, str]={}):
        self.used = True
        raw_tag = RawTag(tag, attr)
        self.stack.append(raw_tag)
    
    def push_content(self, content: str):
        assert self.tag_idx is not None
        self.stack.append(content)
    
    def resolve(self, tag: str, state: KomlState=KomlState.BEGIN):
        tag_idx = self._raw_tag_at(tag)
        if tag_idx < 0:
            raise KomlCheckError(f'tag <{tag}> cannot be resolved')
        raw_tag = self.stack[tag_idx]
        raw_items = self.stack[tag_idx + 1:]

    
    def _resolve(self, tag: str, items: list[str, RawTag, Tag], state: KomlState) -> Tag:
        processed: list[Tag] = []
        for item in items:
            if isinstance(item, RawTag):
                raise KomlCheckError(f'tag <{tag}> found in wrong place')
        if tag == 'pattern':
            pass
        elif tag == 'template':
            pass
        elif tag == 'blank' and state in [KomlState.IN_CASE, KomlState.IN_SWITCH]:
            return Blank()







    