import xml
from .parser import create_parser
from .brain import PatternMatcher, TemplateSolver
from .context import Context
from .customize import CustomBag

class KomlBot:
    def __init__(self, custom_bag:CustomBag|None=None) -> None:
        self.matcher: PatternMatcher = PatternMatcher()
        self.custom_bag: CustomBag = custom_bag or CustomBag()
        self.solver: TemplateSolver = TemplateSolver(self.custom_bag)

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
        
    def respond(self, question: str, context: Context) -> str|None:
        matched = self.matcher.match(question, context)
        if matched:
            ans = self.solver.solve(matched, context)
            context.push_history(question, ans, matched.cid)
            return ans
        else:
            return None
        
    def converse(self) -> None:
        context = Context()
        while True:
            question = input('<< ')
            answer = self.respond(question, context)
            print(f'>> {answer}')