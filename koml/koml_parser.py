from xml.sax.xmlreader import Locator
import sys
import xml.sax
import xml.sax.handler
import xml

class KomlParserError(Exception):
    pass

class KomlHandler(xml.sax.ContentHandler):
    def __init__(self):
        pass

    def startElement(self, tag, attributes):
        print(tag, attributes.getNames())

    def endElement(self, tag):
        print(tag)

    def characters(self, content):
        print(content)

