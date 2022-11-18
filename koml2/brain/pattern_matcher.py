from korean_rule_helper import KoreanRuleHelper, KoreanSentence, Rule
from ..tags import *
from ..context import Context
from .pattern_rule import PatternRule


class PatternMatcher:
    def __init__(self) -> None:
        self.ruler: KoreanRuleHelper = KoreanRuleHelper()
        self.patterns: list[PatternRule] = []

    def add(self, case: Case) -> None:
        pattern_rules = PatternRule.from_case(case)
        self.patterns.extend(pattern_rules)

    def match(self, sentence: str, context: Context) -> PatternRule|None:
        ksent = KoreanSentence(sentence)
        holder: list[PatternRule] = []

        for prule in self.patterns:
            # follow_cid : if prev_chat not matching cid -> give up case
            if prule.follow_cid:
                if not context.prev_chat:
                    continue
                if context.prev_chat.cid not in prule.follow_cid:
                    continue
            # follow rules : if not matching the follow -> give up case
            if prule.follow_rules:
                def match_follow(ksent: KoreanSentence, follow_rules: list[list[Rule]]) -> bool:
                    for rule in follow_rules:
                        is_match, _ = self.ruler.match(ksent, rule)
                        if is_match:
                            return True
                    return False
                if not context.prev_chat:
                    continue
                prev_ans = KoreanSentence(context.prev_chat.answer)
                is_match = match_follow(prev_ans, prule.follow_rules)
                if not is_match:
                    continue
            # check pattern
            is_match, args = self.ruler.match(ksent, prule.pattern)
            if is_match:
                assert len(prule.args) == len(args)
                for prule_arg, arg in zip(prule.args, args):
                    assert isinstance(arg, str)
                    prule_arg.val = arg
                holder.append(prule)

        if holder:
            picked = max(holder, key=lambda x: x.priority_score)
            return picked
        else:
            return None
        

        
            
            

        

        




        

    
    

    