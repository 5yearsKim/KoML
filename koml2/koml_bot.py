import xml
from .parser import create_parser
from .pattern_matcher import PatternMatcher

class KomlBot:
    def __init__(self) -> None:
        self.matcher: PatternMatcher = PatternMatcher()

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
        print(self.matcher.patterns)
        
