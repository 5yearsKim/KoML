import xml
from korean_rule_helper import KoreanSentence
from .parser import create_parser
from .brain import PatternMatcher, TemplateSolver
from .context import Context
from .customize import CustomBag

class KomlBot:
    def __init__(self, custom_bag:CustomBag|None=None, space_sensitive: bool=False, debug: bool=False) -> None:
        self.custom_bag: CustomBag = custom_bag or CustomBag()
        self.matcher: PatternMatcher = PatternMatcher(self.custom_bag, space_sensitive=space_sensitive)
        self.solver: TemplateSolver = TemplateSolver(self.custom_bag)
        self.debug: bool = debug

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
        if save_path:
            self.matcher.save(save_path)
            print(f'saved to {save_path}!')
    
    def load(self, load_path: str) -> None:
        self.matcher.load(load_path)
        
    def respond(self, question: str, context: Context) -> str|None:
        question = question.strip()
        if self.debug:
            ksent = KoreanSentence(question)
            print(ksent.tags)
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
