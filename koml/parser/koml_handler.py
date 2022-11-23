from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import Locator
from ..tags import Case
from .errors import KomlCheckError, FileLoc
from .koml_state import KomlState
from .resolver import Resolver

class KomlHandler(ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.state :KomlState = KomlState.BEGIN
        def get_loc() -> FileLoc:
            return self.location
        self.resolver :Resolver = Resolver(get_loc) #type: ignore
        self.cases: list[Case] = []

    @property
    def location(self) -> FileLoc:
        locator: Locator = self._locator # type: ignore
        line, column = locator.getLineNumber(), locator.getColumnNumber() #type: ignore
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
            allowed = ['blank', 'set', 'get', 'think', 'func', 'random', 'ri', 'arg', 'switch', 'switch', 'pivot', 'scase', 'default']
        # elif self.state == KomlState.IN_SWITCH:
        #     allowed = ['pivot', 'scase', 'default', 'random', 'li', 'blank', 'set', 'get' , 'think', 'func', 'arg']
        if tag not in allowed:
            raise KomlCheckError(f'tag {tag} is not allowed in {self.state} state', self.location)

        # logic
        if tag == 'koml':
            pass
        else:
            self.resolver.push_tag(tag, attr=attributes)

        if tag == 'case':
            self.state = KomlState.IN_CASE 
        elif tag == 'follow':
            self.state = KomlState.IN_FOLLOW
        elif tag == 'pattern':
            self.state =  KomlState.IN_PATTERN
        elif tag == 'template':
            self.state = KomlState.IN_TEMPLATE

    def endElement(self, tag: str) -> None:
        if tag == 'koml':
            pass
        elif tag == 'case':
            self.resolver.resolve(tag, self.state)
            case = self.resolver.finalize()
            self.cases.append(case)
        else:
            self.resolver.resolve(tag, self.state)
        
        if tag == 'case':
            self.state = KomlState.BEGIN
        elif tag == 'follow':
            self.state = KomlState.IN_CASE
        elif tag == 'pattern':
            self.state = KomlState.IN_CASE
        elif tag == 'template':
            self.state = KomlState.IN_CASE

    def characters(self, content: str) -> None:
        if content == '\n' or content.isspace():
            return
        self.resolver.push_content(content, self.state)
    
        
        
