import xml
from xml.sax.handler import ContentHandler
from .errors import KomlCheckError, FileLoc
from .koml_state import KomlState
from .resolver import Resolver

class KomlHandler(ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.state :KomlState = KomlState.BEGIN


    @property
    def location(self) -> FileLoc:
        locator = self._locator # type: ignore
        line, column = locator.getLineNumber(), locator.getColumnNumber()
        return FileLoc(line, column)

    def startElement(self, tag: str, attributes: dict[str, str]) -> None:
        if self.state == KomlState.BEGIN:
            allowed = ['koml', 'case']
        elif self.state == KomlState.IN_CASE:
            allowed = ['follow', 'pattern', 'template']
        elif self.state == KomlState.IN_FOLLOW:
            allowed = ['li']
        elif self.state == KomlState.IN_PATTERN:
            allowed = ['li', 'blank']
        elif self.state == KomlState.IN_TEMPLATE:
            allowed = ['random', 'li', 'blank', 'set', 'get', 'think', 'func', 'arg', 'switch']
        elif self.state == KomlState.IN_SWITCH:
            allowed = ['pivot', 'scase', 'default', 'random', 'li', 'blank', 'set', 'get' , 'think', 'func', 'arg']
        if tag not in allowed:
            raise KomlCheckError(f'tag {tag} is not allowed in this scope', self.location)

        # self._start_element(tag, attributes)

        if tag == 'case':
            self.state = KomlState.IN_CASE 
        elif tag == 'follow':
            self.state = KomlState.IN_FOLLOW
        elif tag == 'pattern':
            self.state =  KomlState.IN_PATTERN
        elif tag == 'template':
            self.state = KomlState.IN_TEMPLATE
        elif tag == 'switch':
            self.state = KomlState.IN_SWITCH

    def endElement(self, tag: str) -> None:
        print('end tag', tag)