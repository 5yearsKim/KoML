from korean_rule_helper import KoreanRuleHelper, KoreanSentence
from ..tags import *
from .pattern_rule import PatternRule


class PatternMatcher:
    def __init__(self) -> None:
        self.ruler: KoreanRuleHelper = KoreanRuleHelper()
        self.patterns: list[PatternRule] = []

    def add(self, case: Case) -> None:
        pattern_rules = PatternRule.from_case(case)
        self.patterns.extend(pattern_rules)

    def match(self, sentence: str) -> PatternRule|None:
        ksent = KoreanSentence(sentence)
        holder: list[PatternRule] = []

        for prule in self.patterns:
            if prule.follow_cid:
                pass
            if prule.follow_rules:
                pass
            # check pattern
            is_match, args = self.ruler.match(ksent, prule.pattern)
            if is_match:
                assert len(prule.args) == len(args)
                for idx, arg in enumerate(args):
                    prule.args[idx].val = arg
                holder.append(prule)

        if holder:
            picked = max(holder, key=lambda x: x.priority_score)
            return picked
        else:
            return None
        

        
            
            

        

        




        

    
    

    