import xml
from .koml_parser import create_parser
from .pattern_matcher import PatternMatcher
from .context import Context

class Kernel:
    def __init__(self):
        self._brain = PatternMatcher()
    
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
                self._brain.add(case)
        self._brain.save('brain.pickle')
    
    def recall(self, path):
        self._brain.load(path)

    def respond(self, question:str, context:Context):
        answer = 'this is a test'
        context.push_history(question, answer)
        return answer, context

    def converse(self):
        context = Context()
        while True:
            question = input('<< ')
            answer, context = self.respond(question, context)
            print(context.history)
            print(f'>> {answer}')

    

    

