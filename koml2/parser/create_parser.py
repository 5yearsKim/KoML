import xml
from xml.sax.xmlreader import XMLReader
from .koml_handler import KomlHandler

def create_parser() -> XMLReader:
    parser = xml.sax.make_parser()
    handler = KomlHandler()
    parser.setContentHandler(handler) # type: ignore
    return parser