import xml
from .koml_parser import create_parser

class Kernel:
    def __init__(self):
        pass
    
    def learn(self, files):
        for file in files:
            parser = create_parser()
            handler = parser.getContentHandler()
            try:
                parser.parse(file)
            except xml.sax.SAXParseException as err:
                print('error:', err)
                continue

            for case in handler.cases:
                print(case)

