import xml
from koml.koml_parser import KomlHandler

if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = KomlHandler()
    parser.setContentHandler( Handler )

    parser.parse("koml.xml")
    handler = parser.getContentHandler()

    cases = handler.cases
    for case in cases:
        print(case)
        print('------------')
