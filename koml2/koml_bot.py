import xml
from .parser import create_parser
from .brain import PatternMatcher, TemplateSolver

class KomlBot:
    def __init__(self) -> None:
        self.matcher: PatternMatcher = PatternMatcher()
        self.solver: TemplateSolver = TemplateSolver()

    def learn(self, files: list[str], save_path: str | None =None) -> None:
        for file in files:
            print(f'processing @{file}')
            parser = create_parser()
            handler = parser.getContentHandler() # type: ignore
            try:
                parser.parse(file) # type: ignore
            except xml.sax.SAXParseException as e:
                print(f'parse error: {e}')
                continue
            for case in handler.cases:
                self.matcher.add(case)
        
    def respond(self, question: str) -> str|None:
        matched = self.matcher.match(question)
        if matched:
            ans = self.solver.solve(matched)
            return ans
        else:
            return None
        
    def converse(self) -> None:
        while True:
            question = input('<< ')
            answer = self.respond(question)
            print(f'>> {answer}')