from korean_rule_helper import KoreanRuleHelper, KoreanSentence, Rule
import pickle
from ..tags import *
from ..context import Context
from ..customize import CustomBag
from .pattern_rule import PatternRule


class PatternMatcher:
    def __init__(self, custom_bag: CustomBag, space_sensitive: bool=True) -> None:
        self.ruler: KoreanRuleHelper = KoreanRuleHelper(space_sensitive=space_sensitive)
        self.patterns: list[PatternRule] = []
        self.custom_bag: CustomBag = custom_bag 

    def add(self, case: Case) -> None:
        pattern_rules = PatternRule.from_case(case)
        self.patterns.extend(pattern_rules)

    def match(self, sentence: str, context: Context) -> PatternRule|None:
        ppcsr = self.custom_bag.preprocessor
        prev_bot_ans : KoreanSentence| None = None
        if context.prev_chat:
            prev_bot_ans = KoreanSentence(context.prev_chat.answer)
            # no preprocessing for prev bot answer
            # prev_bot_ans = ppcsr.process(prev_bot_ans)
        ksent = KoreanSentence(sentence)
        ksent = ppcsr.process(ksent)
        
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
                def match_follow(prev_sent: KoreanSentence, follow_rules: list[list[Rule]]) -> bool:
                    for rule in follow_rules:
                        is_match, _ = self.ruler.match(prev_sent, rule)
                        if is_match:
                            return True
                    return False
                if not prev_bot_ans:
                    continue
                is_match = match_follow(prev_bot_ans, prule.follow_rules)
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
        

    def save(self, save_path: str) -> None:
        with open(save_path, 'wb') as fw:
            pickle.dump(self.patterns, fw)

    def load(self, load_path: str) -> None:
        with open(load_path, 'rb') as fr:
            patterns = pickle.load(fr)
            self.patterns = patterns

