from korean_rule_helper import KoreanRuleHelper
from ..tags import *
from .errors import PatternMatcherError
from .pattern_rule import PatternRule


class PatternMatcher:
    def __init__(self) -> None:
        self.ruler: KoreanRuleHelper = KoreanRuleHelper()
        self.patterns: list[PatternRule] = []

    def add(self, case: Case) -> None:
        pattern_rules = PatternRule.from_case(case)
        self.patterns.extend(pattern_rules)
    



        

    
    

    