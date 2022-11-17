from __future__ import annotations
from korean_rule_helper import Rule
from ..tags import Case, Template , PatItem
from .errors import PatternMatcherError
from .utils import pattern2rule

class PatternRule:
    def __init__(self, pattern: list[Rule], template: Template, follow_cid: list[str]=[], follow_rules: list[list[Rule]]=[]) -> None:
        self.pattern: list[Rule] = pattern
        self.template: Template = template 
        self.follow_cid: list[str] =  follow_cid
        self.follow_rules: list[list[Rule]] = follow_rules
        self.priority_score: int = self._get_priority_score(pattern)

    def __repr__(self):
        divider = f'\n****** p-score: {self.priority_score} ******'
        follow = f'{self.follow_rules}\n' if self.follow_rules else ''
        follow_cid = f'(cid : {self.follow_cid})' if self.follow_cid else ''
        return f'{divider}\nFollow {follow_cid}\n{follow}Pattern\n{self.pattern}'

    def _get_priority_score(self, pattern: list[Rule]) -> int :
        return 0

    @staticmethod
    def from_case(case: Case) -> list[PatternRule]:
        holder : list[PatternRule] = []
        for idx in range(len(case.pattern.children)):
            pat_item: PatItem = case.pattern.children[idx]
            pat_rule = pattern2rule(pat_item)
            if (case.follow):
                follow_rules = list(map(lambda x: pattern2rule(x), case.follow.children))
                cid = case.follow.cid
            else: 
                follow_rules = []
                cid = [] 
            item = PatternRule(pat_rule, case.template, follow_cid=cid, follow_rules=follow_rules)
            holder.append(item)
        return holder

        




    


    

