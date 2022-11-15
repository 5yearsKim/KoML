import xml
from xml.sax.handler import ContentHandler
from enum import Enum
from .errors import KomlCheckError, FileLoc

class State(Enum):
    BEGIN = 0
    IN_CASE=1
    IN_FOLLOW=2
    IN_PATTERN=3
    IN_SUBPAT=4
    IN_TEMPLATE=5
    IN_SWITCH=6

class KomlHandler(ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.state :State = State.BEGIN

    @property
    def location(self) -> FileLoc:
        locator = self._locator # type: ignore
        line, column = locator.getLineNumber(), locator.getColumnNumber()
        return FileLoc(line, column)

    def startElement(self, tag: str, attributes: dict[str, str]) -> None:
        if self.state == State.BEGIN:
            allowed = ['koml', 'case']
        elif self.state == State.IN_CASE:
            allowed = ['follow', 'pattern', 'subpat', 'template']
        elif self.state == State.IN_FOLLOW:
            allowed = ['li']
        elif self.state == State.IN_PATTERN:
            allowed = ['star']
        elif self.state == State.IN_SUBPAT:
            allowed = ['li', 'star']
        elif self.state == State.IN_TEMPLATE:
            allowed = ['random', 'li', 'star', 'set', 'get', 'think', 'func', 'arg', 'switch']
        elif self.state == State.IN_SWITCH:
            allowed = ['pivot', 'scase', 'default', 'random', 'li', 'star', 'set', 'get' , 'think', 'func', 'arg']
        if tag not in allowed:
            raise KomlCheckError(f'tag {tag} is not allowed in this scope', self.location)

        # self._start_element(tag, attributes)

        if tag == 'case':
            self.state = State.IN_CASE 
        elif tag == 'follow':
            self.state = State.IN_FOLLOW
        elif tag == 'pattern':
            self.state =  State.IN_PATTERN
        elif tag == 'subpat':
            self.state = State.IN_SUBPAT
        elif tag == 'template':
            self.state = State.IN_TEMPLATE
        elif tag == 'switch':
            self.state = State.IN_SWITCH

    def endElement(self, tag: str) -> None:
        print('end tag', tag)