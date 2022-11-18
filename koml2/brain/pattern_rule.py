from __future__ import annotations
from korean_rule_helper import Rule
from ..tags import Case, Template , PatItem
from .utils import pattern2rule
from .blank_arg import BlankArg

class PatternRule:
    def __init__(self, pattern: list[Rule], args: list[BlankArg], template: Template,\
            cid: str|None=None, follow_cid: list[str]=[], follow_rules: list[list[Rule]]=[]) -> None:
        self.pattern: list[Rule] = pattern
        self.args: list[BlankArg] = args
        self.template: Template = template 
        self.cid: str|None = cid 
        self.follow_cid: list[str] =  follow_cid
        self.follow_rules: list[list[Rule]] = follow_rules
        self.priority_score: int = self._get_priority_score(pattern)

    def __repr__(self) -> str:
        divider = f'\n****** p-score: {self.priority_score} ******'
        follow_cid = f'(cid : {self.follow_cid})' if self.follow_cid else ''
        return f'{divider}\nFollow {follow_cid}\n{self.follow_rules}\nPattern\n{self.pattern}\nArgs\n{self.args}'

    def _get_priority_score(self, pattern: list[Rule]) -> int :
        score = 10
        for rule in pattern:
            surface = rule.surface
            if surface and surface == '*':
                score -= 2
            elif surface:
                score += len(surface)
            elif rule.optional:
                score -= 1
            elif rule.blank:
                score -= 2
        if self.follow_cid:
            score += 5
        if self.follow_rules:
            score += 3
        return score

    def key_arg(self, key: str) -> str|None:
        for arg in self.args:
            if arg.key == key:
                return arg.val
        return None


    def idx_arg(self, idx: int) -> str|None:
        if idx not in range(1, len(self.args) + 1):
            raise IndexError(f'arg index {idx} out of range({len(self.args)})')
        return self.args[idx - 1].val

    @staticmethod
    def from_case(case: Case) -> list[PatternRule]:
        holder : list[PatternRule] = []
        for idx in range(len(case.pattern.children)):
            pat_item: PatItem = case.pattern.children[idx]
            pat_rule, args = pattern2rule(pat_item)
            cid = case.id
            if (case.follow):
                follow_rules = list(map(lambda x: pattern2rule(x)[0], case.follow.children))
                follow_cid = case.follow.cid
            else: 
                follow_rules = []
                follow_cid = [] 
            item = PatternRule(pat_rule, args, case.template, \
                cid=cid, follow_cid=follow_cid, follow_rules=follow_rules)
            holder.append(item)
        return holder

        




    


    

