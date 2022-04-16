from aiml.AimlParser import create_parser

parser = create_parser()

parser.parse('default.aiml')

handler = parser.getContentHandler()
