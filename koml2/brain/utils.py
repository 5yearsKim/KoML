from korean_rule_helper import Rule
from ..tags import * 
from .blank_arg import BlankArg

def pattern2rule(pattern: PatItem) -> tuple[list[Rule], list[BlankArg]]:
    rule_holder: list[Rule] = []
    arg_holder: list[BlankArg] = []
    for item in pattern.child:
        if isinstance(item, Text):
            rule: Rule = Rule.from_str(item.val)
        elif isinstance(item, WildCard):
            rule = convert_wildcard(item) 
        elif isinstance(item, PatBlank):
            rule = Rule(blank=True, pos=item.pos, npos=item.npos)
            arg = BlankArg(key=item.key)
            arg_holder.append(arg)
        else:
            raise Exception(f'pattern converting for {item} not supported')
        rule_holder.append(rule)
    return rule_holder, arg_holder

        
def convert_wildcard(wildcard: WildCard) -> Rule:
    wc: str = wildcard.val 
    if wc == '*':
        return Rule.from_str('*')
    else:
        pos: str = wildcard.val.strip('_').upper()
        return Rule(pos=pos, optional=True)

