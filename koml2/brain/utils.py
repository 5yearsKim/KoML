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
    optional = wildcard.optional
    if wc == '*':
        return Rule.from_str('*')
    elif wc in ['_', '_?']:
        return Rule(pos='J', optional=optional)
    elif wc in ['_??']:
        return Rule(surface='?', optional=True)
    elif wc in ['_s', '_s?']:
        return Rule(pos='JKS', optional=optional)
    elif wc in ['_c' , '_c?']:
        return Rule(pos='JKC', optional=optional)
    elif wc in ['_x' , '_x?']:
        return Rule(pos='JX', optional=optional)
    elif wc in ['_o' , '_o?']:
        return Rule(pos='JKO', optional=optional)
    elif wc == '_i':
        raise Exception('wildcard _i is not allowed in pattern range')
    else:
        raise Exception(f'wildcard {wc} is not supported')

