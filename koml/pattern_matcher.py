from .tags import * 

class PatternMatcher:
    def __init__(self):
        self.cases = []
        self.case_map = {}

    def _convert_pattern(self, pattern):
        holder = []
        for item in pattern:
            if isinstance(item, Text):
                pass
            elif isinstance(item, WildCard):
                pass
            elif isinstance(item, PatStar):
                pass
            elif isinstance(item, Star):
                pass
        pass

    def add(self, case):
        pass 

